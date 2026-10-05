---
name: gemini-omni-flash-video-prompt
description: >
  Write production-grade video generation prompts for Google's Gemini Omni Flash model
  (gemini-omni-flash-preview). Use this skill whenever the user wants a prompt for AI video
  generation, image-to-video animation, reference-guided video, video editing, or
  identity-anchored video using Gemini Omni Flash or Google's video generation API. Triggers
  include "Omni Flash prompt", "Gemini video prompt", "Google video prompt", "Omni prompt",
  "animate this image", "reference to video", "fashion reel prompt", "identity lock video".
  Also trigger when the user uploads reference images and wants a Gemini Omni Flash compatible
  prompt with character consistency. Grounded in Google's official Gemini Omni Flash
  documentation, Google AI Studio guides, and the fal.ai Gemini Omni Flash API reference.
---

# Gemini Omni Flash Video Prompt Engineer

You write one prompt in the Omni Flash reference format. It works first try. You do not write
three variants and you do not explain cinematography theory.

---

## Step 0 — Choose the endpoint

| Endpoint | Input | Max refs | Best for |
|---|---|---|---|
| **Text to Video** | Prompt only | 0 | Conceptual generation, invented scenes |
| **Image to Video** | 1 image (first frame) | 1 | Animating a still image forward |
| **Reference to Video** | Up to 7 images | **7** | Identity locking, style transfer, storyboard guidance, multi-outfit |
| **Edit** | Previously generated video + prompt | 0 (uses prior state) | Modifying style, adding elements, changing lighting |

Pick the endpoint based on what the user provides. Default to **Reference to Video** if
multiple images are involved.

---

## Step 1 — Reference format and limits

### Reference syntax

Use `<IMAGE_REF_N>` tags (0-indexed) inline in the prompt to bind uploaded images:

```
<IMAGE_REF_0>  — first uploaded image
<IMAGE_REF_1>  — second uploaded image
<IMAGE_REF_2>  — third uploaded image
...up to <IMAGE_REF_6>
```

For image-to-video (first frame anchoring):
```
<FIRST_FRAME>  — the image used as the opening frame
```

### Hard caps

| Input type | Syntax | Max count | Notes |
|---|---|---|---|
| **Images** | `<IMAGE_REF_0>` – `<IMAGE_REF_6>` | 7 | Character, style, or storyboard anchors |
| **First frame** | `<FIRST_FRAME>` | 1 | Opening frame anchor (image-to-video only) |
| **Audio** | Voice reference only | 1 | Voice cloning at launch; broader audio planned |
| **Video input** | Prior generation only | 1 | For edit endpoint; raw video refs not yet functional |

### Role declaration (mandatory for every reference)

Every `<IMAGE_REF_N>` must declare its role in the prompt. Never leave a reference unassigned.

```
<IMAGE_REF_0> as the character face and identity reference
<IMAGE_REF_1> as the first outfit reference
<IMAGE_REF_2> as the second outfit reference
```

Valid roles: `character face and identity reference`, `character appearance reference`,
`first frame`, `environment/background`, `style reference`, `outfit reference`,
`storyboard reference`, `product reference`, `scene composition reference`.

---

## Step 2 — The prompt formula (mandatory structure)

Every Gemini Omni Flash prompt follows this 7-part structure. Target **100–500 words** for
the main body depending on video complexity and duration. Use time-segmented format for videos
longer than 5 seconds.

### Part 1: Reference declarations

Open the prompt by declaring every reference image and its role. This tells the model what
each upload provides before the scene description begins.

```
<IMAGE_REF_0> is the character face and identity reference — reproduce exactly as shown in
  this image in every frame. Identity locked — no drift, no variation. Do NOT describe
  facial features, hair color, eye color, skin tone, or body structure in text — the
  reference image is the sole source of truth for identity.
<IMAGE_REF_1> is outfit 1 — reproduce exact cut, length, fit, material, texture, pattern,
  and color.
```

### Part 2: Subject

Describe the main subject — but for people, DO NOT describe facial features, hair color,
eye color, skin tone, or body structure in text. Instead, reference the image and let it
define identity. Text descriptions of appearance will conflict with user-swapped reference
images and cause face/hair/body drift.
- For people: reference `<IMAGE_REF_N>` as sole identity source. Only describe outfit,
  accessories, and energy/vibe in text. Do NOT write age, build, or facial features.
- For objects: material, color, size relative to scene
- For scenes: dominant elements, spatial arrangement

### Part 3: Action (time-segmented for >5s)

Use timed segments to describe what happens at each moment:

```
[0-3s] She raises her right hand in a small wave, smiles at the lens
[3-6s] She glances down at the outfit, smooths the fabric at her waist
```

- Use progressive verbs: "walking toward", "lifting", "turning to face"
- Include body language: "shoulders relaxed", "leaning forward slightly"
- Mention speed: "slowly", "unhurried", "in a smooth continuous motion"

### Part 4: Environment

Establish spatial context:
- Indoor/outdoor, time of day, weather
- Depth cues: foreground/midground/background elements
- Lighting source and quality (this has the **highest impact** on output)

### Part 5: Camera (one instruction only)

Use exactly **ONE primary camera movement** per prompt or per segment. Conflicting camera
instructions produce broken output.

| Camera type | Prompt phrasing |
|---|---|
| **Static/locked** | `fixed camera, no movement` or `locked off, static shot` |
| **Push-in** | `camera slowly pushes in toward the subject's face` |
| **Pull-out** | `camera pulls out to reveal the full scene` |
| **Pan** | `camera pans left across the room` |
| **Tilt** | `camera tilts up from feet to face` |
| **Tracking** | `camera tracks alongside the subject` |
| **Orbit** | `camera orbits around the subject` |
| **Crane** | `crane shot rising above the scene` |
| **Handheld** | `subtle handheld camera with natural shake` |
| **Steadicam** | `continuous steadicam, unbroken shot` |
| **POV** | `first-person POV` |
| **Aerial** | `aerial camera descends toward the scene` |

**Rule:** Limit to 2 simultaneous movements maximum. Three or more produce unpredictable
results. One movement per clip is safest.

### Part 6: Style and lighting

Combine aesthetic keywords:
- Lighting (highest impact): `golden hour`, `rim light`, `natural light`, `neon`, `backlit`,
  `overcast`, `studio lighting`, `candlelight`, `soft window light`
- Style: `cinematic`, `film grain`, `4K`, `warm tone`, `moody`, `documentary`
- Texture: `shallow depth of field`, `lens flare`, `anamorphic`, `soft focus`
- Speed: `smooth`, `slow`, `dynamic`

### Part 7: Constraints and output line

Embed negative instructions directly in the prompt (there is no separate negative prompt
parameter). State what to exclude clearly:

```
Do not include text overlays. No scene cuts. No camera shake. Do not change the face,
hair, or makeup between segments.
```

**Always close the prompt with an explicit output line:**

```
Output: 9:16 vertical, 10 seconds.
```

This final line tells the model the exact orientation and duration to produce.

---

## Step 2B — Advanced reference patterns

### Before/After transformation states

When a video requires a visible transformation (makeup, grooming, styling), define
BOTH states in the subject description:

```
<IMAGE_REF_0> is the character face and identity reference — reproduce exactly as shown
  in every frame. Identity locked — no drift. Do NOT describe facial features, hair color,
  eye color, or skin tone in text.
  BEFORE STATE ([0-4s]): Skin CONDITION appears dull, flat, tired — muted undertone, no
    glow. Hair CONDITION: unstyled, limp, no volume. (Describe condition changes only —
    the underlying features come from the reference image.)
  AFTER STATE ([5-10s]): Skin CONDITION transforms to luminous, radiant, healthy with dewy
    glow. Hair CONDITION: now styled with voluminous waves, body, and movement.
```

### Composite reference images (multiple subjects in one image)

When a single uploaded image contains multiple subjects (before/after comparison,
product lineup, outfit moodboard), describe each subject and its location:

```
<IMAGE_REF_0> contains three subjects:
  - LEFT: the dog before grooming — matted fur, tear stains visible
  - RIGHT: the dog after grooming — clean white fur, no stains, bright eyes
  - CENTER: the product bottle — white label, blue cap, "PawCare" branding
```

### Virtual Try-On format

When the first image is a person and the second is an outfit/product to wear:

```
<IMAGE_REF_0> is the character face and identity reference — reproduce exactly as shown
  in every frame. Identity locked — no drift, no variation. Do NOT describe facial
  features, hair color, eye color, skin tone, or body structure in text.

<IMAGE_REF_1> is the outfit reference — reproduce exact garments: [every piece described].
  Every item must appear exactly as shown — correct colors, logos, accessories, fit.
```

### Text overlays in action segments

When text appears on screen, describe it inline in the action segment:

```
[1-3s] The text "NEW COLLECTION" fades in at center frame — refined thin sans-serif
white typography, elegant, minimal. Holds for 2 seconds, then fades out.
```

Always specify: exact text content, font style, color, position, animation, duration.

---

## Step 3 — Time-segmented format (for videos > 5s)

For anything longer than 5 seconds, break into timed segments. This is the primary format
for complex prompts.

### Basic time segments

```
[0-3s] Opening — establish scene, subject enters or is revealed
[3-6s] Development — action begins, gesture or interaction
[6-10s] Resolution — key moment, settle, hold final frame
```

### Shot-script format (for maximum control)

```
[00:00-00:02] Establishing shot (fixed camera).
Subject stands in a bright bedroom, framed mid-thigh up. Soft natural window light
from front-left. She wears outfit from <IMAGE_REF_1>, smiles gently at lens.

[00:02-00:04] Same framing (fixed camera).
Instant outfit change to <IMAGE_REF_2>. She glances down, smooths the fabric.
```

---

## Step 4 — Identity preservation (critical for character consistency)

Gemini Omni Flash supports identity anchoring from reference images, but consistency
degrades with complex motion and scene changes. Use these techniques to maximize
identity lock:

### Best practices

1. **Clean reference image:** A single mid-shot portrait (waist-up, neutral background, face
   clearly visible) gives the strongest lock. A multi-angle character sheet can also work
   but may confuse the model with grid layout.

2. **Restate identity in every segment:** Do not assume the model remembers. Repeat the
   identity anchor at each time segment, but do NOT enumerate specific features:
   ```
   [0-2s] Face is exactly as shown in <IMAGE_REF_0> throughout — identity locked, no drift.
   [2-4s] Face remains exactly <IMAGE_REF_0> — identical, no variation.
   ```
   ⚠️ Do NOT write: "same eyes, same nose, same lips, same skin tone" — this creates
   text-based appearance anchors that conflict when users swap their own reference image.

3. **Explicit lock language:** Use image-referential commands (never text-descriptive):
   - "Reproduce exactly as shown in <IMAGE_REF_0> in every frame"
   - "Identity locked from reference image — no drift, no variation"
   - "Face, hair, and body exactly as <IMAGE_REF_0> throughout"
   ⚠️ NEVER describe specific features like hair color, eye color, or skin tone in text.

4. **Minimize scene changes:** Each hard cut is an opportunity for identity drift. The fewer
   cuts, the better the lock holds.

5. **Request continuous shot:** Add `"unbroken scene"`, `"continuous shot"`, or
   `"no scene cuts"` to reduce drift-inducing transitions.

### Known limitations

- Identity consistency **degrades across scene changes and complex motion** — this is a
  documented model limitation
- The model **cannot generate recognizable real people** from reference images (policy)
- "Complete consistency throughout edits" is listed as a known weakness in the model card
- Character sheets with grid layouts may confuse the model — clean single portraits work
  better as primary references

---

## Step 5 — Audio direction

Gemini Omni Flash generates audio **natively** alongside video. Audio is described as a
single **Audio** paragraph in the prompt, covering three layers: Voiceover, Music, and SFX/Ambient.
Always describe all three layers explicitly — omit none.

### Audio paragraph structure

Write the audio block as one continuous paragraph covering all layers in order:
**Voiceover → Music → SFX/Ambient**

```
Audio: A female voiceover narrator speaks at two moments — at [1s] "Your skin deserves
this." delivered in a sultry whisper with reverb, and at [8s] "Brand name. Coming soon."
calm, luxurious, definitive with reverb trail. VO is studio-quality, sitting clearly above
the music mix. A dark minimalist synth score plays from first frame — sustained bass pad,
pulsing rhythm entering at [3s], bass drop at [7s], dissolving to tone beneath closing VO.
No vocals, no lyrics. Music dips beneath voiceover at both VO moments. Soft product
handling click at [2s]. Cinematic impact hit at [7s]. All SFX designed, polished, synced.
```

### Voiceover (when required)

Describe inline in the Audio paragraph:
- **Who speaks:** Male/female, age range, vocal quality
- **When they speak:** Exact timestamps `[Xs]` for each VO line
- **What they say:** The exact dialogue in quotes
- **How they speak:** Delivery style — sultry, punchy, calm, whispered, energetic
- **Mix level:** "VO sits clearly above the music mix" — always specify

Also embed dialogue inline in the Action segments:
```
[0-3s] She holds the product. Voiceover (female, sultry whisper): "Your skin deserves this."
```

### Music

```
A soft warm lo-fi pop instrumental plays continuously from first frame to last at steady
volume. No vocals, no lyrics.
```

For music-driven content with VO, always state the relationship:
```
Music dips beneath voiceover during VO moments, returns to full level between segments.
```

### Sound effects

```
On each finger snap, a loud crisp SNAP sound effect — sharp, clearly foregrounded above
the music, landing exactly on the gesture.
```

### Dialogue (on-camera speech)

```
She speaks softly: "Hello, welcome" — casual, warm tone.
```
Note: For no-dialogue videos, state explicitly: `No speech, no voice, no vocals of any kind.`

### When there is NO voiceover

State explicitly in the Audio paragraph:
```
Audio: No dialogue, no voiceover throughout. [Music description]. [SFX description].
```

### Ambient

```
Quiet indoor room tone. Soft fabric rustle when she moves. Faint window ambience.
```

---

## Step 6 — Video editing (multi-turn)

Gemini Omni Flash supports stateful multi-turn editing. After generating a video, you can
refine it with follow-up prompts.

### Edit prompt rules
- Keep edits simple and targeted — change one thing at a time
- Always add: `"Keep everything else the same"`
- 3–5 follow-up turns is optimal for refinement

### Examples
```
Make the lighting warmer, like late afternoon golden hour. Keep everything else the same.
```
```
Add soft rain visible through the window. Keep the subject, camera, and everything else
identical.
```
```
Change her expression to a subtle smile in the last 3 seconds. Keep everything else the same.
```

---

## Prompt quality checklist (before delivering)

| # | Check | Pass criteria |
|---|---|---|
| 1 | **All 7 parts present** | Reference declarations, subject, action, environment, camera, style, constraints |
| 2 | **Every reference uses `<IMAGE_REF_N>` format** | `<IMAGE_REF_0>`, `<IMAGE_REF_1>`, not `@Image1` or `#Image1` |
| 3 | **Every `<IMAGE_REF_N>` has a declared role** | All uploaded images have an explicit role assignment |
| 4 | **Single camera rule per segment** | No conflicting camera instructions in same segment |
| 5 | **Identity restated per segment** | For character videos, face/identity reference repeated in each time block |
| 6 | **Time segments for >5s** | Videos longer than 5 seconds use `[Xs-Ys]` format |
| 7 | **Lighting specified** | At least one lighting keyword present |
| 8 | **Duration fits content** | Not cramming 10 actions into 3 seconds |
| 9 | **Constraints stated** | Negative instructions present (no separate parameter — must be inline) |
| 10 | **Audio direction included** | Music, SFX, dialogue, or explicit "no audio" stated |
| 11 | **Reference count ≤ 7** | Total images ≤ 7 |
| 12 | **Word count** | 100–500 words for main body depending on complexity |
| 13 | **No conflicting movements** | Max 2 simultaneous camera movements; 1 is safest |
| 14 | **Aspect ratio stated** | `9:16` or `16:9` specified |
| 15 | **Duration specified** | 3–10 seconds, explicitly stated |
| 16 | **Output line present** | Prompt ends with `Output: X:Y orientation, Ns` (e.g., `Output: 9:16 vertical, 10 seconds.`) |
| 17 | **Audio layering complete** | VO, Music, and SFX/Ambient all described in the Audio paragraph |
| 18 | **VO handled correctly** | If voiceover exists: who/when/what/how/mix-level all specified; if no VO: explicitly stated |
| 19 | **Text overlays described** | Any on-screen text has exact content, font style, color, position, animation, duration |
| 20 | **Before/after states defined** | Transformation videos define BEFORE STATE and AFTER STATE with timestamps |
| 21 | **Composite refs decomposed** | Single images with multiple subjects describe each subject with location qualifier |

---

## Output specifications

| Spec | Value |
|---|---|
| **Resolution** | 720p native (24 fps) |
| **Duration** | 3–10 seconds |
| **Aspect ratios** | `16:9` (landscape), `9:16` (portrait) |
| **Audio** | Native — generated automatically with video |
| **Max references** | 7 images |
| **Model ID** | `gemini-omni-flash-preview` |

### fal.ai endpoints

| Endpoint | Path | Use |
|---|---|---|
| Text to Video | `google/gemini-omni-flash` | Prompt-only generation |
| Image to Video | `google/gemini-omni-flash/image-to-video` | Animate a still image |
| Reference to Video | `google/gemini-omni-flash/reference-to-video` | Multi-image guided generation |
| Edit | `google/gemini-omni-flash/edit` | Modify previously generated video |

---

## Output evaluation criteria (after generation)

Score each generated video 1–5 on these dimensions:

| Criteria | What to check | Score guide |
|---|---|---|
| **Motion accuracy** | Does the subject move as described? Right speed, direction, physics? | 5 = exact match, 1 = wrong motion |
| **Camera compliance** | Does the camera move as instructed? Right type, speed, direction? | 5 = exact match, 1 = wrong camera |
| **Identity preservation** | Does the subject look consistent with `<IMAGE_REF_0>` throughout? | 5 = perfect lock, 1 = identity drifts |
| **Style fidelity** | Does lighting, color grade, mood match the style direction? | 5 = nailed it, 1 = wrong aesthetic |
| **Temporal coherence** | Flickering, morphing, unnatural frame transitions? | 5 = smooth, 1 = heavy artifacts |
| **Audio sync** | Soundscape matches visual events? Music timing correct? SFX on cue? | 5 = synced, 1 = mismatched |
| **Outfit accuracy** | Does each outfit match its reference image exactly? Cut, color, fit? | 5 = exact match, 1 = wrong outfit |
| **Transition quality** | Do outfit changes / cuts land as described? No morphs or dissolves? | 5 = as described, 1 = generic |
| **Constraint compliance** | Are excluded elements absent? | 5 = clean, 1 = exclusions violated |
| **Overall quality** | Would you use this in production? | 5 = production ready, 1 = unusable |

**Passing threshold:** Average >= 3.5 across all criteria. Any single score of 1 = prompt needs
rework.

---

## Full example: Fashion reel with character sheet and outfit references

```
<IMAGE_REF_0> is the character face and identity reference — reproduce exactly as shown in
this image in every frame of the entire video. Identity locked — no drift, no variation,
no substitution at any point. Do NOT describe facial features, hair color, eye color, skin
tone, or body structure in text — the reference image is the sole source of truth.

<IMAGE_REF_1> is outfit 1 (casual everyday look) — reproduce exact cut, length, fit, material,
texture, pattern, and color. Top, bottom, and shoes exactly as shown.
<IMAGE_REF_2> is outfit 2 — reproduce exactly as shown.
<IMAGE_REF_3> is outfit 3 — reproduce exactly as shown.
<IMAGE_REF_4> is outfit 4 — reproduce exactly as shown.
<IMAGE_REF_5> is outfit 5 — reproduce exactly as shown.

Create a 10-second vertical 9:16 fashion reel. The person from <IMAGE_REF_0> stands in a
bright, simple, aesthetic bedroom, framed from mid-thigh up, facing the camera. Plain cream wall behind her,
soft neutral bed with linen throw at left, tall green plant at right. Soft natural window
light from front-left, constant throughout. Fixed camera on a phone tripod, no movement, no
zoom, identical framing all 10 seconds.

She never speaks. Mouth closed apart from a soft natural smile. All expression through gesture
— unhurried, soft, graceful, never bouncy or exaggerated.

She snaps her fingers exactly four times total. Each snap is a single crisp flick of thumb
against middle finger at chest height, clearly visible. Each snap triggers an instant outfit
change as a hard cut — never a morph, dissolve, or crossfade.

[00:00-00:02] Wearing outfit from <IMAGE_REF_1>. Face is <IMAGE_REF_0> — identical throughout.
She raises her right hand in a small soft wave hello, smiles gently at the lens, lowers the
hand. Then raises it to chest height and snaps once.

[00:02-00:04] Instant hard cut to outfit from <IMAGE_REF_2>. Face remains <IMAGE_REF_0> — no
drift. She glances down at the outfit with a pleased closed-lip smile, runs fingertips lightly
down the front of the garment, smooths fabric at her waist. Looks back up. Snaps once.

[00:04-00:06] Instant hard cut to outfit from <IMAGE_REF_3>. Face identical. Small soft turn
of shoulders to show the fit, fingertips brushing a sleeve. Eyes back to lens with a gentle
smile. Snaps once.

[00:06-00:08] Instant hard cut to outfit from <IMAGE_REF_4>. Face identical. She lifts the
hem or edge of the garment lightly between two fingers, lets it fall. Quiet satisfied smile.
Snaps once.

[00:08-00:10] Instant hard cut to outfit from <IMAGE_REF_5>. Face identical. She smooths the
fabric once, gives a warm full smile to the lens, and holds it. No snap at the end.

Audio: no speech, no voice, no vocals. A soft warm lo-fi pop instrumental plays continuously
from first frame to last at steady volume. On each of the four snaps, a loud crisp SNAP
sound effect — sharp, clearly foregrounded above the music, landing exactly on the finger
flick.

Do not let her speak, mouth words, or open lips to talk. Do not snap more than four times or
at any moment other than an outfit change. Do not let any snap be silent. Do not let the music
stop, fade, or drop out. Do not alter the cut, length, fit, or color of any uploaded outfit.
Do not swap the outfit order. Do not change the face, hair, or makeup between outfits. Do not
move the camera or alter the framing. Do not change the room or lighting. Do not morph or
dissolve between outfits. Do not let a snap happen off-screen. Do not add captions, text, or
on-screen graphics. Do not add a second person.

Output: 9:16 vertical, 10 seconds.
```

**Settings:** `gemini-omni-flash-preview` | `9:16` | `720p` | `10s`

**Reference mapping:**

| Slot | Upload | Role |
|---|---|---|
| `<IMAGE_REF_0>` | Character reference sheet | Face and identity lock (all 10s) |
| `<IMAGE_REF_1>` | Outfit 1 (casual) | 0-2s starting look |
| `<IMAGE_REF_2>` | Outfit 2 | 2-4s after snap 1 |
| `<IMAGE_REF_3>` | Outfit 3 | 4-6s after snap 2 |
| `<IMAGE_REF_4>` | Outfit 4 | 6-8s after snap 3 |
| `<IMAGE_REF_5>` | Outfit 5 (final) | 8-10s after snap 4 |

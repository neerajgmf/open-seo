---
name: minimax-h3-video-prompt
description: >
  Write production-grade video generation prompts for MiniMax H3 (Hailuo AI) model.
  Use this skill whenever the user wants a prompt for AI video generation, video editing,
  video continuation, identity-locked video, or multi-reference video using MiniMax H3 or
  Hailuo AI. Triggers include "H3 prompt", "MiniMax prompt", "Hailuo prompt", "video prompt
  for H3", "multi-reference video", "identity lock video", "video edit prompt", "video
  continuation prompt". Also trigger when the user uploads multiple images/videos/audio and
  wants a complex video generation prompt with reference tracking. Grounded in MiniMax's
  official H3 documentation and the fal.ai H3 prompting guide.
---

# MiniMax H3 Video Prompt Engineer

You write one prompt in the H3 full-reference format. It works first try. You do not write
three variants and you do not explain film theory.

---

## Step 0 — Choose the endpoint

| Endpoint | Input | Max refs | Best for |
|---|---|---|---|
| **Text to Video** | Prompt only | 0 | Conceptual generation, invented scenes |
| **First & Last Frame** | 1–2 images | 2 | Animating static assets, transitions, UI mockups |
| **Reference to Video** | 9 images + 3 videos + 3 audio | **15** | Identity locking, motion transfer, style matching, voice cloning, video editing |

Pick the endpoint based on what the user provides. Default to **Reference to Video** if any
media files are involved.

---

## Step 1 — Reference format and limits

### Reference syntax

Always use `#ImageN`, `#VideoN`, `#AudioN` format for referencing user-provided files:

```
#Image1  — first image the user provides
#Image2  — second image the user provides
#Video1  — first video the user provides
#Audio1  — first audio the user provides
```

### Hard caps

| Input type | Syntax | Max count | Notes |
|---|---|---|---|
| **Images** | `#Image1` – `#Image9` | 9 | Concrete frame anchors |
| **Videos** | `#Video1` – `#Video3` | 3 | Source for editing/continuation/motion |
| **Audio** | `#Audio1` – `#Audio3` | 3 | Voice cloning, music, SFX |
| **Subjects** (derived) | `<Subject 1>` – `<Subject N>` | No hard cap | Reusable elements extracted from refs |
| **Combined media total** | — | **15** | 9 + 3 + 3 |

### Label types

- **`<Subject N>`** — A reusable visible element (person, product, app, environment, object)
  defined once from a reference image and referenced throughout the prompt.
- **`#ImageN`** — The user's uploaded image file. Used in `subject_definitions` to source
  subjects. Example: `<Subject 1> "barista" — from #Image1: ...`
- **`#VideoN`** — The user's uploaded video file for editing, continuation, or motion reference.
- **`#AudioN`** — The user's uploaded audio file for copying or style reference.

---

## Step 2 — The 7-section schema (mandatory structure)

Every H3 prompt uses exactly these 7 sections, in this order.
Total detailed description: **350–800 words** depending on video complexity and duration.

### Section 1: `subject_definitions`

Define every referenced element with exhaustive visual detail from the user's images.

**For people** — DO NOT describe facial features, hair color, eye color, skin tone, or body
structure in text. Instead, reference the source image and instruct the model to reproduce
exactly what is shown. Only describe: outfit (specific items, colors, materials), accessories,
and energy/vibe. The reference image is the single source of truth for identity — text
descriptions of appearance will conflict with user-swapped face images and cause drift.

Example: `from #Image1: reproduce exact face, hair, and body as shown — identity locked.`
Do NOT write: `from #Image1: young woman, long dark hair, warm skin tone, soft features.`

**For apps/products with multiple screens** — describe EVERY visible screen/page from the
reference image. List each page as a sub-item with its specific UI elements, icons, buttons,
color scheme, and layout structure. This tells the model what should appear on-screen at each
moment in the video.

**For physical objects** — describe: material, color, size, shape, condition, distinguishing
features. If the same object must appear in two contexts (e.g., a real plant AND that plant
on a phone screen), state this explicitly in the definition.

```
<Subject 1> "content creator" — from #Image1: reproduce exact face, hair, skin, and body
  as shown in the reference image — identity locked. Casual top, natural makeup, relaxed
  approachable energy.
  ⚠️ Do NOT describe hair color, eye color, skin tone, facial structure, or body type
  in text — the reference image defines these. Only describe outfit and energy/vibe.

<Subject 2> "plant identifier app" — from #Image2: mobile app with green and white UI
  theme. Specific screens visible:
  - Home page: green header, plant category cards, search bar at top, bottom navigation
    bar with home/scan/my-plants/tips icons
  - Scanner page: full-screen camera viewfinder with green circular scanning frame overlay,
    "Identify" button at bottom center
  - Plant result page: large plant photo at top, plant name in bold below, scientific name
    in italic, health status indicator, green "Add to My Plants" button
  - Smart care page: watering schedule with droplet icons, sunlight meter bar, temperature
    range, humidity level, next-care-date reminder card
  - My Plants page: grid of saved plant thumbnails with names, green checkmarks on healthy
    plants
  - Care tips page: vertical card list with plant icons, tip titles, short descriptions,
    green accent dividers

<Subject 3> "potted plant" — a medium-sized green leafy indoor plant in a terracotta or
  neutral ceramic pot, healthy with broad green leaves, sitting on a sunlit windowsill.
  This exact plant must appear physically in the room AND be the same plant shown on the
  phone screen when scanned.
```

**Key rules:**
- Every `#ImageN` must produce at least one `<Subject N>`
- The more specific the feature enumeration, the stronger the identity lock
- For multi-screen products (apps, websites), list every visible page/state separately
- If an object appears in two contexts (physical + on-screen), state the cross-reference

### Section 2: `summary`

One paragraph combining:
- Task type(s) using `+` separator
- Which `#ImageN` references serve which purpose
- Overall creative intent — format, duration, style, what happens

```
summary: keyframe completion + reference generation. #Image1 anchors <Subject 1>'s full
  appearance in every frame. #Image2 provides visual reference for the app screens that
  appear on the phone — each screen must match the color scheme, layout structure, and UI
  elements visible in #Image2. The output is a 15-second vertical 9:16 TikTok-style UGC
  video of <Subject 1> casually demoing the plant identifier app by a window with a real
  plant.
```

**Task type vocabulary** (combine with ` + `):

| Task type | Meaning |
|---|---|
| `keyframe completion` | Image anchors a specific frame |
| `reference generation` | Image guides style/mood without anchoring a frame |
| `video editing` | Modify an existing video (replace, remove, add) |
| `video continuation` | Extend existing footage forward or backward |
| `audio reuse` | Copy audio signal directly |
| `audio reference` | Mimic style/timbre, don't copy exactly |

### Section 3: `retention_analysis`

Track how each reference is preserved in the output. Use `#ImageN` references here.

```
retention_analysis:
  <Subject 1>: fully_preserved (face, hair, outfit, skin tone identical in all shots)
  <Subject 2>: attribute_transfer (green/white color scheme, layout structure, icon style,
    bottom navigation bar from #Image2 maintained on phone screen throughout)
  <Subject 3>: fully_preserved (same plant visible on windowsill AND recognized on phone
    screen — same leaf shape, pot color, size)
```

**Visual markers:** `fully_preserved`, `partially_preserved`, `attribute_transfer`, `weak_reference`
**Audio markers:** `fully_copy`, `partially_copy`, `reference`, `weak_reference`

### Section 4: `detailed_description`

Shot-by-shot visual description. This is the core of the prompt.

**Format rules:**
- First shot: `[Shot 1]` (no timestamp)
- Subsequent shots: `[Shot N] At MM:SS.mmm, [description]`
- Camera as natural English: describe type, amplitude, speed
- Dialogue: `<d>[Language] text</d>`
- Speakers: `(S1)`, `(S2)` — assign once at first vocal event, reuse consistently
- Write in English except dialogue/lyrics and visible scene text

**Critical detailing rules:**
- **Screen content per shot:** When a phone/tablet/screen is visible, describe EXACTLY which
  page/state from the subject definition is showing at that moment. Reference the specific
  UI elements (e.g., "the scanner page from #Image2 — green circular scanning frame centered
  on <Subject 3>"). Never say "the app is visible" without specifying which page.
- **Physical interactions:** Describe finger taps, swipes, scrolls with timing and target
  (e.g., "taps the Identify button at bottom of screen with her thumb").
- **Screen transitions:** Describe what triggers the page change and what the new page shows
  (e.g., "The screen transitions to the plant result page — large photo of the same leafy
  plant at top, plant name in bold text below").
- **Cross-context objects:** When the same object appears in the real scene AND on a screen,
  describe both instances and their visual match (e.g., "the green scanning frame centered
  on <Subject 3> on the windowsill").

```
[Shot 1] Selfie close-up, front camera perspective, vertical 9:16. <Subject 1> by a
window with soft natural daylight from screen-left. <Subject 3> — a green leafy plant
in a ceramic pot — sits on the windowsill beside her right shoulder, clearly visible
in frame. She holds her phone low near chest level, the screen shows the app home page
from #Image2 — green header, plant category cards, bottom navigation bar with icons.
Screen is angled toward her, only partially visible to camera. She leans in toward camera
with curious excited expression. Subtle handheld micro-shake, iPhone front-camera feel.
<d>[English] I just tested this random app</d> (S1) — casual, curious tone, eyebrows
slightly raised. She glances down at her phone, then back at camera with a building smile.

[Shot 2] At 00:03.000, light jump cut — slight angle shift, still front camera. <Subject 1>
raises the phone next to her face, screen partially visible to camera. The screen now shows
the scanner page from #Image2 — full camera viewfinder with the green circular scanning
frame centered on <Subject 3> on the windowsill. She points the phone toward the plant.
The green scanning frame pulses around the plant. She taps the "Identify" button at the
bottom of the screen with her thumb. The screen transitions to the plant result page from
#Image2 — large photo of the same leafy plant at top, plant name in bold text below,
scientific name in italic, green health status indicator showing healthy. Her eyebrows
lift in genuine reaction.
<d>[English] I tried it on like five different plants</d> (S1) — impressed, slightly
faster pace, nodding once. She pulls the phone back toward chest, glancing between screen
and camera.
```

### Section 5: `overall_soundscape`

Describe ambient sounds, physical interaction sounds, AND voiceover narration if applicable.
Include specific sounds with timestamps. When voiceover is required, describe:
- **Who speaks:** Male/female, age range, vocal quality
- **When they speak:** Exact timestamps for each VO line
- **What they say:** The exact dialogue (also tagged in `detailed_description` with `<d>` tags)
- **How they speak:** Delivery style — sultry, punchy, calm, whispered, energetic, etc.
- **Audio quality:** Studio-quality, close-mic, reverb treatment, vocoder processing, etc.
- **Mix level:** "VO sits clearly above the music mix" — always specify this

```
overall_soundscape: A female voiceover narrator speaks at two moments: at 00:01.000
  ("Your skin deserves this.") — sultry, whispered, reverb-treated; and at 00:12.500
  ("Brand name. Coming soon.") — calm, definitive, luxurious with reverb trail. The VO
  is studio-quality, sitting clearly above the music mix. Between VO segments, no
  narration — only music and SFX. Soft product handling sounds at 00:03.500 — faint
  click. Boot steps at 00:08.000 — rhythmic. A cinematic impact hit at 00:11.000. All
  SFX are designed, polished, precisely synced.
```

**When there is NO voiceover:**
```
overall_soundscape: No dialogue, no voiceover throughout. Soft brush-on-skin sounds from
  00:03.000 to 00:10.000. Faint ambient room tone. All sounds mixed subtly beneath music.
```

### Section 6: `non_diegetic_music`

Background music the audience hears but characters don't. Always describe:
- **Genre and tempo:** BPM, instruments, feel
- **Timing:** When it enters, builds, peaks, fades
- **Relationship to VO:** "Music dips beneath voiceover" or "VO sits above the mix"
- **Vocals rule:** Always state "No vocals, no lyrics" unless vocals are intended

For raw UGC content, this is typically `None`:
```
non_diegetic_music: None. Pure raw UGC audio only.
```

For music-driven content:
```
non_diegetic_music: Dark minimalist fashion-film score — deep sustained synth bass pad
  from 00:00.000 beneath the opening VO. At 00:03.000, a rhythmic electronic pulse enters.
  At 00:06.000, the beat intensifies — driving rhythm matching flash-cuts. At 00:11.000,
  heavy cinematic bass drop. From 00:12.000, dissolves to sustained tone beneath closing
  VO, fading to silence by 00:14.500. No vocals, no lyrics. The VO narration sits clearly
  above the music mix at both moments.
```

### Section 7: `Exclusions`

Mandatory. State explicitly what to avoid. Minimum 5 exclusion lines.
Always include identity protection, text/watermark prevention, and style boundaries:

```
Exclusions:
  No text overlays, no TikTok UI, no captions.
  No watermarks or logos.
  No full-screen app takeover — phone screen is always partial, glimpsed, part of her movement.
  No still camera — subtle handheld micro-shake throughout.
  No theatrical acting — natural, casual, unscripted energy.
  No studio lighting — raw natural daylight only.
  No background clutter — clean windowsill with only <Subject 3>.
  No face distortion, flickering identity, or outfit changes between cuts.
  No Chinese text or garbled characters on any surface.
  No smooth transitions — only raw jump cuts.
  No different plant appearing on screen vs windowsill — must be the same plant.
```

---

## Step 2B — Advanced subject definition patterns

### Before/After transformation states

When a video requires a visible transformation (makeup, grooming, cleaning, styling), define
BOTH states in the subject definition:

```
<Subject 1> "beauty model" — from #Image1: reproduce exact face, hair, skin, and body
  as shown in the reference image — identity locked throughout both states.
  ⚠️ Do NOT describe hair color, eye color, skin tone, or facial structure in text.
  BEFORE STATE (Shots 1–2): Skin condition appears dull, flat, tired — muted undertone,
    no glow. Hair hangs flat, unstyled, limp, no volume. (Describe CONDITION changes only,
    not the underlying features which come from the reference image.)
  AFTER STATE (Shots 3–4): Skin condition transforms to luminous, radiant, healthy with
    dewy glow. Hair is now styled — soft voluminous waves with body and movement.
```

### Composite reference images (multiple subjects in one image)

When a single uploaded image contains multiple subjects (e.g., before/after comparison,
product lineup, outfit moodboard), define each subject separately and specify its location
within the image:

```
<Subject 1> "dog — before state" — from #Image1 (left): [description with condition]
<Subject 2> "dog — after state" — from #Image1 (right): [description with improvement]
<Subject 3> "product" — from #Image1 (center): [product description]
```

### Virtual Try-On format

When the first image is a person and the second is an outfit/product to wear:

```
<Subject 1> "model" — from #Image1: reproduce exact face, hair, skin, and body as shown
  in the reference image — identity locked in every frame.
  ⚠️ Do NOT describe hair color, eye color, skin tone, facial structure, or body type
  in text. The reference image is the sole source of truth for identity. Only describe
  accessories and energy/vibe if needed.

<Subject 2> "outfit" — from #Image2: [every garment, accessory, shoe described exactly]
  Every piece must appear exactly as described from #Image2 — correct colors, correct
  logos, correct accessories, correct fit.
```

### Text overlays in shots

When text appears on screen, describe it within the shot's `detailed_description`:

```
At 00:01.000, the text "NEW COLLECTION" fades in at center frame in refined thin
sans-serif white typography — elegant, minimal, holding for approximately 2 seconds.
```

Always specify: exact text content, font style, color, position, animation, duration.

---

## Step 3 — Editing & continuation syntax

### Video editing (replace/remove/add)
```
Replace the newspaper in #Video1 with a green hardcover book.
Replace the wooden chair with a red velvet sofa.
Remove the sunglasses and reveal clear face with defined eyebrows.
Keep all other elements identical — same lighting, same camera movement, same timing.
```

**Rule:** Pair every replacement with a constraint about what to preserve.

### Video continuation
```
Continue #Video1 forward. The character who was walking toward camera continues past,
the camera holds position and watches them recede into the distance. Maintain the same
lighting conditions and color grade.
```

### Transition descriptions
Write transitions as **physical events**, not named effects:
- "fast binocular-scan transitions with whip movement, motion blur, optical smearing"
- "circular vinyl-record wipes"
- "vertical car-door cuts"
- NOT: "dissolve", "fade to black", "cross-fade"

---

## Step 4 — Performance & style direction

Use natural language for acting/style direction:
- "natural short-form drama, never theatrical"
- "cool attitude, elevated and restrained"
- "photoreal cinematic treatment, high-contrast lighting"
- "documentary intimacy, handheld warmth"

**Camera language vocabulary:**
- Lens: "wide angle with strong perspective distortion", "85mm portrait compression"
- Movement: "subtle handheld shake, then push in quickly and rack focus"
- Texture: "fine grain, soft highlight halation, restrained color"
- Exposure: "backlit exposure breathing", "crushed blacks, lifted shadows"

---

## Prompt quality checklist (before delivering)

| # | Check | Pass criteria |
|---|---|---|
| 1 | **All 7 sections present** | subject_definitions, summary, retention_analysis, detailed_description, overall_soundscape, non_diegetic_music, Exclusions |
| 2 | **Every reference uses #ImageN format** | `#Image1`, `#Image2`, not `<Picture 1>` |
| 3 | **Every #ImageN produces a Subject** | All uploaded images have at least one `<Subject N>` derived from them |
| 4 | **Multi-screen products fully described** | If a reference shows an app/website, every visible page/screen is listed with specific UI elements |
| 5 | **Screen content per shot specified** | Every shot where a screen is visible names the exact page and its elements |
| 6 | **Cross-context objects stated** | Objects appearing in two contexts (real + on-screen) have explicit match instructions |
| 7 | **Task type stated** | Summary uses valid task type vocabulary with `+` separator |
| 8 | **Retention markers set** | Every subject/reference has a preservation level assigned |
| 9 | **Shot timestamps** | Shot 1 has no timestamp; Shot 2+ have `At MM:SS.mmm` |
| 10 | **Dialogue tagged** | All spoken text in `<d>[Language] text</d>` format |
| 11 | **Speaker IDs stable** | `(S1)`, `(S2)` assigned once and reused consistently |
| 12 | **Word count** | Detailed description is 350–800 words depending on complexity |
| 13 | **Exclusions ≥ 5 lines** | At least 5 specific negative direction lines |
| 14 | **Reference count ≤ 15** | Total images + videos + audio ≤ 15 |
| 15 | **No conflicting instructions** | No opposing camera/movement/mood within same shot |
| 16 | **Transitions as physics** | No named effects like "dissolve" — describe the physical motion |
| 17 | **Language rule** | English throughout except inside `<d>` tags and visible scene text |
| 18 | **Character count ≤ 7000** | Total prompt must not exceed 7,000 characters |
| 19 | **Audio layering complete** | VO, music, and SFX described in separate sections (overall_soundscape + non_diegetic_music) |
| 20 | **VO handled correctly** | If voiceover exists: who/when/what/how/mix-level all specified; if no VO: explicitly stated |
| 21 | **Text overlays described** | Any on-screen text has exact content, font style, color, position, animation, duration |
| 22 | **Before/after states defined** | Transformation videos define BEFORE STATE and AFTER STATE in subject_definitions |
| 23 | **Composite refs decomposed** | Single images with multiple subjects define each subject with location qualifier |

---

## Output evaluation criteria (after generation)

Score each generated video 1–5 on these dimensions:

| Criteria | What to check | Score guide |
|---|---|---|
| **Motion accuracy** | Does the subject move as described? Right speed, direction, physics? | 5 = exact match, 1 = wrong motion |
| **Camera compliance** | Does the camera move as instructed? Right type, speed, direction? | 5 = exact match, 1 = wrong camera |
| **Identity preservation** | Does the subject look consistent with `<Subject>` definition throughout? | 5 = perfect lock, 1 = identity drifts |
| **Style fidelity** | Does lighting, color grade, mood match the style direction? | 5 = nailed it, 1 = wrong aesthetic |
| **Temporal coherence** | Flickering, morphing, unnatural frame transitions? | 5 = smooth, 1 = heavy artifacts |
| **Audio sync** | Soundscape matches visual events? Music timing correct? | 5 = synced, 1 = mismatched |
| **Dialogue accuracy** | Spoken text matches `<d>` tags? Lip sync correct? Speaker ID stable? | 5 = accurate, 1 = wrong/missing |
| **Screen content accuracy** | Does the phone show the correct app page at the correct shot? | 5 = right page at right time, 1 = wrong/blank |
| **Transition quality** | Transitions match physical descriptions? No default dissolves? | 5 = as described, 1 = generic |
| **Constraint compliance** | Are excluded elements absent? | 5 = clean, 1 = exclusions violated |
| **Retention accuracy** | Do `fully_preserved` refs actually stay fully preserved? | 5 = exact, 1 = preservation failed |
| **Cross-context match** | Objects in two contexts (real + screen) look the same? | 5 = identical, 1 = different |
| **Overall quality** | Would you use this in production? | 5 = production ready, 1 = unusable |

**Passing threshold:** Average ≥ 3.5 across all criteria. Any single score of 1 = prompt needs rework.

---

## Full example: UGC app demo prompt

```
subject_definitions:
  <Subject 1> "content creator" — from #Image1: reproduce exact face, hair, skin, and body
    as shown in the reference image — identity locked. Casual top, natural makeup, relaxed
    approachable energy. (Do NOT describe hair color, eye color, skin tone, or facial
    structure in text — the reference image defines these.)

  <Subject 2> "plant identifier app" — from #Image2: mobile app with green and white UI
    theme. Specific screens visible:
    - Home page: green header, plant category cards, search bar at top, bottom navigation
      bar with home/scan/my-plants/tips icons
    - Scanner page: full-screen camera viewfinder with green circular scanning frame overlay,
      "Identify" button at bottom center
    - Plant result page: large plant photo at top, plant name in bold below, scientific name
      in italic, health status indicator, green "Add to My Plants" button
    - Smart care page: watering schedule with droplet icons, sunlight meter bar, temperature
      range, humidity level, next-care-date reminder card
    - My Plants page: grid of saved plant thumbnails with names, green checkmarks on healthy
      plants
    - Care tips page: vertical card list with plant icons, tip titles, short descriptions,
      green accent dividers

  <Subject 3> "potted plant" — a medium-sized green leafy indoor plant in a terracotta or
    neutral ceramic pot, healthy with broad green leaves, sitting on a sunlit windowsill.
    This exact plant must appear physically in the room AND be the same plant shown on the
    phone screen when scanned.

summary: keyframe completion + reference generation. #Image1 anchors <Subject 1>'s full
  appearance in every frame. #Image2 provides visual reference for the app screens that
  appear on the phone — each screen must match the color scheme, layout structure, and UI
  elements visible in #Image2. The output is a 15-second vertical 9:16 TikTok-style UGC
  video of <Subject 1> casually demoing the plant identifier app by a window with a real
  plant.

retention_analysis:
  <Subject 1>: fully_preserved (face, hair, outfit, skin tone identical in all 5 shots)
  <Subject 2>: attribute_transfer (green/white color scheme, layout structure, icon style,
    bottom navigation bar from #Image2 maintained on phone screen throughout)
  <Subject 3>: fully_preserved (same plant visible on windowsill AND recognized on phone
    screen — same leaf shape, pot color, size)

detailed_description:
  [Shot 1] Selfie close-up, front camera perspective, vertical 9:16. <Subject 1> by a
  window with soft natural daylight from screen-left. <Subject 3> — a green leafy plant
  in a ceramic pot — sits on the windowsill beside her right shoulder, clearly visible
  in frame. She holds her phone low near chest level, the screen shows the app home page
  from #Image2 — green header, plant category cards, bottom navigation bar with icons.
  Screen is angled toward her, only partially visible to camera. She leans in toward camera
  with curious excited expression. Subtle handheld micro-shake, iPhone front-camera feel.
  <d>[English] I just tested this random app</d> (S1) — casual, curious tone, eyebrows
  slightly raised. She glances down at her phone, then back at camera with a building smile.

  [Shot 2] At 00:03.000, light jump cut — slight angle shift, still front camera. <Subject 1>
  raises the phone next to her face, screen partially visible to camera. The screen now shows
  the scanner page from #Image2 — full camera viewfinder with the green circular scanning
  frame centered on <Subject 3> on the windowsill. She points the phone toward the plant.
  The green scanning frame pulses around the plant. She taps the "Identify" button at the
  bottom of the screen with her thumb. The screen transitions to the plant result page from
  #Image2 — large photo of the same leafy plant at top, plant name in bold text below,
  scientific name in italic, green health status indicator showing healthy. Her eyebrows
  lift in genuine reaction.
  <d>[English] I tried it on like five different plants</d> (S1) — impressed, slightly
  faster pace, nodding once. She pulls the phone back toward chest, glancing between screen
  and camera.

  [Shot 3] At 00:06.500, light jump cut. Medium close-up, <Subject 1> holding phone near
  chest level. The screen now shows the smart care page from #Image2 — watering schedule
  with blue droplet icons, sunlight meter bar showing medium-high, temperature range,
  humidity percentage, next watering date card. The screen is in frame but secondary to her
  face. She gestures with her free hand, palm open, casual emphasis. She briefly scrolls
  the screen with her thumb — the care content moves upward revealing more plant care
  details below.
  <d>[English] and it got every single one right you just take a photo and it tells you
  what it is</d> (S1) — quick pace, genuinely impressed, small hand gestures.

  [Shot 4] At 00:10.000, light jump cut. Back to tighter selfie framing. <Subject 1>
  tilts the phone toward camera — the screen shows the care tips page from #Image2 — vertical
  card list with green plant icons, tip titles like watering frequency and sunlight needs,
  green accent dividers between cards. She holds the screen visible for about one and a half
  seconds. Tilts it back. Small nod, warm smile.
  <d>[English] It even shows you like when to water it and how much sun it needs</d> (S1) —
  impressed shifting to surprised, slower pace.

  [Shot 5] At 00:13.000, light jump cut. Tightest framing — face fills most of frame.
  <Subject 1> leans in close to camera, conspiratorial energy. <Subject 3> still visible
  over her shoulder on the windowsill — same plant, same pot, unchanged. She holds the phone
  at chest level, screen showing the my plants page from #Image2 — grid of saved plant
  thumbnails with green checkmarks.
  <d>[English] and its free I did not expect that</d> (S1) — surprised whisper, small laugh,
  slight head shake. Warm genuine smile, eyes bright, direct to camera. Subtle micro-nod.
  Hold on her face for the final beat.

overall_soundscape: Quiet indoor room tone with faint ambient hum. Soft finger tap on phone
  glass (at 00:04.000, one tap on Identify button). Gentle screen scroll sound (at 00:08.500).
  Subtle fabric rustle when she gestures. Faint window ambience. No background music, no
  other people. iPhone microphone quality — slightly compressed, intimate. Her breath audible
  between sentences.

non_diegetic_music: None. Pure raw UGC audio only.

Exclusions:
  No text overlays, no TikTok UI, no captions.
  No watermarks or logos.
  No full-screen app takeover — phone screen is always partial, glimpsed, part of her movement.
  No still camera — subtle handheld micro-shake throughout.
  No theatrical acting — natural, casual, unscripted energy.
  No studio lighting — raw natural daylight only.
  No background clutter — clean windowsill with only <Subject 3>.
  No face distortion, flickering identity, or outfit changes between cuts.
  No Chinese text or garbled characters on any surface.
  No smooth transitions — only raw jump cuts.
  No different plant appearing on screen vs windowsill — must be the same plant.
```

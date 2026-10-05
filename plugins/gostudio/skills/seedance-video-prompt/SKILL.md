---
name: seedance-video-prompt
description: >
  Write production-grade video generation prompts for ByteDance's Seedance 2.0 model.
  Use this skill whenever the user wants a prompt for AI video generation, video editing,
  video extension, or motion control using Seedance 2.0. Triggers include "video prompt",
  "Seedance prompt", "Seedance 2 prompt", "animate this image", "extend this video",
  "video from image", "add camera movement", "make this move". Also trigger when the user
  uploads an image or video and wants a Seedance-compatible prompt to generate or edit video.
  Grounded in ByteDance's official Seedance 2.0 documentation and community best practices.
---

# Seedance 2.0 Video Prompt Engineer

You write one prompt. It works first try. You do not write three variants and you do not
explain cinematography theory.

---

## Step 0 — Understand the input

Ask or infer from context:
1. **What is the source material?** (text only, image, video, audio, or combination)
2. **What is the desired output?** (generate new video, edit existing, extend, replicate camera)
3. **Duration?** (4–15 seconds; default 5s for simple, 10s for complex)
4. **Style?** (cinematic, documentary, commercial, artistic, etc.)

---

## Step 1 — Reference limits (hard caps)

| Input type | Tag syntax | Max count | Notes |
|---|---|---|---|
| **Images** | `@Image1` – `@Image9` | 9 | Each must declare its role |
| **Videos** | `@Video1` – `@Video3` | 3 | For camera/motion/edit reference |
| **Audio** | `@Audio1` – `@Audio3` | 3 | For BGM, voice, SFX |
| **Combined total** | — | **12** | Cannot exceed 12 files total |

**Critical rule:** Every `@` reference MUST declare what it provides. Never leave a reference
unassigned.

### Role declaration syntax

```
@Image1 as the character appearance reference
@Image2 as the environment/background
@Video1 for camera movement reference
@Audio1 as background music
```

Valid roles: `character appearance`, `first frame`, `last frame`, `environment/background`,
`style reference`, `camera movement reference`, `action choreography reference`,
`effects reference`, `rhythm/beat reference`, `voice tone reference`.

---

## Step 2 — The prompt formula (mandatory structure)

Every Seedance 2.0 prompt follows this 6-part formula. Target **60–100 words**.

```
[SUBJECT], [ACTION], in [ENVIRONMENT], camera [MOVEMENT], style [STYLE], avoid [CONSTRAINTS]
```

### Part-by-part rules

### 1. SUBJECT
- Describe the main subject with enough detail for identity but not excessive
- For people: age range, build, key clothing, distinguishing features
- For objects: material, color, size relative to scene
- For scenes: dominant elements, spatial arrangement

### 2. ACTION
- Describe **physical interactions**, not just poses
- Use progressive verbs: "walking toward", "lifting", "turning to face"
- Include body language: "shoulders relaxed", "leaning forward slightly"
- Mention speed: "slowly", "abruptly", "in a smooth continuous motion"

### 3. ENVIRONMENT
- Establish spatial context: indoor/outdoor, time of day, weather
- Include depth cues: foreground/midground/background elements
- Mention lighting source and quality (this has the HIGHEST impact)

### 4. CAMERA (one instruction only)
- **Use exactly ONE primary camera movement per prompt**
- Conflicting camera instructions = broken output

| Camera type | When to use | Example phrasing |
|---|---|---|
| **Push-in** | Build intensity, reveal detail | `camera slowly pushes in toward the subject's face` |
| **Pull-out** | Reveal environment, create scale | `camera pulls out to reveal the full cityscape` |
| **Pan** | Horizontal tracking, scanning | `camera pans left across the workshop` |
| **Tilt** | Vertical movement | `camera tilts up from feet to face` |
| **Tracking** | Follow moving subject | `camera tracks alongside the runner` |
| **Orbit** | 360° rotation around subject | `camera orbits around the sculpture` |
| **Aerial** | High-altitude establishing | `aerial camera descends toward the rooftop` |
| **Handheld** | Natural/documentary feel | `subtle handheld camera with natural shake` |
| **Fixed** | Static composition | `fixed camera, no movement` |
| **Crane** | Sweeping vertical + horizontal | `crane shot rising above the crowd` |
| **Whip pan** | Fast energy transition | `whip pan to the right revealing the second character` |
| **Hitchcock zoom** | Unease, vertigo | `Hitchcock zoom — dolly out while zooming in` |
| **First-person POV** | Immersive perspective | `first-person POV walking through the forest` |

### 5. STYLE
- Anchoring keywords: `cinematic`, `film grain`, `4K`, `warm tone`, `moody`, `documentary`
- Lighting (highest impact): `golden hour`, `rim light`, `natural light`, `neon`, `backlit`,
  `overcast`, `studio lighting`, `candlelight`
- Speed: `imperceptible`, `slow`, `smooth`, `dynamic`
- Texture: `shallow depth of field`, `lens flare`, `anamorphic`, `soft focus`

### 6. CONSTRAINTS (avoid list)
- State what to exclude: `avoid text overlays`, `avoid rapid cuts`, `avoid modern elements`
- Prevents the model from adding unwanted elements

---

## Step 3 — Time-segmented format (for videos > 5s)

For anything longer than 5 seconds, break into timed segments:

```
0–3s: [opening — establish scene, camera starts wide]
3–6s: [development — action begins, camera pushes in]
6–10s: [climax — key moment, peak of action]
10–15s: [resolution — settle, hold final frame]
```

### Shot-script format (for complex sequences)

```
【Style】Cinematic, golden hour, film grain
【Duration】10 seconds

[00:00–00:03] Establishing wide (fixed camera).
Autumn park at golden hour, leaves falling. A woman in a red coat stands on a stone bridge.
Warm ambient light, long shadows. Birds chirping, distant water.

[00:03–00:07] Medium close-up (slow push-in).
She turns to face camera, hair catching the wind. Expression shifts from contemplative to
a subtle smile. Leaves drift past her shoulder.

[00:07–00:10] Close-up (fixed camera).
Her eyes, warm light reflected. She exhales softly. Hold on this frame.
Sound of wind fading to silence.
```

---

## Step 4 — Audio direction

- Describe sounds as physical events: "footsteps on gravel", "wind through leaves"
- For music: genre + mood + instrument hints: "soft piano melody, contemplative"
- For dialogue: basic voice direction: "speaks softly in a low register"
- Beat-sync: "transitions match the beat drops at 3s and 7s"

---

## Step 5 — Common capability patterns

| Pattern | Prompt approach |
|---|---|
| **Image → video** | `@Image1 as first frame` + describe what happens next |
| **Video extension** | `@Video1 as the starting clip, continue the action forward` |
| **Camera replication** | `Replicate @Video1's camera movement` + new scene description |
| **Style transfer** | `@Image1 as style reference` + describe new content in that style |
| **Character consistency** | `@Image1 as the character, maintain exact appearance throughout` |
| **Product showcase** | `@Image1 as the product, 360° orbit, studio lighting, white background` |
| **Video editing** | `@Video1 as source, replace [X] with [Y], keep everything else identical` |

---

## Prompt quality checklist (before delivering)

Run every prompt through this checklist. All must pass:

| # | Check | Pass criteria |
|---|---|---|
| 1 | **Word count** | 60–100 words (simple) or segmented (complex) |
| 2 | **Single camera rule** | Exactly ONE primary camera instruction |
| 3 | **All references declared** | Every `@` tag has a role assignment |
| 4 | **No conflicting instructions** | No "static" + "orbit", no "slow" + "dynamic" in same segment |
| 5 | **Physical action described** | Actions use progressive verbs, not static descriptions |
| 6 | **Lighting specified** | At least one lighting keyword present |
| 7 | **Duration fits content** | Not cramming 10 actions into 4 seconds |
| 8 | **Constraints stated** | `avoid` section present with at least one exclusion |
| 9 | **No face generation** | Seedance 2.0 does NOT support realistic human face generation |
| 10 | **Reference count ≤ 12** | Total @Image + @Video + @Audio ≤ 12 |

---

## Output evaluation criteria (after generation)

Score each generated video 1–5 on these dimensions:

| Criteria | What to check | Score guide |
|---|---|---|
| **Motion accuracy** | Does the subject move as described? Right speed, direction, physics? | 5 = exact match, 1 = wrong motion |
| **Camera compliance** | Does the camera move as instructed? Right type, speed, direction? | 5 = exact match, 1 = wrong camera |
| **Identity preservation** | Does the subject look consistent with reference throughout? | 5 = perfect consistency, 1 = identity lost |
| **Style fidelity** | Does lighting, color grade, mood match the style keywords? | 5 = nailed the mood, 1 = wrong aesthetic |
| **Temporal coherence** | Are there flickering, morphing, or unnatural frame transitions? | 5 = smooth throughout, 1 = heavy artifacts |
| **Audio sync** | Does audio match the visual events and timing? | 5 = perfectly synced, 1 = mismatched |
| **Constraint compliance** | Are excluded elements actually absent? | 5 = clean, 1 = excluded items appear |
| **Overall quality** | Would you use this in production? | 5 = production ready, 1 = unusable |

**Passing threshold:** Average ≥ 3.5 across all criteria. Any single score of 1 = prompt needs rework.

---

## Example prompts

### Simple (text-to-video)
```
A golden retriever runs through shallow ocean waves at sunset, water splashing around its
paws, tail wagging. Camera tracks alongside the dog at eye level. Cinematic, golden hour
warm tones, shallow depth of field. Avoid text, avoid humans in frame.
```

### With image reference
```
@Image1 as first frame. The woman in the red dress slowly turns to face the camera, her
hair caught by a gentle breeze. She smiles subtly. Camera holds fixed at medium close-up.
Cinematic, soft natural light, shallow depth of field, film grain. Avoid rapid movement,
avoid background distractions.
```

### Complex multi-shot
```
@Image1 as character appearance. @Image2 as environment reference. @Audio1 as background music.

【Style】Cinematic, moody blue tones, shallow depth of field
【Duration】10 seconds

[00:00–00:03] Wide establishing (slow push-in).
Rain-soaked Tokyo alley at night, neon signs reflected in puddles. The character walks toward
camera in a dark coat, hands in pockets.

[00:03–00:07] Medium shot (tracking alongside).
Character continues walking, glancing at shop windows. Neon light plays across their face.
Rain drips from an awning.

[00:07–00:10] Close-up (fixed camera).
Character stops, looks directly into camera. Rain on their shoulders. Hold.
Ambient rain sounds, distant traffic, soft lo-fi beat from @Audio1.
```

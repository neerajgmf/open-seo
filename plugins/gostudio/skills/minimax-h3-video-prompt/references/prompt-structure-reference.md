# MiniMax H3 — Prompt Structure Quick Reference

## The 7-Section Template (copy-paste)

```
subject_definitions:
  <Subject 1> "[label]" — from #Image1: [enumerate ALL visual features exhaustively]
  <Subject 2> "[label]" — from #Image2: [for apps/products: list EVERY visible page/screen
    with specific UI elements, icons, buttons, colors, layout]
  <Subject 3> "[label]" — [physical objects: material, color, size, shape. If object appears
    in two contexts (real + on-screen), state this explicitly]

summary: [task type 1] + [task type 2]. #Image1 [role]. #Image2 [role].
  #Audio1 [role]. The output is a [duration]-second [format] [style] sequence of [what happens].

retention_analysis:
  <Subject 1>: [fully_preserved | partially_preserved | attribute_transfer | weak_reference]
    ([what specifically is preserved])
  <Subject 2>: [level] ([what is preserved])
  <Audio 1>: [fully_copy | partially_copy | reference | weak_reference]

detailed_description:
  [Shot 1] [Description — no timestamp. Specify which screen/page is showing if relevant]
  [Shot 2] At MM:SS.mmm, [description. Name exact page from subject definition + its elements]
  [Shot 3] At MM:SS.mmm, [description]

overall_soundscape: [Diegetic sounds with timestamps for interactions — taps, swipes, etc.]

non_diegetic_music: [Background music direction — or "None" for raw UGC]

Exclusions:
  [Minimum 5 specific lines]
  [Always include: identity, text/watermark, style boundaries]
  [For cross-context objects: "No different X appearing in context A vs context B"]
```

## Reference Format

**Always use `#ImageN`, `#VideoN`, `#AudioN`** — never `<Picture N>`.

```
#Image1  — first uploaded image
#Image2  — second uploaded image
#Video1  — first uploaded video
#Audio1  — first uploaded audio
```

## Subject Definition Rules

### People
```
<Subject 1> "label" — from #Image1: [hair length/color/style], [face features],
  [skin tone], [outfit — specific items, colors, materials], [accessories],
  [body type], [energy/vibe]
```

### Apps / Products with multiple screens
```
<Subject 2> "app name" — from #Image2: [overall UI theme]. Specific screens visible:
  - Page 1: [header, buttons, icons, layout, colors]
  - Page 2: [header, buttons, icons, layout, colors]
  - Page 3: [header, buttons, icons, layout, colors]
```

### Physical objects appearing in two contexts
```
<Subject 3> "object" — [material, color, size, shape, condition].
  This exact object must appear [context 1] AND [context 2].
```

## Screen Content Per Shot (critical for app demos)

Every shot where a screen is visible MUST specify:
1. **Which page** from the subject definition is showing
2. **Which specific elements** are visible (buttons, icons, text areas)
3. **What interaction** triggers the next page (tap, swipe, scroll)
4. **What the next page shows** after the transition

```
...the screen shows the scanner page from #Image2 — full camera viewfinder with the
green circular scanning frame centered on <Subject 3>. She taps the "Identify" button
at the bottom. The screen transitions to the plant result page from #Image2 — large
photo of the same leafy plant at top, plant name in bold text below...
```

## Task Type Vocabulary

| Type | Use when |
|---|---|
| `keyframe completion` | Image anchors a specific frame |
| `reference generation` | Image guides style/mood without anchoring |
| `video editing` | Modifying existing video |
| `video continuation` | Extending existing footage |
| `audio reuse` | Copying audio signal directly |
| `audio reference` | Mimicking style/timbre only |

Combine with ` + `: `keyframe completion + reference generation`

## Retention Markers

**Visual:** `fully_preserved` → `partially_preserved` → `attribute_transfer` → `weak_reference`
**Audio:** `fully_copy` → `partially_copy` → `reference` → `weak_reference`

## Camera Language (natural English, not keywords)

Instead of: `push-in`
Write: `the camera pushes in gently — a slow dolly movement covering about two meters over four seconds`

Instead of: `handheld`
Write: `subtle handheld micro-shake, iPhone front-camera feel`

Instead of: `jump cut`
Write: `light jump cut — slight angle shift, still front camera feel`

## Transition Language (physical events, not effects)

Instead of: `dissolve` → `the image softens and bleeds through overexposure`
Instead of: `cut` → `light jump cut — slight angle shift`
Instead of: `fade to black` → `exposure drops, shadows consuming frame from edges inward`

## Hard Limits

| Limit | Value |
|---|---|
| Max images | 9 |
| Max videos | 3 |
| Max audio | 3 |
| Max combined | 15 |
| Max prompt length | 7,000 characters |
| Detailed description target | 350–500 words |
| Shot 1 timestamp | None (no timestamp) |
| Shot 2+ timestamp | `At MM:SS.mmm` |
| Dialogue language | Original language inside `<d>` tags |
| Everything else | English |
| Minimum exclusions | 5 lines |

## Endpoint Decision Tree

```
User provides NO media files?
  → Text to Video endpoint

User provides 1-2 images only (as start/end frames)?
  → First & Last Frame endpoint

User provides any combination of images/videos/audio?
  → Reference to Video endpoint (default)
```

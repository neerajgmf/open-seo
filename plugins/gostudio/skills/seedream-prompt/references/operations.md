# Operation Skeletons

One skeleton per operation. Slots in `CAPS`. Fill every slot or drop it deliberately.
All skeletons follow the SPACE framework: Subject → Palette/Style → Arrangement → Camera/Light → Extra Detail.

---

## T2I — text to image, no references

**Skeleton:** `[Subject] + [Style/Medium] + [Lighting] + [Composition] + [Details]`

```
SUBJECT_DESCRIPTION, ACTION_OR_POSE, in LOCATION_DESCRIPTION.
STYLE_OR_MEDIUM, COLOUR_PALETTE_OR_GRADE.
LIGHTING_DESCRIPTION from LIGHT_DIRECTION.
COMPOSITION_AND_FRAMING, shot with LENS_TYPE.
EXTRA_CONSTRAINTS.
```

Official-density example:

> Close portrait of a woman beside a rain-covered window, loose dark hair, soft grey
> daylight, natural skin texture, quiet editorial photography.

Notes:
- Front-load the most important element — Seedream prioritizes what comes first.
- 30–100 words is the sweet spot. Under 15 produces generic results.
- Write natural-language sentences, not keyword stacks.
- State the intended use to set the generation mode: "editorial fashion portrait" vs "photo".

---

## REF_GEN — generation guided by reference images

**Skeleton:** `[Reference roles] + [Relationship instruction] + [New scenario]`

```
REFERENCE ROLES
Image 1 is ROLE_1. Image 2 is ROLE_2. Image 3 is ROLE_3.

TASK
Using Image X as ASPECT and Image Y as ASPECT, RELATIONSHIP_INSTRUCTION.

NEW SCENARIO
Place the result in SCENE_DESCRIPTION. LIGHTING. CAMERA.
```

Supported roles: face/identity, pose, art style, background environment, garment, product,
colour palette, layout.

Seedream 4.5 accepts up to **14 reference images**. Seedream 5.0 Pro accepts up to **10**.
Every image must have an explicit role label. Unlabelled references get averaged.

Seedream achieves subject-driven generation via multi-reference conditioning at inference
time — no fine-tuning or DreamBooth training step required. Pass subject photos as references
and the model maintains identity/style consistency.

---

## EDIT — conversational edit / inpaint

**Skeleton:** targeted change + explicit preservation.

```
DESCRIBE_THE_CHANGE.
Keep everything else unchanged — preserve FACE, HAIRSTYLE, POSE, CLOTHING, EXPRESSION,
BACKGROUND, LIGHTING, CAMERA_ANGLE, and COMPOSITION exactly as they are.
```

For additions:

```
Add NEW_ELEMENT to LOCATION_IN_SCENE.
Integrate it naturally with matching perspective, lighting, and shadows.
Leave everything else unchanged.
```

Rules:
- Every edit must end with a preservation clause naming what stays.
- Avoid vague instructions like "change it" — specify exactly what changes.
- For mask-based inpainting: white pixels = edit region, black pixels = preserve.
  Use a slightly conservative mask (2-3 pixels inside the edge) so the model respects
  surrounding texture.
- **Denoise strength 0.35–0.55** for precise changes on Seedream 4.5 (higher values
  invite fake textures).
- Multi-turn beats one giant edit. One change per turn.

---

## STYLE — style transfer

```
Apply the artistic style of STYLE_REFERENCE to the subject in IMAGE_1.
Preserve COMPOSITION_ELEMENTS: facial features, proportions, and pose.
Render with STYLISTIC_ELEMENTS and a palette of COLOUR_DESCRIPTION.
```

Name the concrete stylistic mechanics: "swirling impasto brushstrokes" carries more than
"Van Gogh style" alone. Use both.

For material transfer: "Apply Pattern A to the phone case in Photo B with realistic
reflections and curvature. Edit materials only, keep structure."

---

## COMPOSE — combine multiple images into one scene

```
Create a new image by combining elements from the provided images.
Take ELEMENT_FROM_IMAGE_1 and place it ON_OR_WITH ELEMENT_FROM_IMAGE_2.
The final image should be FINAL_SCENE_DESCRIPTION, with lighting and shadows adjusted
to match SCENE_LIGHTING.
```

The lighting-reconciliation clause prevents the output reading as a collage. Never drop it.

Label every input image by role: "Use the face from Image 1, the outfit from Image 2,
and the background from Image 3."

---

## PRESERVE — high-fidelity detail preservation

Use whenever a face, logo, product mark or typeface must survive an edit intact.

```
Using the provided images, place ELEMENT_FROM_IMAGE_2 onto ELEMENT_FROM_IMAGE_1.
DETAILED_DESCRIPTION_OF_WHAT_MUST_NOT_CHANGE — describe it feature by feature.
Ensure these features remain completely unchanged.
The added element should INTEGRATION_BEHAVIOUR.
```

Describe the thing you want preserved in heavy detail. Listing hair colour, eye colour
and expression makes the model hold them. Saying "keep the face the same" does not.

Seedream 4.5 achieves a 9.6/10 facial landmark consistency score across dynamic camera
shifts — but still restate invariants explicitly.

---

## TEXT — typography-led assets

Layer these rules onto whichever base skeleton applies.

```
TEXT CONTENT
Render the following text exactly:
- Top line: "EXACT_STRING" in FONT_DESCRIPTION_1
- Bottom line: "EXACT_STRING" in FONT_DESCRIPTION_2

LAYOUT
POSITION_AND_ALIGNMENT_SPEC, with consistent spacing.
```

Rules:
- Exact strings in double quotes, always.
- Font described: "heavy blocky Impact font", "thin minimalist sans-serif",
  "flowing elegant brush script".
- **Generate at 2K resolution minimum** for crisp typography.
- Keep text to **3–5 words per element** for highest accuracy (10 max).
- **Name the language explicitly** for non-English text.
- **Specify right-to-left** for Arabic and Hebrew.
- Route to **Seedream 5.0 Pro** for multilingual text (14 languages native).
- State placement: "centered at the top", "bottom-left corner".

Seedream 5.0 Pro text accuracy: ~89.5%. Headlines perform well. Dense small text is where
errors appear. Long text (10+ words) can garble across all versions.

---

## SKETCH — sketch to finished render (5.0 Pro only)

```
Convert this rough MEDIUM sketch of SUBJECT into a STYLE_DESCRIPTION image.
Preserve the SPECIFIC_FEATURES_FROM_SKETCH but add MATERIALS_AND_DETAILS.
Place it in SETTING. LIGHTING. CAMERA.
```

Seedream 5.0 Pro accepts rough sketches (doodles, color blocks, lines) as spatial guidance.
The model "reads the intent and renders the real object." Provide a plain-language note
describing what the sketch represents.

---

## SEQUENTIAL — batch generation (5.0 Lite only)

```
Generate a PANEL_COUNT image sequence in STYLE.
Image 1: BEAT_1. Image 2: BEAT_2. Image 3: BEAT_3.
Keep CHARACTER_DESCRIPTION consistent across all images.
```

**Seedream 5.0 Lite only** — supports up to 15 sequential outputs.
Seedream 5.0 Pro does NOT support sequential generation.
Use Edit Sequential mode to apply the same transformation across multiple images while
preserving identity.

---

## CONSISTENCY — same subject, new angle or scene

```
A SHOT_TYPE of this SUBJECT against BACKGROUND, ANGLE_OR_DIRECTION.
Keep the subject's IDENTIFYING_FEATURES identical to the reference.
```

Use reference images to lock identity across shots. Seedream 4.5's cross-image consistency
module computes feature maps across multiple inputs simultaneously, triangulating
identity-critical data points while allowing controlled variation in pose, lighting,
and background.

For batch consistency: maintain the same reference image set across all prompts in a series.

---

## OUTPAINT — extend image beyond original borders

```
Extend this image DIRECTION by AMOUNT. Generate content that naturally continues the
existing scene: match the LIGHTING, PERSPECTIVE, COLOUR_PALETTE, and STYLE of the
original. The transition should be seamless.
```

Provide the original image with a mask covering the extension area. The model generates
context-aware fill.

---

## REGION — precision region editing (5.0 Pro only)

```
REGION TARGET
Select the ELEMENT at LOCATION in the image.

CHANGE
Change it to NEW_DESCRIPTION.

PRESERVE
Keep everything else unchanged — face, hair, pose, background, lighting.
```

Seedream 5.0 Pro supports four targeting methods:
- **Point** — tap a spot to select the element
- **Bounding box** — draw a rectangle around the target
- **Arrow** — point at the element
- **Sketch** — draw a rough shape over the target area

---

## LAYER — layer separation (5.0 Pro only)

Three targeting modes:

1. **Omit prompt** = automatic full decomposition (model decides layers)
2. **Describe target elements** in natural language = selective extraction
3. **Bounding box coordinates** = `<bbox>x1 y1 x2 y2</bbox>` (normalized [0, 1000])

Output: base image + up to **16 transparent PNG layers**, each with z_index, bounding box,
name, and description. Use for downstream compositing, animation, or design handoff.

# Operation Skeletons

One skeleton per operation. Slots in `CAPS`. Fill every slot or drop it deliberately.
All skeletons follow OpenAI's official prompt structure: Background/Scene → Subject → Key Details → Constraints.

---

## T2I — text to image, no references

**Skeleton:** `[Scene/Background] + [Subject] + [Key Details] + [Constraints]`

```
Scene: LOCATION_DESCRIPTION, CONDITIONS_AND_ATMOSPHERE.
Subject: A SHOT_TYPE of SUBJECT_DESCRIPTION, ACTION_OR_POSE.
Details: LIGHTING_DESCRIPTION. Shot from CAMERA_ANGLE with LENS_TYPE. STYLE_AND_GRADE.
MATERIAL_AND_TEXTURE_DETAILS.
Constraints: EXCLUSIONS.
```

Official-density example from OpenAI cookbook:

> A close-up portrait of a woman in her 30s, natural skin texture with visible pores and
> subtle smile lines, shot with an 85mm f/1.4 lens, soft golden-hour window light from
> camera-left, shallow depth of field with gentle bokeh, wearing a cream linen shirt,
> warm color temperature.

Notes:
- Subject first is the strongest opening, but the order matters less than completeness.
- For complex multi-element scenes, use step-by-step construction: "First, create the
  background of X. Then, in the foreground, add Y. Finally, place Z on top of Y."
- State the intended use to set the generation "mode": "A hero banner for a tech startup"
  vs "a photo".

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
colour palette, layout, clothing reference.

GPT Image models accept up to **16 input images** per API call. Every image must have an
explicit role label. Unlabelled references get averaged.

---

## EDIT — conversational edit / semantic mask / inpaint

**Skeleton:** targeted change + explicit preservation.

```
Using the provided image, change only TARGET_ELEMENT to NEW_DESCRIPTION.
Keep everything else in the image exactly the same, preserving the original style,
lighting, composition, and all other objects.
```

For additions:

```
Using the provided image of SUBJECT, add NEW_ELEMENT to the scene.
INTEGRATION_INSTRUCTION so it matches the existing lighting, perspective and shadows.
Leave everything else unchanged.
```

Rules:
- The word **only** is load-bearing. Keep it.
- Name what stays, not just what changes. "Keep the pillows, the lighting, and the
  background unchanged" outperforms a generic preservation clause.
- Multi-turn beats one giant edit. Recommend iterating: one change per turn.
- Restate invariants on every iteration. The model has no persistent memory of your intent
  across API calls. Without restating, identity and style drift accumulate.
- For mask-based inpainting: transparent areas (alpha=0) in the mask indicate the edit zone.
  The mask must be a PNG with the same dimensions as the source image, under 4 MB.
  Important: the model treats the mask as **guidance**, not exact pixel boundaries.

---

## STYLE — style transfer

```
Transform the provided photograph of SUBJECT into the artistic style of STYLE_OR_ARTIST.
Preserve the original composition of COMPOSITION_ELEMENTS, but render all elements with
STYLISTIC_ELEMENTS and a palette of COLOUR_DESCRIPTION.
```

Name the concrete stylistic mechanics, not just the artist. "Swirling impasto brushstrokes"
carries more than "Van Gogh style" alone. Use both.

Specify what to preserve (facial structure, proportions, layout) and what to transform
(color palette, brush technique, rendering style) as separate lists.

---

## COMPOSE — combine multiple images into one scene

```
Create a new image by combining elements from the provided images.
Take ELEMENT_FROM_IMAGE_1 and place it ON_OR_WITH ELEMENT_FROM_IMAGE_2.
The final image should be FINAL_SCENE_DESCRIPTION, with lighting and shadows adjusted
to match SCENE_LIGHTING.
```

The lighting-reconciliation clause is what stops the output reading as a collage. Never drop it.

GPT Image 2 handles up to 16 input images. Label every input by role.

---

## PRESERVE — high-fidelity detail preservation

Use whenever a face, logo, product mark or typeface must survive an edit intact.

```
Using the provided images, place ELEMENT_FROM_IMAGE_2 onto ELEMENT_FROM_IMAGE_1.
DETAILED_DESCRIPTION_OF_WHAT_MUST_NOT_CHANGE — describe it feature by feature.
Ensure these features remain completely unchanged.
The added element should INTEGRATION_BEHAVIOUR.
```

Counter-intuitive but documented: **describe the thing you want preserved in heavy detail**.
Listing hair colour, eye colour and expression makes the model hold them. Saying "keep the
face the same" does not.

Add negative constraints for drift: "Do not stylize the face, do not cartoonize it, do not
apply anime effects."

---

## TEXT — typography-led assets

Layer these rules onto whichever base skeleton applies.

```
TEXT CONTENT
Render the following text exactly, verbatim:
- Top line: "EXACT_STRING" in FONT_DESCRIPTION_1
- Middle line: "EXACT_STRING" in FONT_DESCRIPTION_2
- Bottom line: "EXACT_STRING" in FONT_DESCRIPTION_3

LAYOUT
POSITION_AND_ALIGNMENT_SPEC, with consistent spacing.
No additional text, no extra characters, no duplicate text.
```

Rules:
- Exact strings in quotes, always. Add "render verbatim" to reinforce.
- Font described or named: "heavy blocky Impact font", "thin minimalist Century Gothic",
  "flowing elegant brush script", "bold geometric sans similar to Futura Bold".
- Run the two-step: settle the copy in conversation, then generate the image with it.
- Keep text short: under 10 words per text element for reliability.
- Route to **GPT Image 2** for commercial text. Text fidelity is its clearest advantage
  (~99% character-level accuracy across Latin, CJK, Hindi, Bengali).
- Use `quality: high` for text-heavy assets.

---

## SKETCH — sketch or wireframe to finished render

```
Convert this rough MEDIUM sketch of SUBJECT into a STYLE_DESCRIPTION image.
Preserve the exact SPECIFIC_FEATURES_FROM_SKETCH but add MATERIALS_AND_DETAILS.
Place it in SETTING. LIGHTING. CAMERA.
Do not add new elements or text not present in the sketch.
```

Say explicitly which sketch attributes are binding (layout, perspective, proportions) and
which are loose (exact line positions, surface detail). Use "do not add new elements" to
prevent creative reinterpretation.

---

## SEQUENTIAL — panels, storyboards, step sequences

```
Make a PANEL_COUNT panel SEQUENCE_TYPE in STYLE.
Panel 1: BEAT_1. Panel 2: BEAT_2. Panel 3: BEAT_3.
Keep CHARACTER_DESCRIPTION consistent across all panels.
LAYOUT_SPEC.
```

Use GPT Image 2 or 1.5. The model may not reliably honour an exact panel count, so state
it and expect to retry.

---

## CONSISTENCY — same subject, new angle or scene

```
A SHOT_TYPE of this SUBJECT against BACKGROUND, ANGLE_OR_DIRECTION.
Keep the subject's IDENTIFYING_FEATURES identical to the reference.
```

Method: iterate, and feed previously generated images back as additional references on each
turn. That is what holds the identity across a series. For a specific pose, supply a pose
reference image and label its role.

Use a **fixed character description** (name, distinctive features, clothing, build) and
include it verbatim in every prompt. Named characters ("Maya", "Pilot Girl") help the model
lock onto a consistent visual identity.

Include distinctive, unusual visual markers (specific scar, unique hat, tattoo) that act as
anchors the model can latch onto consistently.

---

## OUTPAINT — extend image beyond original borders

```
Extend this image DIRECTION by AMOUNT. Generate content that naturally continues the
existing scene: match the LIGHTING, PERSPECTIVE, COLOUR_PALETTE, and STYLE of the
original. The transition between original and extended areas should be seamless.
```

Uses the edit endpoint. Provide the image with transparent borders indicating where to
extend, or use a mask. The model fills in the extended area.

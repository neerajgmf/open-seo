# Operation Skeletons

One skeleton per operation. Slots in `CAPS`. Fill every slot or drop it deliberately.
All skeletons are taken from or derived directly from Google's official templates.

---

## T2I — text to image, no references

**Skeleton:** `[Subject] + [Action] + [Location/context] + [Composition] + [Style]`

```
A SHOT_TYPE of SUBJECT_DESCRIPTION, ACTION_OR_POSE, in LOCATION_DESCRIPTION.
LIGHTING_DESCRIPTION. Shot from CAMERA_ANGLE with LENS_TYPE. STYLE_AND_GRADE.
```

Official example worth matching in density:

> A striking fashion model wearing a tailored brown dress, sleek boots, and holding a structured
> handbag. Posing with a confident, statuesque stance, slightly turned. A seamless, deep cherry red
> studio backdrop. Medium-full shot, center-framed. Fashion magazine style editorial, shot on
> medium-format analog film, pronounced grain, high saturation, cinematic lighting effect.

Notes:
- Order matters less than presence. Subject first is still the strongest opening.
- For complex multi-element scenes, use step-by-step construction instead: "First, create the
  background of X. Then, in the foreground, add Y. Finally, place Z on top of Y." Official technique.

---

## REF_GEN — generation guided by reference images

**Skeleton:** `[Reference roles] + [Relationship instruction] + [New scenario]`

```
REFERENCE ROLES
Image 1 is ROLE_1. Image 2 is ROLE_2. Image 3 is ROLE_3.

TASK
Using IMAGE_X as ASPECT and IMAGE_Y as ASPECT, RELATIONSHIP_INSTRUCTION.

NEW SCENARIO
Place the result in SCENE_DESCRIPTION. LIGHTING. CAMERA.
```

Roles that actually work: face/identity, pose, art style, background environment, garment, product,
colour palette, layout.

Style references are Pro-only, up to 3. If the user supplies a style ref, route to
`gemini-3-pro-image` and say so.

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
- Name what stays, not just what changes. "Keep the pillows and the lighting unchanged" outperforms a
  generic preservation clause.
- Multi-turn beats one giant edit. Recommend iterating: one change per turn, conversationally.

---

## STYLE — style transfer

```
Transform the provided photograph of SUBJECT into the artistic style of STYLE_OR_ARTIST.
Preserve the original composition of COMPOSITION_ELEMENTS, but render all elements with
STYLISTIC_ELEMENTS and a palette of COLOUR_DESCRIPTION.
```

Name the concrete stylistic mechanics, not just the artist. "Swirling impasto brushstrokes" carries
more than "Van Gogh style" alone. Use both.

---

## COMPOSE — combine multiple images into one scene

```
Create a new image by combining elements from the provided images.
Take ELEMENT_FROM_IMAGE_1 and place it ON_OR_WITH ELEMENT_FROM_IMAGE_2.
The final image should be FINAL_SCENE_DESCRIPTION, with lighting and shadows adjusted
to match SCENE_LIGHTING.
```

The lighting-reconciliation clause is what stops the output reading as a collage. Never drop it.

---

## PRESERVE — high-fidelity detail preservation

Use whenever a face, logo, product mark or typeface must survive an edit intact.

```
Using the provided images, place ELEMENT_FROM_IMAGE_2 onto ELEMENT_FROM_IMAGE_1.
DETAILED_DESCRIPTION_OF_WHAT_MUST_NOT_CHANGE — describe it feature by feature.
Ensure these features remain completely unchanged.
The added element should INTEGRATION_BEHAVIOUR.
```

Counter-intuitive but official: **describe the thing you want preserved in heavy detail**. Listing hair
colour, eye colour and expression makes the model hold them. Saying "keep the face the same" does not.

---

## GROUNDED — real-time or factual data

**Skeleton:** `[Search request] + [Analytical task] + [Visual translation]`

```
SEARCH_INSTRUCTION (e.g. "Search for the current weather and date in Bengaluru").
Use this data to ANALYTICAL_TASK.
Visualise this as VISUAL_TREATMENT, with TEXT_AND_LAYOUT_SPEC.
```

Requires `tools: [{"type": "google_search"}]` in the API call. Not available on Lite.
NB2 additionally supports `search_types: ["web_search", "image_search"]`, which pulls reference imagery.
NB2 image-search grounding will not return real-world images of people.

If you use image search grounding in a product, you must display the returned `search_suggestions`.
That is a terms-of-service requirement, not a style choice.

---

## TEXT — typography-led assets

Layer these rules onto whichever base skeleton applies.

```
TEXT CONTENT
Render the following text exactly:
- Top line: "EXACT_STRING" in FONT_DESCRIPTION_1
- Middle line: "EXACT_STRING" in FONT_DESCRIPTION_2
- Bottom line: "EXACT_STRING" in FONT_DESCRIPTION_3

LAYOUT
POSITION_AND_ALIGNMENT_SPEC, with consistent spacing.
```

Rules:
- Exact strings in quotes, always.
- Font described or named: "heavy blocky Impact font", "thin minimalist Century Gothic", "flowing
  elegant brush script".
- Run the two-step: settle the copy in conversation, then generate the image with it.
- For localisation, generate in one language then ask for translation of the text only, everything
  else unchanged.
- Route to Pro for anything commercial. Text fidelity is its clearest advantage.

---

## SKETCH — sketch or wireframe to finished render

```
Turn this rough MEDIUM sketch of SUBJECT into a STYLE_DESCRIPTION image.
Keep SPECIFIC_FEATURES_FROM_SKETCH but add MATERIALS_AND_DETAILS.
Place it in SETTING. LIGHTING. CAMERA.
```

Say explicitly which sketch attributes are binding and which are loose. Google's own logo example uses
"don't exactly follow the sketch, get inspired from it" when the sketch is directional only.

---

## SEQUENTIAL — panels, storyboards, step sequences

```
Make a PANEL_COUNT panel SEQUENCE_TYPE in STYLE.
Panel 1: BEAT_1. Panel 2: BEAT_2. Panel 3: BEAT_3.
Keep CHARACTER_DESCRIPTION consistent across all panels.
LAYOUT_SPEC.
```

Needs NB2 or Pro. Lite cannot hold consistency. The model will not reliably honour an exact panel
count, so state it and expect to retry.

---

## CONSISTENCY — same subject, new angle or scene

```
A SHOT_TYPE of this SUBJECT against BACKGROUND, ANGLE_OR_DIRECTION.
Keep the subject's IDENTIFYING_FEATURES identical to the reference.
```

Method: iterate, and feed previously generated images back in as additional references on each turn.
That is what holds the identity across a 360 set. For a specific pose, supply a pose reference image
and label its role.

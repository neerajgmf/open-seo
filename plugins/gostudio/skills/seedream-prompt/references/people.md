# People and Identity

Load this whenever a real human likeness is involved. Face work fails in specific, repeatable
ways. These lines are the fixes.

---

## Model ceilings, state them honestly

| | Seedream 5.0 Pro | Seedream 4.5 | Seedream 5.0 Lite |
|---|---|---|---|
| Max reference images | 10 | 14 | 14 |
| Facial landmark consistency | Good | 9.6/10 | Good |
| Skin realism | Over-smoothed | Best (natural texture) | Moderate |
| Text rendering (in-image) | 14 languages native | EN + ZH | EN + ZH |
| Layer separation | Yes (up to 16 layers) | No | No |
| Region editing | Precision (point/bbox/sketch) | Basic | No |

**Portrait skin realism**: Seedream 4.5 still wins on skin texture. Seedream 5.0 Pro
over-smooths skin — a documented regression. For maximum portrait realism, route to 4.5.

Identity preservation is strong but not guaranteed. Budget 2–3 generations per delivered
portrait. Seedream 4.5's cross-image consistency module achieves 9.6/10 facial landmark
consistency across dynamic camera shifts.

---

## The five failure modes and their fixes

**1. Over-smoothed skin (5.0 Pro).** Skin loses natural texture and reads as airbrushed.
Fix: explicit imperfection cues. "Natural skin texture, visible pores, fine expression lines,
natural asymmetry, no beauty filters." This "imperfection engineering" approach does more for
realism than any "8K masterpiece" quality keyword.

**2. Pose drift during edits.** Changing clothing or accessories shifts the subject's pose.
Fix: name the exact pose in the preservation clause. "Keep the subject's exact pose — weight
on left foot, right hand at hip, shoulders angled 30 degrees to camera."

**3. Default body.** Given only a face reference, the model builds a generic body.
Fix: an explicit build slot per person. Use visual descriptors, not numeric measurements.

**4. Group averaging.** In multi-person shots, features can blend between subjects.
Fix: name each person, pin each to a frame position, label each reference image by role.
"Image 1 is Person A (left of frame). Image 2 is Person B (right of frame). Keep their
features entirely separate."

**5. Action overshoot.** Dynamic scenes on 5.0 Pro can overshoot the intended action.
Fix: tone down action descriptors. "Gently reaching forward" not "lunging."

---

## Numeric measurements do not transfer

Kilograms, centimetres and clothing sizes mean nothing to the model. Map to descriptors
before injection.

Build: `slim` · `lean` · `average` · `athletic` · `solid` · `broad` · `heavyset`
Height: `short` · `average height` · `tall`

---

## Reusable skeleton: face reference to full-length portrait

```
REFERENCE ROLES
Use the attached photographs as identity references only.
Image 1 is PERSON_1. Image 2 is PERSON_2.

TASK
Generate one photorealistic full-length portrait photograph of these people together.

IDENTITY PRESERVATION
Each person's face must remain exactly as it appears in their reference photograph:
identical facial structure, eye shape and colour, nose, mouth, jawline, hairline, hair
colour and length, facial hair, skin tone and skin texture, and any visible glasses, moles
or scars. Do not slim, lighten, smooth, age, or beautify any face. Keep their features
entirely separate and do not merge characteristics between them.

BODY CONSTRUCTION
Build each body below the neck as a natural anatomical continuation of that person's visible
head, neck and shoulder proportions. PERSON_1 has a BUILD_1 build and HEIGHT_1 height.
Give the group naturally varied heights and builds.

WARDROBE
PERSON_1 wears WARDROBE_1. All garments are well-fitted and correctly tailored to each
person's build, with natural fabric drape and realistic creasing.

SETTING
SETTING_DESCRIPTION, with a clean background.

LIGHTING
LIGHTING_DESCRIPTION, falling evenly across every face, with soft shadows on the ground
beneath each person's feet consistent with a single light direction.

CAMERA
Shot with a 50mm lens at f/4, eye-level, straight-on. Sharp focus across all subjects.
Natural skin texture, visible pores, fine expression lines.

FRAMING
Full-length: every subject visible from head to shoes, clear headroom, visible floor.
```

Settings: `seedream-4-5` for best skin realism · `2K` · `3:2` for groups, `2:3` for solo.
For 4.5, add `guidance_scale: 7.0 · steps: 28`.

---

## Input texture matching

The face-to-full-portrait prompt must respect the medium of the input image. Without an explicit
match clause, Seedream models default to full-colour photorealism regardless of what was uploaded.

**Detection rules (applied by the orchestrating agent or backend before prompt assembly):**

| Input medium | Rendering instruction added to prompt |
|---|---|
| Colour photograph | `Render as a full-colour photorealistic photograph.` |
| Black-and-white / greyscale photograph | `Render as a black-and-white photograph matching the input's greyscale tonal range, contrast, and grain. Do not add colour.` |
| Sepia-toned photograph | `Render in sepia tone matching the input's warmth and tonal range. Do not convert to full colour.` |
| Pencil sketch / graphite drawing | `Render as a pencil sketch on white paper, matching the input's line weight, shading style, and graphite texture. Do not add colour or photorealistic rendering.` |
| Ink drawing / line art | `Render as ink line art matching the input's stroke weight, contrast, and hatching style. Do not add colour or photorealistic rendering.` |
| Charcoal drawing | `Render as a charcoal drawing matching the input's smudge texture, tonal depth, and paper grain. Do not add colour.` |
| Watercolour painting | `Render as a watercolour painting matching the input's wash transparency, colour palette, and paper texture.` |
| Digital illustration / cartoon | `Render as a digital illustration matching the input's art style, line work, colour palette, and shading technique.` |

If the medium is ambiguous, default to matching the input exactly and state: "Match the exact
visual medium, texture, colour palette, and rendering style of the input image."

---

## Ready-to-use: face to full portrait (condensed)

Drop-in prompt for solo and group inputs. Seedream-specific: identity is front-loaded (Seedream
prioritizes first content), pose is pinned to prevent drift (failure mode #2), action language
is removed to prevent overshoot (failure mode #5), and a named preservation clause closes the prompt.

```
The attached image is the identity reference. Preserve each person's exact
facial features, skin tone, hair, and any glasses/moles/scars — do not
beautify, slim, or lighten any face. Detect the visual medium of the input —
photograph, black-and-white photo, pencil sketch, ink drawing, charcoal,
watercolour, digital illustration, or other. The output must match the exact
same medium, texture, colour palette, and rendering style. Do not convert a
sketch to a photograph or a black-and-white image to colour.

Generate a full-length portrait of every person visible in their left-to-right
order. If one person, show them centred. Keep each person's features entirely
separate. Build each body as a natural continuation of their visible proportions
with varied heights and builds. Match the exact body posture, shoulder angle,
head tilt, arm position, and weight distribution visible in the input — extend
that pose naturally through the full body. If the environment or background is
visible in the input, extend it consistently; if not, place the person in a
natural setting that matches the input's lighting and mood. Extend visible
clothing naturally; if only a face is visible, dress in smart-casual neutrals
matching the input's medium. Match the input's lighting direction, quality, and
colour temperature. 50mm at f/4, full-length framing with headroom and visible
floor. Natural skin texture, visible pores, fine expression lines, no beauty
filters. Keep unchanged: face, expression, skin tone, hair, identifying marks,
body posture. No watermark, no text, no extra people, no duplicate body parts.
```

Settings: `seedream-4-5` · `2K` · `2:3` solo, `3:2` group.
For 4.5, add `guidance_scale: 5.5 · steps: 28` (lower guidance for portraits).

Note: Seedream 5.0 Pro over-smooths skin — route to 4.5 for best portrait realism.
5.0 Pro may also block real human face references due to deepfake moderation filters.

---

## Headshot and half-length

```
A photorealistic SHOT_TYPE of SUBJECT_DESCRIPTION with EXPRESSION, looking DIRECTION.
Wearing GARMENT in FABRIC and COLOUR, FIT_DESCRIPTION.
Background: BACKGROUND_DESCRIPTION.
LIGHTING_DESCRIPTION sculpting the jawline.
Shot with an 85mm portrait lens, shallow depth of field.
Natural skin texture, visible pores, fine expression lines. The overall mood is MOOD.
```

The "natural skin texture, visible pores" line is the cheapest defence against plastic skin,
especially on Seedream 5.0 Pro.

---

## Imperfection engineering (realism technique)

Instead of stacking quality keywords ("8K masterpiece ultra-detailed"), add positive
imperfection cues for photorealism:

```
visible skin pores, natural asymmetry, no makeup look, sensor noise, handheld softness,
no beauty filters
```

Realism comes from one coherent camera contract per image, not from quality modifiers.

---

## Virtual try-on (with reference images)

```
Place the garment from Image 2 onto the person in Image 1. Maintain the person's exact
pose, facial features, and body proportions. Adjust the garment's draping naturally to
match the body position. Keep the original background, lighting, and color temperature.
No other changes.
```

Label each input image by role. This is a PRESERVE operation with clothing as the variable.

---

## Wardrobe vocabulary

Choose these silently. Do not explain them in the prompt.

- Always state fit: `tailored`, `well-fitted`, `relaxed cut`, `oversized`.
- Fabrics signal quality: wool, cashmere, cotton poplin, silk, linen, tweed, denim.
- Authority palette: navy, charcoal, black, cream, white, burgundy, forest green.
- Name the specific garment: "open-collar cotton poplin shirt", not "a shirt".

---

## Ethical line

Do not write prompts that place a real, identifiable person into a scenario they did not
consent to, that misrepresent them, or that sexualise them. Likeness work is for people who
supplied their own photograph.

Note: Seedream 5.0 Pro has stricter content moderation than 4.5 and may block real photographs
of human faces as reference images (deepfake liability). AI-generated portraits, illustrations,
and stylized faces typically pass the filter.

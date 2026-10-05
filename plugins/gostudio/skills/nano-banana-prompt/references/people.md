# People and Identity

Load this whenever a real human likeness is involved. Face work fails in specific, repeatable ways.
These lines are the fixes. They are worth more than any wardrobe detail.

---

## Model ceilings, state them honestly

| | NB2 | NB Pro | Lite |
|---|---|---|---|
| Characters held with resemblance | 4 | 5 | none |
| Objects held with fidelity | 10 | 6 | 14 |
| Style references | none | 3 | none |

Beyond the character ceiling, resemblance degrades regardless of prompt quality. Say this rather than
writing a prompt that cannot work.

Google also documents that character consistency across edits varies even inside the limits. Budget
retries. For a paid product, 3 to 4 generations per delivered image is a realistic assumption on
full-length work.

---

## The five failure modes and their fixes

**1. Identity drift.** The face comes back prettier, slimmer, younger, lighter.
Fix: an explicit anti-beautification clause. "Do not slim, lighten, smooth, age, or beautify any face."

**2. Group bleed.** In a multi-person shot, faces converge toward an average.
Fix: name each person, pin each to a frame position, and add "keep their features entirely separate
and do not merge characteristics between them."

**3. Default body.** Given only a face, the model builds a tall, slim body.
Fix: an explicit build slot per person. Non-negotiable for anything below the shoulders.

**4. Uniform stature.** Groups render as people of identical height.
Fix: "Give the group naturally varied heights and builds rather than uniform proportions."

**5. Collage effect.** A group reads as separate cutouts pasted together.
Fix: one stated light direction plus ground shadows beneath every person's feet.

---

## Numeric measurements do not transfer

Kilograms, centimetres and clothing sizes mean nothing to the model. Map to descriptors before
injection. This mapping belongs in the backend, not in the prompt.

Build: `slim` · `lean` · `average` · `athletic` · `solid` · `broad` · `heavyset`
Height: `short` · `average height` · `tall`
Weight change: 1–12 kg maps to `moderate`, 13–30 kg maps to `significant`

When a body changes shape, the single most important instruction is re-tailoring: garments must be
refitted to the new build, not stretched over it. Without that line the clothes stay the old size and
the whole image reads as fake.

---

## Reusable skeleton: face reference to full-length portrait

Works for one person or a group. The per-person lines repeat; everything else is fixed. For solo,
collapse to a single instance and swap the composition line.

```
REFERENCE ROLES
Use the attached photographs as identity references only.
Image 1 is PERSON_1. Image 2 is PERSON_2. Image 3 is PERSON_3.

TASK
Generate one photorealistic full-length portrait photograph of these people together,
standing as a group.
[solo: of this person, standing alone.]

IDENTITY PRESERVATION
Each person's face must remain exactly as it appears in their reference photograph:
identical facial structure, eye shape and colour, nose, mouth, jawline, hairline, hair
colour and length, facial hair, skin tone and skin texture, and any visible glasses, moles
or scars. Do not slim, lighten, smooth, age, or beautify any face. Each reference is a
distinct individual. Keep their features entirely separate and do not merge characteristics
between them.

BODY CONSTRUCTION
Build each body below the neck as a natural anatomical continuation of that person's visible
head, neck and shoulder proportions. PERSON_1 has a BUILD_1 build and HEIGHT_1 height.
PERSON_2 has a BUILD_2 build and HEIGHT_2 height. Give the group naturally varied heights
and builds rather than uniform proportions. Hands have five fingers each, in relaxed,
natural positions.

WARDROBE
PERSON_1 wears WARDROBE_1. PERSON_2 wears WARDROBE_2. All garments are well-fitted and
correctly tailored to each person's build, with natural fabric drape, visible weave texture,
and realistic creasing at the elbows, waist and knees.

COMPOSITION AND POSE
PERSON_1 stands at the left of the frame, PERSON_2 at the centre, PERSON_3 at the right.
[solo: The subject stands centred in the frame.]
Relaxed, confident standing poses with weight naturally distributed, shoulders squared
toward the camera, feet planted on the ground. Each person occupies their own space with a
small, natural gap between shoulders.

SETTING
SETTING_DESCRIPTION, with a clean and uncluttered background.

LIGHTING
LIGHTING_DESCRIPTION, falling evenly across every face so all subjects are equally well lit,
with soft shadows on the ground beneath each person's feet consistent with a single light
direction.

CAMERA
Shot on a full-frame camera with a 50mm lens at f/4, eye-level, straight-on. Sharp focus
across all subjects, gently softened background. Natural colour science, realistic skin
tones, fine visible skin detail and pores.

FRAMING
Full-length framing: every subject is visible in full from the top of the head to the shoes,
with clear headroom above the heads and visible floor below the feet. Nothing is cropped at
any edge.
```

Settings: `gemini-3-pro-image` · `2K` · `4:5` solo, `3:2` for two or three people, `16:9` for four or five.

Known weak point: full-length body inference from a face is the least reliable operation in the whole
pipeline. Expect hand and foot issues on roughly one generation in four, and expect resemblance to
soften at full-length distance because the face occupies fewer pixels. Generating at 4K helps and costs
more.

---

## Input texture matching

The face-to-full-portrait prompt must respect the medium of the input image. Without an explicit
match clause, models default to full-colour photorealism regardless of what was uploaded.

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

Drop-in prompt that handles solo and group inputs automatically. Covers all five failure modes
and input-texture matching in minimal token count. Use this when the backend needs a single prompt
for the face-to-full-portrait use case without per-person slot filling.

```
Use the attached image as identity reference. Detect the visual medium of the
input — photograph, black-and-white photo, pencil sketch, ink drawing, charcoal,
watercolour, digital illustration, or other. The output must match the exact
same medium, texture, colour palette, and rendering style as the input. Do not
convert a sketch to a photograph or a black-and-white image to colour.

Generate a full-length portrait of every person visible, maintaining their
left-to-right order. If only one person is detected, show them standing alone
centred in frame. Preserve each person's exact facial features, skin tone, hair,
and any glasses/moles/scars — do not beautify, slim, or lighten any face. Keep
each person's features entirely separate. Build each body as a natural
continuation of their visible proportions with varied heights and builds. Extend
visible clothing naturally; if only a face is visible, dress in smart-casual
neutrals matching the input's medium. Relaxed standing poses, feet on the ground.
Soft directional light from upper left, ground shadows beneath every person's
feet. 50mm lens at f/4 perspective, full-length framing with headroom and visible
floor. No watermark, no text, no extra people, no duplicate body parts.
```

Settings: `gemini-3-pro-image` · `2K` · `4:5` solo, `3:2` group.

---

## Headshot and half-length

Shorter, higher hit rate. Build slot matters less; jawline and shoulder line matter more.

```
A photorealistic SHOT_TYPE of SUBJECT_DESCRIPTION with EXPRESSION, looking DIRECTION.
Wearing GARMENT in FABRIC and COLOUR, FIT_DESCRIPTION.
Background: BACKGROUND_DESCRIPTION.
LIGHTING_DESCRIPTION sculpting the jawline.
Captured with an 85mm portrait lens, FRAMING, shallow depth of field.
Skin retains natural texture and pores. The overall mood is MOOD.
```

The "natural texture and pores" line is the cheapest defence against plastic skin.

---

## Wardrobe vocabulary

Choose these silently. Do not explain them in the prompt.

- Always state fit: `tailored`, `well-fitted`, `relaxed cut`, `oversized`. Never just "a suit".
- Fabrics signal quality: wool, cashmere, cotton poplin, silk, linen, tweed, denim. Never mention
  polyester or "fabric".
- Authority palette: navy, charcoal, black, cream, white, burgundy, forest green.
- Fewer accessories reads more expensive. One considered piece beats three.
- Name the specific garment: "open-collar cotton poplin shirt", not "a shirt".

---

## Ethical line

Do not write prompts that place a real, identifiable person into a scenario they did not consent to,
that misrepresent them, or that sexualise them. Likeness work is for people who supplied their own
photograph. If the reference is a public figure and the request is not clearly satire, editorial or
consented, decline and say why.

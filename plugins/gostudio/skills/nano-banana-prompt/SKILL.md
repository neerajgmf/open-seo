---
name: nano-banana-prompt
description: >
  Write production-grade image generation and editing prompts for Google's Nano Banana models
  (Nano Banana 2 / Gemini 3.1 Flash Image, Nano Banana Pro / Gemini 3 Pro Image, Nano Banana 2 Lite).
  Use this skill whenever the user wants a prompt for AI image generation or editing on Nano Banana,
  NB2, NB Pro, Gemini image, or Google image models. Triggers include "image prompt", "photo prompt",
  "headshot prompt", "portrait prompt", "product shot prompt", "poster prompt", "infographic prompt",
  "logo prompt", "mockup prompt", "thumbnail prompt", "edit this image", "change the background",
  "put this person in", "style transfer", "combine these images", "face to full body", "group photo",
  "nano banana prompt", "NB2 prompt", "NB Pro prompt", "Gemini image prompt". Also trigger when the
  user uploads a reference image and wants a prompt that reproduces, edits, or extends it. Supersedes
  the older nano-banana-stylist skill.
---

# Nano Banana Prompt Engineer

You write one prompt. It works first try more often than not. You do not write three variants
and you do not explain photographic theory.

Grounded in Google's official guidance: the Gemini API image-generation docs, the Google Cloud
"Ultimate Nano Banana prompting guide" (Mar 2026), and the DeepMind Nano Banana Pro tips post.

---

## Step 0 — Route the model

Model choice is an **output** of the brief, not an input. Derive it, then state it.

| Model | API ID | Reference budget | Use when |
|---|---|---|---|
| **Nano Banana 2** | `gemini-3.1-flash-image` | 10 objects, 4 characters | Default. Best cost/quality. Only model with 512px, 1:4/4:1/1:8/8:1 ratios, video-to-image, image-search grounding, `thinking_level` control |
| **Nano Banana Pro** | `gemini-3-pro-image` | 6 objects, 5 characters, **3 style refs** | Style references needed. 5 faces. Brand consistency. Complex typography. Localisation. Highest-stakes asset |
| **NB2 Lite** | `gemini-3.1-flash-lite-image` | 14 objects, **no character consistency** | High volume, 1K only, no grounding. Never for faces |
| Nano Banana (legacy) | `gemini-2.5-flash-image` | 3 images | Do not recommend. Google says migrate off it |

Routing rules that decide it outright:
- Style reference image supplied → **Pro** (only model that accepts style refs)
- 5 people needing likeness → **Pro**. More than 5 → tell the user resemblance will degrade, this is a model ceiling
- 7 or more distinct objects to preserve → **NB2**
- Banner at 8:1 or 4:1 → **NB2** only
- Real-time facts or live data in the image → **NB2 or Pro** (Lite has no grounding)
- Everything else → **NB2**

**Resolution and aspect ratio.** Both take uppercase K: `1K`, `2K`, `4K` (NB2 also `512px`). Lowercase
is rejected by the API. Supported ratios on both: 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9.
NB2 adds 1:4, 4:1, 1:8, 8:1.

---

## Step 1 — Classify the operation

The operation determines the **skeleton**. Read the matching section of
`references/operations.md` before writing anything.

| Signal in the request | Operation |
|---|---|
| Nothing uploaded, describing a scene | `T2I` |
| Uploaded photos, wants a new scene with those subjects | `REF_GEN` |
| Uploaded photo, change one thing, keep the rest | `EDIT` |
| Uploaded photo, same content in a different art style | `STYLE` |
| Two or more uploads to merge into one scene | `COMPOSE` |
| Something specific must survive the edit untouched (face, logo) | `PRESERVE` |
| Needs current or factual real-world data | `GROUNDED` |
| Text or typography is the point | `TEXT` |
| Sketch or wireframe to be rendered out | `SKETCH` |
| Panels, storyboard, step sequence | `SEQUENTIAL` |
| Same character, multiple angles or scenes | `CONSISTENCY` |

Ambiguous cases: `PRESERVE` beats `EDIT` whenever a human face or a brand mark is in the frame.
`TEXT` is a modifier, not a replacement, when the asset is a poster with a photo in it. Layer the
`TEXT` rules on top of the base skeleton.

---

## Step 2 — Pick the detail vocabulary

The operation gives you the skeleton. The output category gives you the words that go in the slots.
Load only the section you need from `references/vocabularies.md`.

`PEOPLE` · `PRODUCT` · `TYPOGRAPHIC` · `EXPLANATORY` · `MOCKUP` · `ENVIRONMENT` · `ILLUSTRATION`

Anything involving human likeness also loads `references/people.md`. That file contains the identity
preservation and multi-person anchoring patterns and it is not optional. Face work fails in specific,
repeatable ways and those lines are the fix.

---

## Step 3 — Fill every slot

Write the prompt as structured prose. Labelled blocks are fine and often better than one paragraph
for NB Pro, because it reasons over structure.

**There is no word limit.** This is the single most common mistake carried over from older models.
NB2 and NB Pro are thinking models that generate interim composition images before rendering, so long
structured prompts get reasoned over rather than diluted. Google's own guidance is to be hyper-specific
and their showcase prompts run 100 to 250 words. A 400-word prompt for a hard brief is correct.

Check completeness instead of length: every slot in the skeleton is filled or consciously omitted.

Ask the user before writing only when a missing slot would change the image materially. Body build for
a full-length shot, text content for a poster, brand colours for a mockup. Otherwise choose well and
move on.

---

## Non-negotiable rules

These come from official docs. Violating any of them measurably degrades output.

1. **Positive framing only.** Describe the intended scene, never the absence. "An empty, deserted
   street" not "no cars". Google calls the correct form a semantic negative prompt.
2. **Text goes in quotes with a described font.** `The headline "URBAN EXPLORER" in a bold, white,
   sans-serif font across the top third.` Never "add a headline".
3. **Text-first for text-heavy assets.** Generate and confirm the copy in conversation first, then ask
   for the image containing that exact copy. Two steps, not one. Official guidance.
4. **Every reference image gets an explicit role.** "Image 1 is the character's face. Image 2 is the
   art style. Image 3 is the background." Unlabelled references get averaged.
5. **Every edit carries a preservation clause.** "Keep everything else in the image exactly the same,
   preserving the original style, lighting and composition." This one line does more work than the rest
   of an edit prompt combined.
6. **Camera language over adjectives.** `low-angle`, `macro`, `85mm at f/1.8`, `three-point softbox`,
   `eye-level`. Named hardware shifts the whole look: GoPro, Fujifilm, disposable camera.
7. **Materials, not object names.** "Navy wool tweed", not "a suit". "Brushed anodised aluminium", not
   "metal". Texture is what makes renders read as real.
8. **State the purpose.** "A logo for a high-end minimalist skincare brand" beats "a logo". Intent
   changes the output.
9. **Numeric human measurements do not transfer.** Kilograms, centimetres and clothing sizes mean
   nothing to the model. Map to visual descriptors before injection. See `references/people.md`.
10. **Never fabricate model capabilities.** If the user asks for something outside the limits in Step 0,
    say so plainly rather than writing a prompt that cannot work.

---

## Output contract

### Chat mode (default)

Output in this order, nothing else:

1. The prompt. Plain text, ready to paste. No preamble, no markdown fences around it.
2. One settings line: `gemini-3-pro-image · 2K · 4:5`
3. Only if genuinely needed, up to three short lines: what will likely need a retry, what the model
   cannot do here, and the one knob worth turning.

No essays about lighting theory. No alternative versions unless asked.

### Backend mode

If the user says the prompt is for programmatic generation, a pack, a template, or an API call, switch
output to a JSON object: one key per slot, plus `model`, `aspect_ratio`, `image_size`. The renderer
composes the string. Do not hand a backend a prose blob it has to string-replace.

Aspect ratio placement differs by surface. Gemini app: put it in the prose. API: use `response_format`
with `aspect_ratio` and `image_size` and leave it out of the prompt text.

---

## Known limitations to surface honestly

Do not oversell. Google documents these:

- Small text and fine detail spelling still fails. Verify every rendered word.
- Data in generated diagrams and infographics is not trustworthy. Always fact-check.
- Multilingual text makes grammar and cultural nuance errors.
- Blending and lighting changes can produce unnatural artefacts.
- Character consistency across edits varies even within limits.
- The model will not reliably honour a requested number of output images.
- Every output carries a SynthID watermark and C2PA content credentials.

Best supported languages: EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR,
ru-RU, ua-UA, vi-VN, zh-CN.

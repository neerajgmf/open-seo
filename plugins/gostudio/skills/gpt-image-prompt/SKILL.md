---
name: gpt-image-prompt
description: >
  Write production-grade image generation and editing prompts for OpenAI's GPT Image models
  (GPT Image 2, GPT Image 1.5, GPT Image 1, GPT Image 1 Mini). Use this skill whenever the
  user wants a prompt for AI image generation or editing on GPT Image, gpt-image-1, gpt-image-2,
  OpenAI image, or ChatGPT image models. Triggers include "image prompt", "photo prompt",
  "headshot prompt", "portrait prompt", "product shot prompt", "poster prompt", "infographic prompt",
  "logo prompt", "mockup prompt", "thumbnail prompt", "edit this image", "change the background",
  "put this person in", "style transfer", "combine these images", "face to full body", "group photo",
  "GPT image prompt", "OpenAI image prompt", "ChatGPT image prompt". Also trigger when the user
  uploads a reference image and wants a prompt that reproduces, edits, or extends it using OpenAI
  models. Grounded in OpenAI's official API docs, the GPT Image Generation Models Prompting Guide
  cookbook, and the gpt-image-1.5 prompting guide.
---

# GPT Image Prompt Engineer

You write one prompt. It works first try more often than not. You do not write three variants
and you do not explain photographic theory.

Grounded in OpenAI's official guidance: the Image Generation API docs, the GPT Image Generation
Models Prompting Guide cookbook, and the gpt-image-1.5 prompting guide.

---

## Step 0 — Route the model

Model choice is an **output** of the brief, not an input. Derive it, then state it.

| Model | API ID | Max Resolution | Use when |
|---|---|---|---|
| **GPT Image 2** | `gpt-image-2` | 4096x4096 (4K) | Default flagship. Best text rendering (~99% accuracy). Up to 16 reference images. Highest quality. Best for commercial assets |
| **GPT Image 1.5** | `gpt-image-1.5` | 1536x1024 | 4x faster than gpt-image-1. Good text rendering. Better logo/face preservation than 1.0. Mid-tier cost |
| **GPT Image 1** | `gpt-image-1` | 1536x1024 | Transparent backgrounds needed. Legacy support. Deprecating Oct 2026 |
| **GPT Image 1 Mini** | `gpt-image-1-mini` | 1536x1024 | High volume, lowest cost (~80% cheaper than 1.0). Same capabilities as 1.0 |

Routing rules that decide it outright:
- Transparent background required → **GPT Image 1 or 1.5** (GPT Image 2 does NOT support transparent backgrounds)
- Commercial text-heavy asset (poster, ad, infographic) → **GPT Image 2** (best text fidelity)
- Budget/high-volume batch → **GPT Image 1 Mini**
- Speed-critical with good quality → **GPT Image 1.5** (4x faster)
- Highest resolution needed (4K) → **GPT Image 2** only
- Everything else → **GPT Image 2**

**Resolution and aspect ratio.** All models support: `1024x1024` (square), `1536x1024` (landscape),
`1024x1536` (portrait), `auto` (model chooses). GPT Image 2 additionally supports up to 4096x4096.

**Quality levels.** All models: `low`, `medium`, `high`, `auto` (default). Use `high` for text-heavy
images, infographics, and print-ready assets. Use `low` for drafts and high-volume batches.

**Output formats.** `png` (default, supports transparency), `webp` (supports transparency, good
compression), `jpeg` (no transparency). Compression control via `output_compression` (0-100%) for
jpeg and webp.

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
| Text or typography is the point | `TEXT` |
| Sketch or wireframe to be rendered out | `SKETCH` |
| Panels, storyboard, step sequence | `SEQUENTIAL` |
| Same character, multiple angles or scenes | `CONSISTENCY` |
| Extending image beyond original borders | `OUTPAINT` |

Ambiguous cases: `PRESERVE` beats `EDIT` whenever a human face or a brand mark is in the frame.
`TEXT` is a modifier, not a replacement, when the asset is a poster with a photo in it. Layer the
`TEXT` rules on top of the base skeleton.

---

## Step 2 — Pick the detail vocabulary

The operation gives you the skeleton. The output category gives you the words that go in the slots.
Load only the section you need from `references/vocabularies.md`.

`PEOPLE` · `PRODUCT` · `TYPOGRAPHIC` · `EXPLANATORY` · `MOCKUP` · `ENVIRONMENT` · `ILLUSTRATION`

Anything involving human likeness also loads `references/people.md`. That file contains the identity
preservation and multi-person anchoring patterns and it is not optional.

---

## Step 3 — Fill every slot

Write the prompt as structured prose following the canonical order:

**Background/Scene → Subject → Key Details → Constraints**

State the **intended use** (ad, UI mock, infographic, social post, product shot) at the start or
end to set the generation "mode" and level of polish.

**Labelled segments work well** for complex prompts because GPT Image models are autoregressive
(they reason over structure rather than averaging keywords):

```
Scene: [description]
Subject: [description]
Details: [specifics]
Constraints: [exclusions]
```

**There is no meaningful word limit.** GPT Image models accept prompts up to 32,000 characters.
These are autoregressive models that generate image tokens sequentially (like text), so long
structured prompts get reasoned over rather than diluted. OpenAI's own showcase prompts run
50 to 250 words. A 400-word prompt for a hard brief is correct.

Check completeness instead of length: every slot in the skeleton is filled or consciously omitted.

Ask the user before writing only when a missing slot would change the image materially. Body build
for a full-length shot, text content for a poster, brand colours for a mockup. Otherwise choose
well and move on.

---

## Non-negotiable rules

These come from official OpenAI docs and cookbook. Violating any of them measurably degrades output.

1. **Positive framing only.** Describe the intended scene, never the absence. "An empty, deserted
   street" not "no cars". GPT Image has no negative prompt parameter. Saying "not X" increases the
   likelihood of X appearing because the word enters the model's attention.
2. **Text goes in quotes with a described font.** `The headline "URBAN EXPLORER" in a bold, white,
   sans-serif font across the top third.` Add "render verbatim" and "no extra words or characters."
3. **Text-first for text-heavy assets.** Settle the copy in conversation first, then ask for the
   image containing that exact copy. Two steps, not one. Official guidance.
4. **Every reference image gets an explicit role.** "Image 1 is the character's face. Image 2 is
   the clothing reference. Image 3 is the background." Unlabelled references get averaged.
5. **Every edit carries a preservation clause.** "Keep everything else in the image exactly the same,
   preserving the original style, lighting, composition, and all other objects." Restate invariants
   on every iteration to prevent drift.
6. **Camera language over adjectives.** `low-angle`, `macro`, `85mm at f/1.4`, `three-point softbox`,
   `eye-level`. Named hardware shifts the whole look: GoPro, Fujifilm, Hasselblad.
7. **Materials, not object names.** "Navy wool tweed", not "a suit". "Brushed anodised aluminium",
   not "metal". Texture is what makes renders read as real.
8. **State the purpose.** "A hero image for a premium skincare brand's landing page" beats "a
   product photo". Intent changes the output mode and polish level.
9. **Constraints go at the END.** Put exclusions ("no text", "no watermark", "no extra elements")
   after all positive descriptors. Placing them early causes the model to weight them as
   compositional guidance rather than exclusions.
10. **Never fabricate model capabilities.** If the user asks for something outside the limits in
    Step 0, say so plainly rather than writing a prompt that cannot work.
11. **Iterate, don't overload.** Start with a clean base prompt, then refine with small, single-change
    follow-ups. One change per turn beats cramming everything into one prompt.

---

## Output contract

### Chat mode (default)

Output in this order, nothing else:

1. The prompt. Plain text, ready to paste. No preamble, no markdown fences around it.
2. One settings line: `gpt-image-2 · 1536x1024 · high`
3. Only if genuinely needed, up to three short lines: what will likely need a retry, what the model
   cannot do here, and the one knob worth turning.

No essays about lighting theory. No alternative versions unless asked.

### Backend mode

If the user says the prompt is for programmatic generation, a pack, a template, or an API call,
switch output to a JSON object: one key per slot, plus `model`, `size`, `quality`, `output_format`.
The renderer composes the string. Do not hand a backend a prose blob it has to string-replace.

API parameters go in the API call, not in the prompt text: `size`, `quality`, `output_format`,
`background`, `n`.

---

## Known limitations to surface honestly

Do not oversell. OpenAI documents these:

- **Hands and body proportions** remain the most common failure point, though substantially
  improved over DALL-E 3. Budget retries for full-body shots.
- **Counting objects** is unreliable. "Exactly 5 apples" may produce 4 or 6.
- **Small and rotated text** still fails. Non-Latin scripts are less reliable than English/Latin.
- **Identity drift** across iterations, even with explicit preservation instructions. Restate
  invariants on every call.
- **Mask precision** in edits: the model uses masks as guidance, not exact pixel boundaries. Edits
  may bleed outside the masked area.
- **Data in generated diagrams and infographics** is not trustworthy. Always fact-check.
- **GPT Image 2 does NOT support transparent backgrounds.** Use GPT Image 1 or 1.5 for that.
- **Skin can turn plastic** in photorealistic rendering. Add "natural texture and pores" to defend.
- Every output carries SynthID watermark and C2PA content credentials. No opt-out.

### Model deprecation timeline

| Model | Deprecation date |
|---|---|
| DALL-E 2, DALL-E 3 | Removed May 12, 2026 |
| gpt-image-1 | October 23, 2026 |
| gpt-image-1.5, gpt-image-1-mini | December 1, 2026 |
| gpt-image-2 | Active (flagship) |

New projects should default to `gpt-image-2` unless transparent backgrounds are required.

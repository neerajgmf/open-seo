---
name: seedream-prompt
description: >
  Write production-grade image generation and editing prompts for ByteDance's Seedream models
  (Seedream 4.5, Seedream 5.0 Lite, Seedream 5.0 Pro). Use this skill whenever the user wants
  a prompt for AI image generation or editing on Seedream, ByteDance image, or Doubao image
  models. Triggers include "image prompt", "photo prompt", "headshot prompt", "portrait prompt",
  "product shot prompt", "poster prompt", "infographic prompt", "logo prompt", "mockup prompt",
  "thumbnail prompt", "edit this image", "change the background", "style transfer", "combine
  these images", "face to full body", "group photo", "Seedream prompt", "Seedream 4.5 prompt",
  "Seedream 5 prompt", "Seedream 5 Pro prompt". Also trigger when the user uploads a reference
  image and wants a prompt that reproduces, edits, or extends it using Seedream models.
  Grounded in ByteDance's official Seedream documentation, the Seed Team technical papers, and
  third-party API documentation from Segmind, fal.ai, and Runware.
---

# Seedream Prompt Engineer

You write one prompt. It works first try more often than not. You do not write three variants
and you do not explain photographic theory.

Seedream is developed by **ByteDance** (the company behind TikTok/Douyin), not Google. It uses
a Diffusion Transformer (DiT) architecture trained on billions of text-image pairs.

---

## Step 0 — Route the model

Model choice is an **output** of the brief, not an input. Derive it, then state it.

| Model | API ID | Max Resolution | Ref Images | Use when |
|---|---|---|---|---|
| **Seedream 5.0 Pro** | `seedream-5-0-pro` | 2K native (~4MP) | Up to 10 | Default flagship. Best text rendering (14 languages). Deep Thinking reasoning. Region/anchor/sketch editing. Layer separation. Design-aware generation |
| **Seedream 4.5** | `seedream-4-5` | 4K native (~16.7MP) | Up to 14 | Highest native resolution. Best portrait skin realism. Full user control (guidance_scale, seed, negative_prompt). More reference images |
| **Seedream 5.0 Lite** | `seedream-5-0-lite` | 2K native | Up to 14 | Deep Thinking + web search grounding. Sequential generation (up to 15 outputs). Budget-friendly |

Routing rules that decide it outright:
- 4K native resolution needed → **Seedream 4.5** only
- Layer separation (split into transparent PNGs) → **Seedream 5.0 Pro** only
- Region/anchor/sketch editing → **Seedream 5.0 Pro** only
- Non-English/non-Chinese text rendering → **Seedream 5.0 Pro** (14 languages native)
- Maximum reference images (>10) → **Seedream 4.5 or 5.0 Lite** (up to 14)
- Sequential batch generation → **Seedream 5.0 Lite** (up to 15 sequential outputs)
- Real-time web data in image → **Seedream 5.0 Lite or Pro** (web search grounding)
- Fine-grained user control (guidance_scale, seed, negative_prompt) → **Seedream 4.5**
- Portrait with maximum skin realism → **Seedream 4.5** (5.0 Pro over-smooths skin)
- Everything else → **Seedream 5.0 Pro**

**Resolution.** Seedream 4.5: `2K` (default, ~8-9MP) and `4K` (~16.7MP). Seedream 5.0 Pro/Lite:
`1K` (~2MP) and `2K` (~4MP). Always generate at 1024x1024 minimum — sub-1K outputs are soft.

**Aspect ratios.** All models: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`.
Seedream 4.5 also supports `match_input_image` for editing.

**API endpoint.** BytePlus ModelArk: `POST https://ark.ap-southeast.bytepluses.com/api/v3/images/generations`

**Seedream 4.5 user-controlled parameters:**

| Parameter | Default | Recommended |
|---|---|---|
| `guidance_scale` | 7.0 | 7-9 general; 5.5-7.5 portraits; 8-12 strict adherence |
| `num_inference_steps` | 30 | 24-30 |
| `seed` | -1 (random) | Any int for reproducibility |
| `negative_prompt` | (none) | 15-25 terms max |

**Seedream 5.0 Pro stripped these controls.** The model handles guidance, steps, and seed
internally. Users control only: prompt, resolution, aspect ratio, reference images, and
editing mode.

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
| Mark a specific spot to edit (point, bbox, arrow) | `REGION` |
| Split output into separate transparent layers | `LAYER` |

`REGION`, `LAYER`, and `SKETCH` editing are **Seedream 5.0 Pro only**.
`SEQUENTIAL` batch generation is **Seedream 5.0 Lite only** (Pro does not support it).

---

## Step 2 — Pick the detail vocabulary

The operation gives you the skeleton. The output category gives you the words that go in the
slots. Load only the section you need from `references/vocabularies.md`.

`PEOPLE` · `PRODUCT` · `TYPOGRAPHIC` · `EXPLANATORY` · `MOCKUP` · `ENVIRONMENT` · `ILLUSTRATION`

Anything involving human likeness also loads `references/people.md`. That file contains the
identity preservation and multi-person patterns and it is not optional.

---

## Step 3 — Fill every slot using the SPACE framework

Seedream prompts follow the **SPACE** framework:

| Element | What to specify |
|---|---|
| **S**ubject | The main focus, described literally |
| **P**alette and style | Colors, artistic direction, film stock, medium |
| **A**rrangement | Layout hierarchy, element positioning, composition |
| **C**amera and light | Shot type, focal length, lighting direction and quality |
| **E**xtra detail | In-image text, language, brand context, constraints |

Front-load the most important element. Seedream prioritizes what comes first in the prompt.

Write **natural-language sentences**, not keyword stacks. Seedream has strong natural language
understanding — full sentences outperform comma-separated keyword lists, especially on 5.0 Pro.

**Optimal prompt length: 30–100 words.** Under 15 words produces generic results (the model
fills in too many details on its own). Over 150 words causes conflicting instructions to
compete. Seedream 5.0 Pro handles longer prompts better due to its reasoning layer, but
still keep it under 150 words.

Check completeness instead of length: every slot in the SPACE framework is filled or
consciously omitted.

Ask the user before writing only when a missing slot would change the image materially.

---

## Non-negotiable rules

These come from official docs and confirmed community patterns. Violating any of them
measurably degrades output.

1. **Positive framing first, negation last.** Describe what you want to see. If you must
   exclude something, append it at the end. Seedream has no dedicated negative prompt field
   in 5.0 Pro — use inline negation sparingly (1-2 items). On 4.5, keep `negative_prompt` to
   15-25 terms maximum.
2. **Text goes in double quotes with a described font.** `The headline "URBAN EXPLORER" in
   bold, white, sans-serif font across the top third.` Always specify placement, style, and
   language for non-English text.
3. **Every reference image gets an explicit role.** "Image 1 is the character's face. Image 2
   is the art style. Image 3 is the background." Unlabelled references get averaged.
4. **Every edit carries a preservation clause.** "Keep everything else unchanged — preserve
   face, hairstyle, pose, clothing, expression, and body position exactly as they are."
   Name what stays, not just what changes.
5. **Camera language over adjectives.** `low-angle`, `macro`, `85mm at f/1.8`, `three-point
   softbox`, `eye-level`. Named hardware shifts the whole look. Lighting direction and quality
   do more than mood words.
6. **Materials, not object names.** "Navy wool tweed", not "a suit". Texture is what makes
   renders read as real.
7. **State the purpose.** "An editorial fashion portrait for a luxury brand campaign" beats
   "a photo of a woman". Intent changes the output mode.
8. **Be literal.** Describe what you see in the frame, not how the result should feel.
   "Late afternoon, low sun, stark shadows" beats "warm atmosphere".
9. **One camera contract per image.** Pick one coherent set of camera settings (lens, aperture,
   film stock) and stick with it. Mixing "macro" with "wide-angle" produces confusion.
10. **Never fabricate model capabilities.** If the user asks for something outside the limits
    in Step 0, say so plainly.
11. **Generate at 2K for text.** Typography accuracy degrades at 1K. Always use 2K resolution
    for text-heavy assets.

---

## Output contract

### Chat mode (default)

Output in this order, nothing else:

1. The prompt. Plain text, ready to paste. No preamble, no markdown fences around it.
2. One settings line: `seedream-5-0-pro · 2K · 16:9`
3. For Seedream 4.5 only, add: `guidance_scale: 7.5 · steps: 30`
4. Only if genuinely needed, up to three short lines: what will likely need a retry, what the
   model cannot do here, and the one knob worth turning.

No essays about lighting theory. No alternative versions unless asked.

### Backend mode

If the user says the prompt is for programmatic generation, a pack, a template, or an API call,
switch output to a JSON object: one key per slot, plus `model`, `aspect_ratio`, `resolution`.
For Seedream 4.5, also include `guidance_scale`, `num_inference_steps`, `seed`,
`negative_prompt`. The renderer composes the string.

Aspect ratio and resolution go in the API call, not in the prompt text.

---

## Known limitations to surface honestly

Do not oversell. ByteDance and community testing document these:

- **Seedream 5.0 Pro over-smooths skin** compared to 4.5. For maximum portrait realism, use 4.5
  and add "natural skin texture, visible pores and fine expression lines."
- **Long text (10+ words) garbles** across all versions. Keep text to 3-5 words per element.
- **Small text and background text** drift and lose accuracy. Generate at 2K minimum.
- **Hands and jewelry** remain inconsistent. Budget retries.
- **Pose preservation during edits** is unreliable — changing clothing often shifts the pose.
- **Action overshoot** in dynamic scenes on 5.0 Pro. Tone down action descriptors.
- **Content-filter false positives** on 5.0 Pro (stricter moderation than 4.5).
- **Data in generated diagrams** is not trustworthy. Always fact-check.
- **5.0 Pro native resolution** maxes at 2K (4.5 goes to 4K native).
- **Color banding artifacts** occasionally appear — no fix documented.
- **Extreme aspect ratios** (21:9, 1:3) sometimes produce stretched compositions.

### Pricing (BytePlus ModelArk)

| Model | 1K price | 2K price |
|---|---|---|
| Seedream 5.0 Pro | ~$0.045/image | ~$0.090/image |
| Seedream 5.0 Lite | ~$0.031/image | — |
| Seedream 4.5 | ~$0.036/image | ~$0.040/image |

First reference image is free; each additional reference is ~$0.003.

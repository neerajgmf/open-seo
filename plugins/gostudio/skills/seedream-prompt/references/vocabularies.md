# Detail Vocabularies

The operation gives the skeleton. This file gives the words for the slots.
Load one section. Do not paste vocabulary lists into prompts — use them to choose.

---

## PEOPLE

See `people.md`. It is the full module, not a section here.

---

## PRODUCT

Slots that matter most: surface, lighting rig, angle, focus point.

```
A high-resolution product photograph of PRODUCT_DESCRIPTION on SURFACE.
The lighting is LIGHTING_SETUP to LIGHTING_PURPOSE.
The camera angle is ANGLE to showcase FEATURE.
Sharp focus on KEY_DETAIL, natural reflections and shadows.
```

- Lighting rigs: three-point softbox setup, single large softbox with a white bounce card,
  hard directional key with a black flag, ring light, natural window light with sheer diffusion.
- Surfaces: polished concrete, brushed travertine, raw linen, seamless paper sweep, brushed
  steel, matte acrylic riser, wet slate, light marble.
- Angles: straight-on hero, elevated 45-degree, top-down flat lay, low hero angle, macro
  three-quarter.
- Materials, always: brushed anodised aluminium, matte ceramic glaze, frosted glass,
  vegetable-tanned leather, injection-moulded soft-touch plastic.
- Name the focus point explicitly. "Sharp focus on the condensation beading on the glass."

### Product negative prompt (Seedream 4.5 only)
```
overblown highlights, plastic reflections, warped labels, extra logos, bent packaging,
fake text, watermark
```

---

## TYPOGRAPHIC — posters, logos, covers, ads

Load the `TEXT` rules from `operations.md` first — they are mandatory here.

- **Generate at 2K resolution minimum** for all text-heavy assets.
- Route to **Seedream 5.0 Pro** for multilingual text (14 languages native).
- Font description carries further than a font name, but give both when you know it.
- Specify hierarchy explicitly: which line is largest, what sits where, alignment, spacing.
- State "no other text" when you mean it.
- Hex colour codes work well for precise palette control: `"Background in #2D6A4F, text
  in #FFFFFF, accent in #F4A261."`
- Keep text to 3-5 words per text element for reliability.

---

## EXPLANATORY — infographics, diagrams, educational visuals

- Generate at 2K resolution minimum.
- Add a factual-accuracy constraint: "a scientifically accurate cross-section".
- But still tell the user to verify — data in generated diagrams is not trustworthy.
- Give the structure: number of steps, reading order, where labels sit, legend placement.
- Metaphor framing produces better layouts: "Explain photosynthesis as if it were a recipe."
- Name the audience. "Suitable for a 4th grader" changes density and vocabulary.
- Seedream 5.0 Pro supports **complex information visualization** — it can transform
  data/concepts into professional layouts.

---

## MOCKUP — brand applications, packaging, apparel, environment

- Always state the surface behaviour: "printed on the fabric, following the folds of the
  shirt", "embossed into the matte board", "silkscreened onto the curved bottle".
- For a set, generate one at a time. Feed prior outputs back as references for consistency.
- For brand consistency, define a brand style block and include it in every prompt:
  ```
  Brand style: [Brand name] visual identity.
  Colors: #1A73E8 blue, #FFFFFF white, #333333 dark gray.
  Typography: bold sans-serif headers, clean body text.
  Tone: professional, modern, approachable.
  ```
- Useful set members: billboard, bus stop, storefront signage, packaging box, tote, apparel,
  business card, app icon, vehicle wrap.
- Seedream 5.0 Pro's layer separation can split mockup output into separate transparent layers
  for downstream compositing.

---

## ENVIRONMENT — scenes, architecture, landscape, interiors

```
A photorealistic SHOT_TYPE of SCENE in CONDITIONS.
LIGHT_QUALITY_AND_DIRECTION. Shot from PERSPECTIVE with LENS.
GRADE_AND_FILM_STOCK.
```

- Time and weather do more than adjectives: "late afternoon, low sun, stark shadows".
- Film stock and grade set the emotional register:
  - "Portra 400" for warm, soft, flattering skin tones
  - "Velvia" for saturated landscapes
  - "Cinestill 800T" for warm tungsten with halation
  - "grainy 35mm film" for nostalgic texture
  - "clean modern digital, neutral white balance" for clinical sharpness
- Scale needs a lens: wide-angle for vastness, macro for intricacy, telephoto for compression.
- Isometric and miniature treatments work well and need the term stated outright.
- Seedream 5.0 Lite with web search grounding can incorporate real-world data into
  environmental visualizations.

---

## ILLUSTRATION — stickers, icons, 2D art, stylised work

```
A STYLE of SUBJECT doing ACTIVITY.
The design features VISUAL_QUALITIES and COLOUR_OR_BACKGROUND_PREFERENCE.
```

- Name medium and rendering method: cel-shading, flat vector, gouache, risograph, 3D clay
  render, pencil on textured parchment, high-contrast black and white ink.
- Line weight matters: "bold, clean outlines" versus "no outlines, soft edges".
- For cut-out assets: "the background must be white" or "on a solid [color] background".
  Say "no text" for icons.
- Colour direction beats colour lists: "a simple two-tone scheme, light blue ground with deep
  blue mark" outperforms naming six hexes.
- Seedream excels at anime and Asian art styles — these are a documented strength over
  competing models.

---

## PHOTOREALISM — camera-language vocabulary

Use camera and photography terms instead of generic quality keywords. "85mm lens" carries
more visual information than "8K ultra-detailed".

**Lens vocabulary:**
- 24mm wide-angle: environmental context, slight barrel distortion
- 35mm: natural street photography feel
- 50mm: standard, natural perspective
- 85mm: portrait isolation, shallow depth of field, gentle compression
- 135mm: strong compression, extreme subject isolation

**Aperture vocabulary:**
- f/1.4: heavy bokeh, dreamy background
- f/2.8: moderate bokeh, good subject separation
- f/5.6: balanced sharpness
- f/11: sharp throughout, landscape-style

**Lighting setups:**
- Rembrandt lighting: triangle of light on cheek, dramatic portrait
- Butterfly lighting: shadow under nose, beauty/fashion
- Split lighting: half face lit, half in shadow, dramatic
- Chiaroscuro: dramatic high-contrast, Renaissance-inspired
- Three-point lighting: key + fill + back, standard studio
- Rim/edge lighting: glowing outline, separation from background

**Film stock and grade:**
- Kodak Portra 400: warm, soft, flattering skin tones
- Fujifilm Velvia: saturated, punchy landscapes
- Cinestill 800T: warm tungsten, halation around highlights
- "grainy 35mm film": nostalgic, textured
- "clean modern digital, neutral white balance": clinical, sharp

---

## CFG (Guidance Scale) Reference — Seedream 4.5 only

Seedream 5.0 Pro does not expose guidance scale. For Seedream 4.5:

| Range | Effect | Best for |
|---|---|---|
| 5.0–6.0 | More creative, artistic, loose | Abstract art, experimental work |
| 5.5–7.5 | Natural portraits (below 5 gets mushy, above 8 stiffens) | Portraits, headshots |
| 7.0–9.0 | General sweet spot | Most content |
| 8.0–9.0 | Tighter prompt matching | Product photography, precise compositions |
| 10.0+ | Risk of oversaturation (~40% of generations) | Avoid unless very specific need |

---

## Negative prompt patterns — Seedream 4.5 only

Keep to **15–25 terms** for best results. Seedream 5.0 Pro does not have a negative prompt
field — use inline natural language negation (1-2 items max) instead.

### General purpose
```
blurry, low resolution, artifacts, distorted, deformed, extra fingers, watermarks,
unnatural skin texture, harsh shadows, oversaturated colors, cartoon effects
```

### Portrait-specific
```
extra fingers, distorted hands, deformed eyes, asymmetrical face, blurry face,
mutated limbs, cartoon effects, unnatural skin texture
```

### Product photography
```
overblown highlights, plastic reflections, warped labels, extra logos, bent packaging,
fake text, watermark
```

### Don't preemptively negate
Generate first, then add negatives to fix specific observed problems. Positive phrasing
outperforms negation: "relaxed natural hands resting at her side" beats "no weird hands".

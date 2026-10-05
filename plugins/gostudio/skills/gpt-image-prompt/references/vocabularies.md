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
A high-resolution, studio-lit product photograph of PRODUCT_DESCRIPTION on SURFACE.
The lighting is LIGHTING_SETUP to LIGHTING_PURPOSE.
The camera angle is ANGLE to showcase FEATURE.
Ultra-realistic, with sharp focus on KEY_DETAIL.
No text, no watermark.
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
- Emphasize tactile realism: paper layers, fibers, folds, fabric weave — so the result reads
  as a photographed physical product rather than a flat illustration.

---

## TYPOGRAPHIC — posters, logos, covers, ads

Load the `TEXT` rules from `operations.md` first — they are mandatory here.

- Route to **GPT Image 2** for anything going to a customer. Text fidelity is its clearest
  advantage (~99% character-level accuracy).
- Use `quality: high` for all text-heavy assets.
- Font description carries further than a font name, but give both when you know it: "a heavy
  geometric sans, similar to Futura Bold".
- Specify hierarchy explicitly: which line is largest, what sits where, alignment, spacing.
- Cut-out and calligram effects work well: "the text acts as a cut-out window, a photograph
  visible ONLY inside the letterforms."
- Negative space belongs in the prompt if the design needs breathing room: "a vast, empty
  off-white canvas creating significant negative space."
- State "no other text" and "no extra characters" when you mean it. The model adds decorative
  filler otherwise.
- Keep text short: under 10 words per text element for reliability.
- For logos: "clean vector style, no gradients, no extra elements or text beyond the mark itself."

---

## EXPLANATORY — infographics, diagrams, educational visuals

- Use `quality: high` for all explanatory assets.
- Add a factual-accuracy constraint in the prompt: "a scientifically accurate cross-section",
  "ensure historical accuracy for the Victorian era".
- But still tell the user to verify. OpenAI documents that data in generated diagrams is not
  trustworthy.
- Give the structure, not just the topic: number of steps, reading order, where labels sit,
  whether there is a legend.
- Metaphor framing produces better layouts than a bare topic. "Explain photosynthesis as if
  it were a recipe, with ingredients and a finished dish."
- Name the audience. "Suitable for a 4th grader" changes density and vocabulary.
- Specify colour palette and style: "clean infographic style, blue and white palette, minimal
  design."
- Add "render all text verbatim, no additional words" for any text-bearing explanatory asset.

---

## MOCKUP — brand applications, packaging, apparel, environment

- GPT Image 2 handles this best: it drapes patterns, logos and artwork onto 3D surfaces while
  preserving lighting and texture.
- Always state the surface behaviour: "printed on the fabric, following the folds of the shirt",
  "embossed into the matte board", "silkscreened onto the curved bottle".
- For a set, generate one at a time. Ask for a consistent aspect ratio across the set and
  feed prior outputs back as references.
- Useful set members: billboard, bus stop, storefront signage, packaging box, tote, apparel,
  business card, app icon, vehicle wrap.
- For brand consistency, define a brand style block and prepend it to every prompt:
  ```
  Brand style: [Brand name] visual identity.
  Colors: #1A73E8 blue, #FFFFFF white, #333333 dark gray.
  Typography: bold sans-serif headers, clean body text.
  Tone: professional, modern, approachable.
  ```

---

## ENVIRONMENT — scenes, architecture, landscape, interiors

```
A photorealistic SHOT_TYPE of SCENE in CONDITIONS.
LIGHT_QUALITY_AND_DIRECTION. Shot from PERSPECTIVE with LENS.
GRADE_AND_FILM_STOCK.
No text, no watermark.
```

- Time and weather do more work than adjectives: "late afternoon, low sun, stark shadows".
- Film stock and grade set the emotional register: "as if on 1980s colour film, slightly grainy",
  "cinematic grading with muted teal tones", "clean modern digital, neutral white balance".
- Scale needs a lens: wide-angle for vastness, macro for intricacy, telephoto compression for
  stacking layers.
- Isometric and miniature treatments work well and need the term stated outright.
- Specify mood through environmental details, not adjectives: "fog rolling through a pine forest"
  beats "mysterious atmosphere".

---

## ILLUSTRATION — stickers, icons, 2D art, stylised work

```
A STYLE of SUBJECT doing ACTIVITY.
The design features VISUAL_QUALITIES and COLOUR_OR_BACKGROUND_PREFERENCE.
No text.
```

- Name medium and rendering method: cel-shading, flat vector, gouache, risograph, 3D clay
  render, pencil on textured parchment, high-contrast black and white ink.
- Line weight and outline treatment matter: "bold, clean outlines" versus "no outlines, soft
  edges".
- For assets that need cut-out use, say "the background must be white" or "on a solid
  [color] background". Say "no text" for icons.
- Colour direction beats colour lists: "a simple two-tone scheme, light blue ground with deep
  blue mark" outperforms naming six hexes.
- For stickers and icons: "clean vector illustration", "solid colors", "minimal shading",
  "no gradients".
- For watercolor: "transparent washes", "paper texture", "soft pigment blooms", "loose
  brushstrokes", "hand-painted".
- For oil painting: "visible brushstrokes", "canvas texture", "impasto technique".

---

## PHOTOREALISM — specific vocabulary for camera-language prompts

Use camera and photography terms instead of generic quality keywords. "85mm lens" carries
more visual information than "8K ultra-detailed award-winning".

**Lens vocabulary:**
- 24mm wide-angle: environmental context, slight barrel distortion
- 35mm: natural street photography feel
- 50mm: standard, natural perspective
- 85mm: portrait isolation, shallow depth of field, gentle compression
- 135mm: strong compression, extreme subject isolation
- 200mm+: telephoto compression, stacking layers, sports/wildlife

**Aperture vocabulary:**
- f/1.4: heavy bokeh, dreamy background, romantic feel
- f/2.8: moderate bokeh, good subject separation
- f/5.6: balanced sharpness and background separation
- f/11: sharp throughout, landscape-style, everything in focus

**Lighting setups:**
- Rembrandt lighting: triangle of light on cheek, dramatic portrait
- Butterfly lighting: shadow under nose, beauty/fashion
- Split lighting: half face lit, half in shadow, dramatic
- Three-point lighting: key + fill + back, standard studio
- Rim/edge lighting: glowing outline, separation from background

**Film stock and grade:**
- Kodak Portra 400: warm, soft, flattering skin tones
- Fujifilm Pro 400H: cool, clean, slight green cast
- Cinestill 800T: warm tungsten, halation around highlights
- Kodachrome: saturated, punchy, vintage
- "Clean modern digital, neutral white balance": clinical, sharp

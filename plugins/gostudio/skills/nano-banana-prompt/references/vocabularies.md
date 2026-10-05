# Detail Vocabularies

The operation gives the skeleton. This file gives the words for the slots.
Load one section. Do not paste vocabulary lists into prompts, use them to choose.

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
```

- Lighting rigs: three-point softbox setup, single large softbox with a white bounce card, hard
  directional key with a black flag, ring light, natural window light with sheer diffusion.
- Surfaces: polished concrete, brushed travertine, raw linen, seamless paper sweep, brushed steel,
  matte acrylic riser, wet slate.
- Angles: straight-on hero, elevated 45-degree, top-down flat lay, low hero angle, macro three-quarter.
- Materials, always: brushed anodised aluminium, matte ceramic glaze, frosted glass, vegetable-tanned
  leather, injection-moulded soft-touch plastic.
- Name the focus point explicitly. "Sharp focus on the condensation beading on the glass."

---

## TYPOGRAPHIC — posters, logos, covers, ads

Load the `TEXT` rules from `operations.md` first, they are mandatory here.

- Route to Pro for anything going to a customer.
- Font description carries further than a font name, but give both when you know it: "a heavy
  geometric sans, similar to Futura Bold".
- Specify hierarchy explicitly: which line is largest, what sits where, alignment, spacing.
- Cut-out and calligram effects work well: "the text acts as a cut-out window, a photograph visible
  ONLY inside the letterforms."
- Negative space belongs in the prompt if the design needs breathing room: "a vast, empty off-white
  canvas creating significant negative space."
- State "no other text" when you mean it. The model adds decorative filler otherwise.

---

## EXPLANATORY — infographics, diagrams, educational visuals

- Pair with `GROUNDED` when facts matter, and still tell the user to verify. Google is explicit that
  data in generated diagrams is not trustworthy.
- Add a factual-accuracy constraint in the prompt: "a scientifically accurate cross-section", "ensure
  historical accuracy for the Victorian era".
- Give the structure, not just the topic: number of steps, reading order, where labels sit, whether
  there is a legend.
- Metaphor framing produces better layouts than a bare topic. "Explain photosynthesis as if it were a
  recipe, with ingredients and a finished dish" is Google's own example and it works.
- Name the audience. "Suitable for a 4th grader" changes density and vocabulary.

---

## MOCKUP — brand applications, packaging, apparel, environment

- Pro handles this best: it drapes patterns, logos and artwork onto 3D surfaces while preserving
  lighting and texture.
- Always state the surface behaviour: "printed on the fabric, following the folds of the shirt",
  "embossed into the matte board", "silkscreened onto the curved bottle".
- For a set, generate one at a time. Ask for a consistent aspect ratio across the set and feed prior
  outputs back as references.
- Useful set members: billboard, bus stop, storefront signage, packaging box, tote, apparel, business
  card, app icon, vehicle wrap.

---

## ENVIRONMENT — scenes, architecture, landscape, interiors

```
A photorealistic SHOT_TYPE of SCENE in CONDITIONS.
LIGHT_QUALITY_AND_DIRECTION. Shot from PERSPECTIVE with LENS.
GRADE_AND_FILM_STOCK.
```

- Time and weather do more work than adjectives: "late afternoon, low sun, stark shadows".
- Film stock and grade set the emotional register: "as if on 1980s colour film, slightly grainy",
  "cinematic grading with muted teal tones", "clean modern digital, neutral white balance".
- Scale needs a lens: wide-angle for vastness, macro for intricacy, telephoto compression for stacking
  layers.
- Isometric and miniature treatments work well and need the term stated outright.

---

## ILLUSTRATION — stickers, icons, 2D art, stylised work

```
A STYLE of SUBJECT doing ACTIVITY.
The design features VISUAL_QUALITIES and COLOUR_OR_BACKGROUND_PREFERENCE.
```

- Name medium and rendering method: cel-shading, flat vector, gouache, risograph, 3D clay render,
  pencil on textured parchment, high-contrast black and white ink.
- Line weight and outline treatment matter: "bold, clean outlines" versus "no outlines, soft edges".
- For assets that need cut-out use, say "the background must be white" or "on a transparent-looking
  solid background". Say "no text" for icons.
- Colour direction beats colour lists: "a simple two-tone scheme, light blue ground with deep blue
  mark" outperforms naming six hexes.

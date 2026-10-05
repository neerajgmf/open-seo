---
name: gostudio-brand-guidelines
description: Source-of-truth GoStudio.ai brand guideline skill. Use this whenever a task needs GoStudio logo rules, colors, typography, visual identity, design tone, collateral style, brand values, or brand/design audit checks. Other GoStudio skills should call this skill before making brand, visual, color, typography, or logo judgments.
---

# GoStudio.ai Brand Guidelines

Use this skill as the brand/design source for GoStudio.ai. It supplies brand guideline references to audit, copywriting, and design tasks.

## Required References

Read for routine checks:

- `references/brand-guidelines/brand-guidelines.md`

Use for exact visual verification:

- `references/brand-guidelines/Brand_Guidelines_compressed-5mb.pdf`

## Brand Collateral Assets

Visual brand collateral is stored in `assets/`:

- `1 (1).webp` — Hero/landing page promotional graphic with logo, headshot examples, and product copy.
- `2.jpg` — Social media collateral: "Your Look. Your Voice. Tailored for Every Social."
- `b1.jpg` — Social media collateral: "Same You. Different Vibe. For All Your Socials."
- `b28.png` — LinkedIn headshot promotional graphic with logo and gradient bar.
- `b29.png` — First impressions promotional graphic with logo and gradient bar.
- `b30.jpg` — Social media collateral (variant of 2.jpg).

Use these as visual references for brand tone, logo placement, gradient usage, social media style, and collateral consistency checks.

## Use This For

- Logo usage, logomark, logotype, lockup, clear space, minimum size, placement, and mistakes.
- Brand colors, palette, tints, gradients, and combinations.
- Typography, Poppins usage, logotype typeface, weights, and type scale.
- Tone of voice: professional, friendly, informative, inspiring.
- Brand values: authenticity, inclusivity, innovation/creativity, excellence.
- Graphic and visual element checks.
- Collateral style reference.

## Call Flow

When another skill needs brand guidance:

1. Load this skill or read `references/brand-guidelines/brand-guidelines.md`.
2. Use the markdown guide for normal text-based checks.
3. Use the PDF when the exact visual treatment matters.
4. If product positioning or pricing conflicts with brand collateral, defer product facts to `gostudio-product-marketing-context` and report the conflict.

## Non-Negotiables

- Do not rely only on memory for color, typography, or logo rules.
- Do not replace exact visual checks with a summary when the issue is visual.
- Do not silently merge old PDF positioning with newer product marketing context.

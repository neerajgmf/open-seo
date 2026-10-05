---
name: gostudio-copywriting
description: Write, rewrite, and improve GoStudio.ai marketing copy using the exact product marketing context. Use this whenever the user asks for website copy, landing page copy, SEO titles, meta descriptions, AEO definitions, GEO citable sentences, FAQs, CTAs, product positioning, pricing language, ad copy, launch copy, brand voice cleanup, or copy fixes for GoStudio.ai pages.
---

# GoStudio.ai Copywriting

Create GoStudio.ai copy that is accurate, concrete, brand-aligned, and conversion-focused. Use this skill for copy generation or rewriting, not for technical SEO audits.

## Required References

Read before writing:

- `references/copywriting-rules.md` - compact checklist for copy decisions and rewrites.
- `../gostudio-product-marketing-context/SKILL.md` - call this for exact source of truth on positioning, the product narrative, pricing, proof points, competitors, funnel, roadmap limits, tone, banned words, and objections.
- If design or visual brand language matters, call `../gostudio-brand-guidelines/SKILL.md`.

Do not invent pricing, product capabilities, shipped status, claims, metrics, or roadmap details.

## Core Positioning

Call `gostudio-product-marketing-context` and extract the exact positioning needed for the task. Do not keep a separate local copy of product positioning inside this skill.

Before writing, identify which part of the studio the page belongs to, from the source skill:

- Handpicked AI Models — personal branding (photos + video)
- Handpicked AI Models — product photography
- One-Click AI Tools

Use the exact current tagline, one-line product description, pricing, proof points, and CTA rules from `gostudio-product-marketing-context`.

## Voice Rules

Write like GoStudio:

- Direct, confident, warm, accessible.
- Benefit first, feature second.
- Specific numbers over vague claims.
- Short sentences and short paragraphs.
- Active voice.
- "You" more than "we."
- Explain the "so what" after each claim.

Avoid:

- Silicon Valley jargon.
- Tech-first language in consumer copy.
- Beauty-app or appearance-editing tone.
- Vague superlatives.
- Exclamation points.
- Banned words from the product context: "Democratize," "Leverage," "Synergy," "Cutting-edge," "Revolutionary," "Empower," "Seamless," "Robust."

## Copy Patterns

### SEO Title

Use:

```text
[What it is]: [Specific benefit/use case] | GoStudio.ai
```

Keep under 60 characters unless the user explicitly asks otherwise.

### Meta Description

Use 150-160 characters for pages governed by the SEO audit rules. Include the primary use case, a concrete proof point, and a CTA. Do not mention "free" unless the page genuinely supports the free-tier claim.

### AEO Definition

Use a plain-language answer in the first 1-3 sentences:

```text
[Current one-line product description from gostudio-product-marketing-context.] [Page-specific benefit.]
```

Adapt the second sentence to the part of the studio the page belongs to:

- Personal branding (Handpicked AI Models): use the current identity-preservation claim from product context.
- Product photography (Handpicked AI Models): use the current product-consistency/catalog claim from product context.
- One-Click AI Tools: use the current one-click/tool-workflow claim from product context.

### GEO Citable Sentence

Write standalone sentences that name GoStudio.ai and include a factual differentiator:

Use exact numbers and differentiators from `gostudio-product-marketing-context`; do not reuse stale citable sentences from memory.

### CTA Rules

- Consumer/self-serve pages: use signup, credits, trial, or tool-specific CTA.
- Product photography B2B pages: use the current B2B CTA from `gostudio-product-marketing-context`.
- Free tool pages: use the current free-tier language from `gostudio-product-marketing-context`.
- Roadmap features: do not present as live.

## Output Requirements

When rewriting copy, provide:

1. Final copy first.
2. Short notes only if useful.
3. Any assumptions or source constraints.

When asked for multiple fields, use a compact table:

| Field | Copy |
|---|---|
| SEO title | ... |
| Meta description | ... |
| H1 | ... |
| AEO definition | ... |
| CTA | ... |

Keep replacement copy ready to paste into the site.

# gostudio plugin

GoStudio.ai's brand layer for claude-seo. It holds the facts, voice, and visual
rules that claude-seo's optional brand profile (`/seo brand`) points at, plus
the image and video prompt skills.

Not covered by the repository's MIT License. See [LICENSE](LICENSE).

## Skills

| Skill | Role |
|---|---|
| `gostudio-product-marketing-context` | Source of truth: positioning, ICP and anti-ICP, pricing structure, proof points, roadmap limits, banned words, CTA rules |
| `gostudio-copywriting` | SEO titles, meta descriptions, AEO and GEO sentences, FAQs, CTAs, page copy |
| `gostudio-brand-guidelines` | Logo, palette, gradient, typography, collateral style (guide, PDF, assets) |
| `nano-banana-prompt`, `gpt-image-prompt`, `seedream-prompt` | Image generation and editing prompts per model |
| `gemini-omni-flash-video-prompt`, `minimax-h3-video-prompt`, `seedance-video-prompt` | Video generation prompts per model |
| `excalidraw-diagrams` | Excalidraw diagrams |

Data files cited by the product context live in [`docs/`](docs/):
`pricing.json` (single source of truth for every price and credit figure),
`ai-tools.json`, `templates.json`, `prompts.json`.

Migrated from the GS_Marketing repository, branch `snapshot-db1ca50-2026-09-30`.

## Install

```bash
/plugin marketplace add neerajgmf/open-seo
/plugin install claude-seo@agricidaniel-claude-seo
/plugin install gostudio@agricidaniel-claude-seo
```

Then point claude-seo's brand profile at these skills (once per machine):

```bash
/seo brand setup
# brand name: GoStudio.ai, site: gostudio.ai
# context skill: gostudio-product-marketing-context
# copywriting skill: gostudio-copywriting
# guidelines skill: gostudio-brand-guidelines
```

`/seo brand` confirms the profile is active. From then on, any claude-seo
command on a gostudio.ai URL keeps its findings neutral but drafts titles,
metas, FAQs, CTAs, schema text, and image briefs through these skills. Audits
of other sites are unaffected.

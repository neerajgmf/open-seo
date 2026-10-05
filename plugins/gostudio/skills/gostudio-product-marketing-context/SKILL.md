---
name: gostudio-product-marketing-context
description: Source-of-truth product marketing context for GoStudio.ai. Use this whenever a task needs GoStudio positioning, the product narrative, pricing, funnel logic, competitors, proof points, roadmap boundaries, brand voice, objections, capabilities, or business context. Other GoStudio skills should call this skill before making product, pricing, positioning, or copy claims.
---

# GoStudio.ai Product Marketing Context

Use this skill as the product-marketing source of truth for GoStudio.ai. It does not produce audits by itself unless the user asks for product-positioning review; it supplies the facts and constraints other skills need.

## Required Reference

Read:

- `references/product-marketing-context.md`

This file is exact source material. Do not rewrite, summarize as a replacement, or invent product facts beyond it.

**Data file paths.** The reference cites `docs/pricing.json`, `docs/ai-tools.json`, `docs/templates.json`, `docs/prompts.json`, and `docs/competitor-research/competitor-landscape.md`. In this plugin those live in the plugin's own `docs/` folder: `../../docs/<file>` from this skill's folder. `pricing.json` is the single source of truth for every price and credit figure. Mentions of `work-log/` and `TASKS.md` point at the retired GS_Marketing repository and have no copy here.

## Use This For

- Product positioning
- The product narrative: **"Your AI Studio for photos and videos — without the complexity."** The lead capability is One-Click AI Tools and templates for everyday visual jobs; Handpicked AI Models (including identity training) is the supporting capability. Preserve the "you direct the studio" principle — *"You command. AI executes."*
- **"Your" means ownership and authorship, not likeness.** Your product, your brand's content, your face — all three. Never write "Your" as a promise that the user's face is in the output.
- **Values & Philosophy** — the four pillars (values as the moat, use-case simplicity, creators create the value, no AI slop). This is the strategic foundation; read it before positioning or About-page work.
- Customer segments / ICPs (simple-needs buyers, ecommerce, headshots & photos, photographers) **and the anti-ICP** — abusers seeking deepfakes or non-consensual imagery (refused on values), and fun-only users with no job to do (not served). **Marketing agencies are NOT anti-ICP.**
- **Two separate identity flows** — Flow A (trained models: headshots & photos, live, unchanged, training charge applies) and Flow B (character sheet / referencing for characters and objects, in development, no training). Never merge them in copy or imply training is being replaced.
- Pricing and credit claims
- Free-tier claims
- B2B vs consumer CTA rules
- Competitor comparisons
- **Prompts vs Templates vs Tools** — three distinct surfaces, never interchangeable. Prompts are text organised by model, on **open ungated pages published both on GoStudio.ai and GitHub**, existing purely for SEO/AEO discovery and routing users onward; templates are prompt + reference images + placeholders, pinned to SOTA models; One-Click AI Tools are built per use case and may run a *different* model for cost or better output. **"One-Click AI Tools" is the only term — "one-click apps" is retired.** Never name the model behind a tool.
- **Curated by default; direct model access for subscribers — and it is marketed.** Both facts are true: nobody *has to* choose a model, and someone who wants to may. Write "never has to choose", never "cannot choose". **The pitch is consolidation, not aggregation:** "one platform, every handpicked model, no juggling ten different platform subscriptions." Prefer that generic phrasing over naming providers; never "choose from 50 models" — that is what the competitive frame positions against. **If copy does name ChatGPT or Gemini, bound the substitution to photo and video work** — those subscriptions also buy chat, writing, and code, which GoStudio does not replace.
- **The selection rule.** Only handpicked models, each chosen as **either the most cost-effective or the best available** for its job. Write "the right model for the job", never "only the best model" — the latter is inaccurate wherever cost decided. Never imply *every* model on the market; the roster is deliberately narrow. Never describe it with the word "play" (that word is the Anti-ICP discriminator).
- Funnel and acquisition strategy — including the use-case page → **template or tool** routing fork
- Roadmap boundaries
- Proof points and quantified claims
- Brand voice, banned words, and copy constraints
- Co-creation pillar ("Built With You" mechanisms)
- Objections and responses

## Call Flow

When another skill needs product context:

1. Load this skill or directly read `references/product-marketing-context.md`.
2. Extract only the relevant section for the task.
3. Treat the context as higher priority than older brand collateral when product scope, pricing, roadmap, or positioning differs.
4. If a page or reference conflicts with this context, report the conflict clearly.

## Non-Negotiables

- Do not invent pricing.
- Do not present roadmap items as shipped.
- Do not use banned words from the context in live copy.
- Do not use B2B demo flow language on consumer pages unless the context allows it.
- Do not use consumer credit/signup CTAs on B2B product-photography pages.

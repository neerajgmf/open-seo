# Brand Profile Contract

An optional brand profile lets claude-seo write deliverable copy and visual
briefs in one brand's voice, when the site under analysis belongs to that
brand. Everything brand-specific lives outside this repository: a user-space
config names installed skills, and those skills hold the facts, voice and
visual rules.

## Detect

Run before drafting any copy or visual brief:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run brand_context.py match --url <target-url>
```

- `active: false`: no profile, a broken profile, or the URL belongs to
  another site. Proceed brand-neutral and do not mention the profile, except
  when `configured: true` and `errors` is non-empty and the host would have
  matched: then report the errors once, so the user can fix the setup.
- `active: true`: apply this contract. `skills` names the installed skills:
  `context_skill` (required), `copywriting_skill` and `guidelines_skill`
  (optional).

Commands that take a topic instead of a URL (`content-brief`,
`competitor-pages generate`, `programmatic plan`, `image-gen`) run `match`
against the user's own site. Ask for it when it is not clear from the
request; never assume the profile's site.

## What changes and what does not

| Output | Brand profile active |
|---|---|
| Findings, scores, priorities, evidence | Unchanged. Always brand-neutral. |
| Deliverable copy: SEO title, meta description, H1, intro, AEO definition, GEO citable sentence, FAQ answers, CTAs, alt text, comparison-page copy, brief voice notes | Drafted through `copywriting_skill` |
| Schema text fields: Organization `name`/`description`/`sameAs`/`logo`, Product and Service descriptions | Facts from `context_skill` only |
| Visual briefs: OG and hero image prompts, page mockups, competitor-page HTML, image recommendations | Rules from `guidelines_skill` |

Loading: invoke the named skills with the Skill tool and follow their own
"required references" instructions. Load only the sections the task needs.
Never paste a brand skill's content into a report verbatim beyond the copy
being delivered.

If `copywriting_skill` is not configured, write the copy yourself, using
`context_skill` for facts, voice and banned words.

## Precedence

1. The user's explicit instruction in this conversation.
2. `context_skill`: product facts, pricing, roadmap status, positioning,
   banned words, CTA rules. It wins over everything below on facts.
3. `copywriting_skill`: copy patterns and voice rules.
4. `guidelines_skill`: visual identity. Within it, the written guide wins
   over older PDF or collateral examples where they disagree.
5. claude-seo's SEO rules (length limits, schema requirements, quality gates).

SEO rules are not silently overridden. When a brand rule and an SEO rule
conflict (a title pattern that exceeds the pixel limit, a "free" claim the
page cannot support, a banned word in a required schema field), deliver the
brand-compliant version, then list the conflict under **Brand conflicts**
with both rules and the trade-off.

## Hard rules

- Never invent pricing, metrics, customer counts, or capabilities. If
  `context_skill` does not state it, leave a `[NEEDS SOURCE]` placeholder.
- Never present roadmap items as shipped.
- Never use the context's banned words in deliverable copy, including words
  inherited from older brand collateral. Flag collateral that uses them.
- Keep the brand's CTA rules per page type (for example consumer signup vs
  B2B demo) exactly as the context defines them.
- The brand profile changes how copy is written, never what the audit finds.
  A weak page is still reported as weak.

## Report section

When the profile is active, add one short section at the end of the output:

```markdown
## Brand profile
- Applied: <brand_name> (matched <matched_site>)
- Sources: <context_skill>, <copywriting_skill>, <guidelines_skill>
- Brand conflicts: <none | list>
```

## Setup

`/seo brand setup` collects the brand name, the domains the brand owns, and
the installed skill names, then runs:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run brand_context.py setup \
  --brand-name "<name>" --site <domain> [--site <domain>] \
  --context-skill <skill> [--copywriting-skill <skill>] [--guidelines-skill <skill>]
```

`/seo brand` (or `/seo brand status`) runs `brand_context.py status` and
reports whether the profile is active and which skills are missing. The
config is written to `~/.config/claude-seo/brand.json` and never committed.

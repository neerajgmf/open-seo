---
name: seo-openpanel
description: OpenPanel product analytics via the hosted OpenPanel MCP (extension). Organic traffic, top and entry pages, referrers, page conversions, funnels, retention, plus OpenPanel's Search Console data (queries, opportunities, cannibalization). Triggers on "OpenPanel", "open panel", "product analytics", "page conversions", "user tracking", "GA4 alternative".
metadata:
  version: "2.4.1"
compatibility: "Requires an OpenPanel read or root API client. Run extensions/openpanel/install.sh to register the openpanel MCP server in ~/.claude.json."
---

# seo-openpanel

Reads first-party analytics from OpenPanel (https://openpanel.dev) through
its hosted MCP server at `https://api.openpanel.dev/mcp`. Use it to tie SEO
findings to real visitor behavior: which organic landing pages get traffic,
how long people stay, and whether they convert.

## Prerequisites

- Run `extensions/openpanel/install.sh` (or `install.ps1`).
- An OpenPanel API client of type `read` (one project) or `root` (all
  projects). Write-only clients are rejected by the server.
- Before any call, confirm the `mcp__openpanel__*` tools are available. If
  they are missing, tell the user to run the installer and start a new
  Claude Code session.

## Routing

| Command | MCP tools |
|---|---|
| `/seo openpanel projects` | `list_projects`, `get_dashboard_urls` |
| `/seo openpanel overview [project]` | `get_analytics_overview`, `get_rolling_active_users` |
| `/seo openpanel top-pages` | `get_top_pages`, `get_page_performance` |
| `/seo openpanel entry-pages` | `get_entry_exit_pages` |
| `/seo openpanel referrers` | `get_top_referrers` (organic vs. other channels) |
| `/seo openpanel conversions [event]` | `get_page_conversions`, `get_funnel` |
| `/seo openpanel engagement` | `get_engagement_metrics`, `get_user_flow` |
| `/seo openpanel audience` | `get_country_breakdown`, `get_device_breakdown` |
| `/seo openpanel retention` | `get_retention_cohort`, `get_weekly_retention_series` |
| `/seo openpanel gsc [overview\|queries\|pages]` | `gsc_get_overview`, `gsc_get_top_queries`, `gsc_get_top_pages` |
| `/seo openpanel gsc opportunities` | `gsc_get_query_opportunities` |
| `/seo openpanel gsc cannibalization` | `gsc_get_cannibalization` |

Start with `list_projects` when the user has not named a project, then
pass the project ID to later calls. Read each tool's input schema rather
than guessing parameter names. For custom questions, discover the data first
with `list_event_names` and `list_event_properties`, then use
`query_events` or `query_sessions`.

The `gsc_*` tools return data only if the project has Google Search Console
connected inside OpenPanel. If they return nothing, fall back to `seo-google`.

## Output conventions

- Cite the source on every metric: "OpenPanel (first-party, project <name>)".
- State the date range used. Default to the last 28 days, the same window as
  `seo-google` and `seo-matomo`, so figures from each can be compared directly.
- Do not show individual visitor profiles (`find_profiles`, `get_profile*`)
  in SEO reports. Report aggregated figures only, unless the user asks
  for a specific profile.

## Limits

- 60 requests per minute per client. Batch questions and avoid looping over
  pages one call at a time when an aggregated tool (`get_top_pages`,
  `get_page_performance`) answers the question.

## Cross-skill delegation

- For Google field data, indexation, and GSC data not in OpenPanel, hand off to `seo-google`.
- For a self-hosted Matomo instance, use `seo-matomo`.
- For content fixes on underperforming landing pages, hand back to `seo-content` or `seo-page`.

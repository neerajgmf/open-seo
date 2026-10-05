# OpenPanel extension setup

[OpenPanel](https://openpanel.dev) is an open-source product analytics
platform. This extension connects its hosted MCP server
(`https://api.openpanel.dev/mcp`, see https://openpanel.dev/docs/mcp) so
SEO findings can be checked against first-party traffic and conversion data.

## Get credentials

In the OpenPanel dashboard, create an API client under Settings -> Clients:

- `read`: access to one project (recommended).
- `root`: access to every project in the organization.

Write-only clients are rejected by the MCP server. Copy the Client ID and
Client Secret.

## Install

```bash
./extensions/openpanel/install.sh        # Linux / macOS
.\extensions\openpanel\install.ps1       # Windows
```

The installer:

1. Prompts for the Client ID and Client Secret (the secret is not echoed).
2. Builds the MCP token, `base64("<client id>:<client secret>")`.
3. Writes `mcpServers.openpanel` to `~/.claude.json` (mode 0600) as an HTTP
   server with an `Authorization: Bearer <token>` header.
4. Copies the `seo-openpanel` skill into `~/.claude/skills/`.

Equivalent manual setup:

```bash
TOKEN=$(printf '%s' "CLIENT_ID:CLIENT_SECRET" | base64)
claude mcp add --scope user --transport http openpanel https://api.openpanel.dev/mcp \
  --header "Authorization: Bearer ${TOKEN}"
```

## Verify

Start a new Claude Code session, then:

```
/mcp                       # openpanel should show as connected
/seo openpanel projects
```

## Uninstall

```bash
./extensions/openpanel/uninstall.sh
```

## Notes

- Rate limit: 60 requests per minute per client.
- The `gsc_*` tools need Google Search Console connected inside OpenPanel.
- Never commit the Client Secret or the token. Both live only in
  `~/.claude.json`.

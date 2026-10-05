#!/usr/bin/env bash
# Claude SEO: OpenPanel extension installer.
#
# Registers the hosted OpenPanel MCP server (https://api.openpanel.dev/mcp)
# in ~/.claude.json and copies the seo-openpanel skill into ~/.claude/skills/.
#
# Prereq: an OpenPanel API client of type `read` or `root`
# (Dashboard -> Settings -> Clients). Write-only clients are rejected.
set -euo pipefail

main() {
    SKILL_DIR="${HOME}/.claude/skills"
    # MCP servers live in ~/.claude.json (the file `claude mcp add` writes).
    # NOT ~/.claude/settings.json - `mcpServers` is not a key Claude Code reads
    # there, so entries written to settings.json silently never load.
    MCP_CONFIG_JSON="${HOME}/.claude.json"

    echo "════════════════════════════════════════"
    echo "║   Claude SEO: OpenPanel extension    ║"
    echo "════════════════════════════════════════"

    command -v python3 >/dev/null 2>&1 || {
        echo "✗ Python 3 required."; exit 1;
    }

    if [ ! -d "${SKILL_DIR}/seo" ]; then
        echo "✗ claude-seo base plugin not installed."
        echo "  Install it first: curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/install.sh | bash"
        exit 1
    fi

    SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" >/dev/null 2>&1 && pwd)"

    read -rp "OpenPanel Client ID: " OP_CLIENT_ID
    read -rsp "OpenPanel Client Secret: " OP_CLIENT_SECRET
    echo
    if [ -z "${OP_CLIENT_ID}" ] || [ -z "${OP_CLIENT_SECRET}" ]; then
        echo "✗ Client ID and Client Secret are both required."; exit 1;
    fi

    mkdir -p "${SKILL_DIR}/seo-openpanel"
    cp "${SOURCE_DIR}/skills/seo-openpanel/SKILL.md" "${SKILL_DIR}/seo-openpanel/SKILL.md"
    echo "✓ Installed skill: ${SKILL_DIR}/seo-openpanel/SKILL.md"

    # Merge MCP config into ~/.claude.json atomically.
    mkdir -p "$(dirname "${MCP_CONFIG_JSON}")"
    CLAUDE_SEO_USERNAME="${OP_CLIENT_ID}" CLAUDE_SEO_SECRET="${OP_CLIENT_SECRET}" \
        python3 - "${MCP_CONFIG_JSON}" <<'PY'
import base64
import json
import os
import sys
import tempfile

# Credentials arrive in the environment, not argv: argv is visible to other
# local users through ps, the environment is not.
path = sys.argv[1]
client_id = os.environ["CLAUDE_SEO_USERNAME"].strip()
secret = os.environ["CLAUDE_SEO_SECRET"].strip()
# OpenPanel's MCP token is base64("<client id>:<client secret>").
token = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
data = {}
if os.path.exists(path):
    try:
        with open(path) as fh:
            data = json.load(fh)
    except json.JSONDecodeError:
        sys.exit(f"✗ {path} is not valid JSON. Nothing was changed; fix it and rerun.")
# Send the token as a header rather than ?token= so it stays out of URLs.
data.setdefault("mcpServers", {})["openpanel"] = {
    "type": "http",
    "url": "https://api.openpanel.dev/mcp",
    "headers": {"Authorization": f"Bearer {token}"},
}
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".",
                          prefix=".settings.", suffix=".json")
try:
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, indent=2)
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
except Exception:
    if os.path.exists(tmp):
        os.unlink(tmp)
    raise
print(f"✓ Wrote mcpServers.openpanel to {path}")
PY

    echo
    echo "Done. Open a new Claude Code session and run:"
    echo "  /seo openpanel projects"
    echo
    echo "Full docs: extensions/openpanel/docs/OPENPANEL-SETUP.md"
}

main "$@"

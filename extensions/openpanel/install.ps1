# Claude SEO - OpenPanel extension installer (Windows / PowerShell).
# Mirrors extensions/openpanel/install.sh.
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$SkillDir = Join-Path $HOME ".claude/skills"
# MCP servers live in ~/.claude.json (the file `claude mcp add` writes).
# NOT ~/.claude/settings.json - `mcpServers` is not a key Claude Code reads
# there, so entries written to settings.json silently never load.
$McpConfigJson = Join-Path $HOME ".claude.json"

if (-not (Test-Path (Join-Path $SkillDir "seo"))) {
    throw "claude-seo base plugin not installed."
}

$ClientId = (Read-Host "OpenPanel Client ID").Trim()
$Secret = Read-Host "OpenPanel Client Secret" -AsSecureString
$Plain = [System.Net.NetworkCredential]::new("", $Secret).Password.Trim()
if (-not $ClientId -or -not $Plain) { throw "Client ID and Client Secret are both required." }

# OpenPanel's MCP token is base64("<client id>:<client secret>").
$Token = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($ClientId + ":" + $Plain))

$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillTarget = Join-Path $SkillDir "seo-openpanel"
New-Item -ItemType Directory -Path $SkillTarget -Force | Out-Null
Copy-Item -Path (Join-Path $SourceDir "skills/seo-openpanel/SKILL.md") `
          -Destination (Join-Path $SkillTarget "SKILL.md") -Force
Write-Host "[OK] Installed skill: $SkillTarget"

# Merge ~/.claude.json.
$settingsContent = if (Test-Path $McpConfigJson) { Get-Content $McpConfigJson -Raw | ConvertFrom-Json } else { [pscustomobject]@{} }
if (-not $settingsContent.mcpServers) { $settingsContent | Add-Member -NotePropertyName mcpServers -NotePropertyValue ([pscustomobject]@{}) -Force }
# Send the token as a header rather than ?token= so it stays out of URLs.
$settingsContent.mcpServers | Add-Member -NotePropertyName 'openpanel' -NotePropertyValue @{
    type = 'http'
    url = 'https://api.openpanel.dev/mcp'
    headers = @{ Authorization = "Bearer $Token" }
} -Force
# Write atomically: stage to a temp file in the same directory, then swap
# it into place, so a crash mid-write never leaves ~/.claude.json truncated.
# -Depth 100 so an existing deeply nested ~/.claude.json round-trips intact.
$TempConfigJson = Join-Path (Split-Path -Parent $McpConfigJson) ".claude.json.$([guid]::NewGuid().ToString('N')).tmp"
$jsonText = $settingsContent | ConvertTo-Json -Depth 100
# Write without a byte-order mark: Node's JSON.parse rejects a BOM.
[System.IO.File]::WriteAllText($TempConfigJson, $jsonText, (New-Object System.Text.UTF8Encoding $false))
Move-Item -Path $TempConfigJson -Destination $McpConfigJson -Force
Write-Host "Wrote mcpServers.openpanel to $McpConfigJson"

Write-Host ""
Write-Host "Done. Open a new Claude Code session and run /seo openpanel projects."

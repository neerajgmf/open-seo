#!/usr/bin/env python3
"""
Brand profile resolver for Claude SEO.

A brand profile lets the copy-producing skills (titles, meta descriptions,
FAQs, CTAs, comparison pages, image prompts) write in one brand's voice when,
and only when, the target site belongs to that brand. Audits of any other
site stay brand-neutral.

The profile lives in user space, never in the repository:

    ~/.config/claude-seo/brand.json
    {
      "brand_name": "Example Co",
      "sites": ["example.com"],
      "context_skill": "example-product-marketing-context",
      "copywriting_skill": "example-copywriting",
      "guidelines_skill": "example-brand-guidelines"
    }

Only ``brand_name``, ``sites`` and ``context_skill`` are required. The three
skill fields name installed Claude Code skills; this script checks that each
one resolves to a ``SKILL.md`` (user, project, this repo's ``plugins/*/skills``,
or an installed plugin) and reports its path, but never reads or prints brand
content.
Claude loads that content through the Skill tool, following
``skills/seo/references/brand-context.md``.

This script makes no network requests: ``match`` compares hostnames only, so
it does not need ``url_safety``.

Usage:
    python brand_context.py status
    python brand_context.py match --url https://www.example.com/pricing
    python brand_context.py setup --brand-name "Example Co" --site example.com \\
        --context-skill example-product-marketing-context \\
        [--copywriting-skill example-copywriting] \\
        [--guidelines-skill example-brand-guidelines]

All commands print JSON. Environment overrides (mainly for tests):
    CLAUDE_SEO_BRAND_CONFIG      alternate config path
    CLAUDE_SEO_BRAND_SKILL_DIRS  extra skill directories, os.pathsep-separated
"""

import argparse
import glob
import json
import os
import re
import sys
import tempfile
from typing import Optional
from urllib.parse import urlparse

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/claude-seo/brand.json")
CONFIG_ENV = "CLAUDE_SEO_BRAND_CONFIG"
SKILL_DIRS_ENV = "CLAUDE_SEO_BRAND_SKILL_DIRS"

SKILL_FIELDS = ("context_skill", "copywriting_skill", "guidelines_skill")
REQUIRED_SKILL_FIELDS = ("context_skill",)

# Skill names are directory names; the pattern also rules out path traversal.
_SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
_HOST_RE = re.compile(r"^(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")


def config_path() -> str:
    """Return the brand profile path, honouring the env override."""
    return os.environ.get(CONFIG_ENV) or DEFAULT_CONFIG_PATH


def skill_dirs() -> list:
    """Directories searched for named skills, in priority order.

    Covers user and project skills, skills shipped by plugins inside this
    repository (``plugins/*/skills``), and skills of installed plugins in
    Claude Code's plugin cache.
    """
    dirs = []
    extra = os.environ.get(SKILL_DIRS_ENV, "")
    dirs.extend(d for d in extra.split(os.pathsep) if d)
    dirs.append(os.path.join(os.getcwd(), ".claude", "skills"))
    dirs.append(os.path.expanduser("~/.claude/skills"))
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dirs.extend(sorted(glob.glob(os.path.join(repo_root, "plugins", "*", "skills"))))
    cache = os.path.expanduser("~/.claude/plugins/cache")
    dirs.extend(sorted(glob.glob(os.path.join(cache, "*", "*", "*", "skills")), reverse=True))
    return dirs


def normalize_host(value: str) -> Optional[str]:
    """Lower-case hostname from a URL or bare domain, without ``www.`` or port."""
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip().lower()
    if "://" not in raw:
        raw = "//" + raw
    host = urlparse(raw).hostname or ""
    if host.startswith("www."):
        host = host[4:]
    return host if _HOST_RE.match(host) else None


def find_skill(name: str) -> Optional[str]:
    """Return the path of ``<name>/SKILL.md`` in the first matching skill dir, or None."""
    for base in skill_dirs():
        path = os.path.join(base, name, "SKILL.md")
        if os.path.isfile(path):
            return path
    return None


def load_profile() -> dict:
    """Read and validate the brand profile.

    Returns a dict with ``configured``, ``active``, ``errors`` and, when the
    file parses, ``brand_name``, ``sites`` and ``skills``. ``active`` is true
    only when there are no errors and every configured skill is installed.
    """
    path = config_path()
    result = {"configured": False, "active": False, "errors": []}
    if not os.path.isfile(path):
        return result
    result["configured"] = True
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        result["errors"].append(f"brand.json is not valid JSON: {exc.__class__.__name__}")
        return result
    if not isinstance(data, dict):
        result["errors"].append("brand.json must be a JSON object")
        return result

    brand_name = data.get("brand_name")
    if not isinstance(brand_name, str) or not brand_name.strip():
        result["errors"].append("brand_name is required")
    else:
        result["brand_name"] = brand_name.strip()

    raw_sites = data.get("sites")
    sites = []
    if not isinstance(raw_sites, list) or not raw_sites:
        result["errors"].append("sites must be a non-empty list of domains")
    else:
        for site in raw_sites:
            host = normalize_host(site)
            if host:
                sites.append(host)
            else:
                result["errors"].append(f"invalid site: {site!r}")
    result["sites"] = sites

    skills = {}
    for field in SKILL_FIELDS:
        name = data.get(field)
        if name is None or name == "":
            if field in REQUIRED_SKILL_FIELDS:
                result["errors"].append(f"{field} is required")
            continue
        if not isinstance(name, str) or not _SKILL_NAME_RE.match(name):
            result["errors"].append(f"{field} must be a kebab-case skill name")
            continue
        path = find_skill(name)
        skills[field] = {"name": name, "installed": path is not None, "path": path}
        if path is None:
            result["errors"].append(f"{field} '{name}' is not installed")
    result["skills"] = skills

    result["active"] = not result["errors"]
    return result


def match_url(url: str) -> dict:
    """Report whether the brand profile applies to ``url``."""
    profile = load_profile()
    host = normalize_host(url)
    matched = None
    if host:
        for site in profile.get("sites", []):
            if host == site or host.endswith("." + site):
                matched = site
                break
    out = dict(profile)
    out["host"] = host
    out["matched_site"] = matched
    out["active"] = bool(profile["active"] and matched)
    if host is None:
        out["errors"] = profile["errors"] + ["url has no valid hostname"]
    return out


def write_profile(args: argparse.Namespace) -> dict:
    """Validate CLI values and write brand.json atomically."""
    errors = []
    sites = []
    for site in args.site:
        host = normalize_host(site)
        if host:
            sites.append(host)
        else:
            errors.append(f"invalid site: {site!r}")
    data = {"brand_name": args.brand_name.strip(), "sites": sites}
    if not data["brand_name"]:
        errors.append("brand_name is required")
    for field in SKILL_FIELDS:
        value = getattr(args, field)
        if value is None:
            continue
        if not _SKILL_NAME_RE.match(value):
            errors.append(f"{field} must be a kebab-case skill name")
        data[field] = value
    if errors:
        return {"written": False, "errors": errors}

    path = config_path()
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".brand-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    except OSError:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    status = load_profile()
    status["written"] = True
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve the Claude SEO brand profile.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Show whether a brand profile is configured and usable")
    match = sub.add_parser("match", help="Check whether the brand profile applies to a URL")
    match.add_argument("--url", required=True, help="Target URL or domain")
    setup = sub.add_parser("setup", help="Write ~/.config/claude-seo/brand.json")
    setup.add_argument("--brand-name", required=True)
    setup.add_argument("--site", action="append", required=True,
                       help="Domain owned by the brand (repeatable)")
    setup.add_argument("--context-skill", dest="context_skill", required=True)
    setup.add_argument("--copywriting-skill", dest="copywriting_skill")
    setup.add_argument("--guidelines-skill", dest="guidelines_skill")
    return parser


def main(argv: Optional[list] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "status":
        out = load_profile()
    elif args.command == "match":
        out = match_url(args.url)
    else:
        out = write_profile(args)
    print(json.dumps(out, indent=2))
    if args.command == "setup" and not out.get("written"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Tests for scripts/brand_context.py, the brand profile resolver.

The resolver decides whether copy-producing skills should write in a brand's
voice. The important property is that it activates only for the brand's own
sites, so audits of competitors and client sites stay brand-neutral, and that
a broken or half-installed profile never activates.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

import brand_context  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    """Isolated config path and skill directory with two installed skills."""
    skills = tmp_path / "skills"
    for name in ("acme-context", "acme-copywriting"):
        (skills / name).mkdir(parents=True)
        (skills / name / "SKILL.md").write_text("---\nname: x\n---\n", encoding="utf-8")
    config = tmp_path / "brand.json"
    monkeypatch.setenv(brand_context.CONFIG_ENV, str(config))
    monkeypatch.setenv(brand_context.SKILL_DIRS_ENV, str(skills))
    monkeypatch.setattr(os.path, "expanduser", lambda p: str(tmp_path / "home") if p == "~/.claude/skills" else p)
    monkeypatch.chdir(tmp_path)
    return config


def _write(config, data):
    config.write_text(json.dumps(data), encoding="utf-8")


VALID = {
    "brand_name": "Acme",
    "sites": ["acme.com"],
    "context_skill": "acme-context",
    "copywriting_skill": "acme-copywriting",
}


def test_no_config_is_inactive(env):
    out = brand_context.load_profile()
    assert out == {"configured": False, "active": False, "errors": []}


def test_valid_profile_is_active(env):
    _write(env, VALID)
    out = brand_context.load_profile()
    assert out["active"] is True
    assert out["brand_name"] == "Acme"
    assert out["skills"]["context_skill"] == {"name": "acme-context", "installed": True}


def test_missing_skill_blocks_activation(env):
    _write(env, {**VALID, "guidelines_skill": "acme-guidelines"})
    out = brand_context.load_profile()
    assert out["active"] is False
    assert any("acme-guidelines" in e for e in out["errors"])


def test_context_skill_is_required(env):
    data = dict(VALID)
    del data["context_skill"]
    _write(env, data)
    out = brand_context.load_profile()
    assert out["active"] is False
    assert "context_skill is required" in out["errors"]


def test_malformed_json_is_reported_not_raised(env):
    env.write_text("{not json", encoding="utf-8")
    out = brand_context.load_profile()
    assert out["configured"] is True
    assert out["active"] is False
    assert out["errors"]


@pytest.mark.parametrize("name", ["../etc", "Acme", "a/b", "x" * 65])
def test_skill_names_cannot_traverse_paths(env, name):
    _write(env, {**VALID, "context_skill": name})
    out = brand_context.load_profile()
    assert out["active"] is False


@pytest.mark.parametrize("url", [
    "https://acme.com/pricing",
    "https://www.acme.com/",
    "https://blog.acme.com/post",
    "acme.com",
    "HTTPS://ACME.COM:443/x",
])
def test_match_own_sites(env, url):
    _write(env, VALID)
    out = brand_context.match_url(url)
    assert out["active"] is True
    assert out["matched_site"] == "acme.com"


@pytest.mark.parametrize("url", [
    "https://competitor.com/",
    "https://notacme.com/",
    "https://acme.com.evil.io/",
    "not a url",
])
def test_other_sites_stay_neutral(env, url):
    _write(env, VALID)
    out = brand_context.match_url(url)
    assert out["active"] is False
    assert out["matched_site"] is None


def test_match_inactive_when_profile_broken(env):
    _write(env, {**VALID, "copywriting_skill": "missing-skill"})
    assert brand_context.match_url("https://acme.com")["active"] is False


def test_setup_writes_profile(env):
    rc = brand_context.main([
        "setup", "--brand-name", "Acme", "--site", "https://www.acme.com/",
        "--context-skill", "acme-context", "--copywriting-skill", "acme-copywriting",
    ])
    assert rc == 0
    data = json.loads(env.read_text(encoding="utf-8"))
    assert data == {
        "brand_name": "Acme",
        "sites": ["acme.com"],
        "context_skill": "acme-context",
        "copywriting_skill": "acme-copywriting",
    }


def test_setup_rejects_bad_values(env):
    rc = brand_context.main([
        "setup", "--brand-name", "Acme", "--site", "not a domain",
        "--context-skill", "../x",
    ])
    assert rc == 2
    assert not env.exists()


def test_cli_prints_json(env, tmp_path):
    _write(env, VALID)
    proc = subprocess.run(
        [sys.executable, os.path.join(_SCRIPTS, "brand_context.py"), "match", "--url", "https://acme.com"],
        capture_output=True, text=True, check=True,
        env={**os.environ, brand_context.CONFIG_ENV: str(env),
             brand_context.SKILL_DIRS_ENV: str(tmp_path / "skills")},
        cwd=tmp_path,
    )
    assert json.loads(proc.stdout)["active"] is True

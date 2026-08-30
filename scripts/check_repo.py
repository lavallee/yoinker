#!/usr/bin/env python3
"""Dependency-free checks for the public Yoinker repository."""

from __future__ import annotations

import re
import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "yoinker" / "SKILL.md"
REQUIRED = (
    "LICENSE",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "RELEASING.md",
    "VERSION",
    "llms.txt",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    "docs/index.html",
    "docs/style.css",
    "docs/site.js",
    "docs/favicon.svg",
    "docs/.nojekyll",
    "evaluation/protocol.md",
    "skills/yoinker/SKILL.md",
    "skills/yoinker/agents/openai.yaml",
    "skills/yoinker/references/assess-an-artifact.md",
    "skills/yoinker/references/answer-an-open-question.md",
    "skills/yoinker/templates/decision-brief.md",
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
LOCAL_PATH = re.compile(r"(?:/home/[^/\s]+|/Users/[^/\s]+|/media/[^/\s]+|[A-Z]:\\Users\\[^\\\s]+)")


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def check_skill(errors: list[str]) -> None:
    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
        return
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError:
        errors.append("SKILL.md frontmatter is not closed")
        return
    fields = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    if fields.get("name") != "yoinker":
        errors.append("SKILL.md name must be yoinker")
    if not fields.get("description"):
        errors.append("SKILL.md description must be non-empty")
    metadata = ROOT / "skills/yoinker/agents/openai.yaml"
    if "$yoinker" not in metadata.read_text(encoding="utf-8"):
        errors.append("agents/openai.yaml default prompt must invoke $yoinker")


def check_version(errors: list[str]) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version):
        errors.append(f"VERSION is not semantic: {version!r}")
        return
    for relative in (
        "README.md",
        "CHANGELOG.md",
        "docs/index.html",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
    ):
        if version not in (ROOT / relative).read_text(encoding="utf-8"):
            errors.append(f"{relative} does not contain version {version}")


def check_plugins(errors: list[str]) -> None:
    manifests = []
    for relative in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        path = ROOT / relative
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"invalid plugin manifest {relative}: {error}")
            continue
        manifests.append((relative, payload))
        if payload.get("name") != "yoinker":
            errors.append(f"{relative} name must be yoinker")
    if len(manifests) == 2 and manifests[0][1].get("version") != manifests[1][1].get("version"):
        errors.append("Claude and Codex plugin versions must match")


def check_site(errors: list[str]) -> None:
    text = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    required_fragments = {
        "worked example": 'id="example"',
        "Codex install command": "codex plugin add yoinker@lyra-forge",
        "Claude Code install command": "/plugin install yoinker@lyra-forge",
        "public repository link": "https://github.com/lavallee/yoinker",
        "copy interaction": 'src="site.js"',
    }
    for label, fragment in required_fragments.items():
        if fragment not in text:
            errors.append(f"landing page is missing {label}")


def check_links(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            clean = target.split("#", 1)[0].strip()
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                errors.append(f"broken relative link: {path.relative_to(ROOT)} -> {target}")


def check_public_hygiene(errors: list[str]) -> None:
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts):
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if match := LOCAL_PATH.search(text):
            errors.append(f"local filesystem path in {path.relative_to(ROOT)}: {match.group(0)}")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    if SKILL.is_file():
        check_skill(errors)
    check_version(errors)
    check_plugins(errors)
    check_site(errors)
    check_links(errors)
    check_public_hygiene(errors)
    if errors:
        print("Yoinker repository checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Yoinker repository checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

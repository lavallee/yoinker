#!/usr/bin/env python3
"""Locate, find, and open Yoinker records. Standard library only.

A record is one Markdown file per assessed artifact or question. It lives in the
project the decision is about (``docs/yoinker/``), or in a per-user store when
there is no project to hold it. A per-user index points at every record this
script opens, so an earlier assessment can be found from any project.

This script never installs, clones, or executes an assessed artifact. Pinning
asks the remote for one ref and reads nothing else.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_RECORDS = Path("docs") / "yoinker"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "decision-brief.md"
FORGES = {"github.com", "gitlab.com", "codeberg.org", "bitbucket.org"}
SAFE_SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
SHA = re.compile(r"[0-9a-f]{40,64}")


def shared_home() -> Path:
    """Per-user store: $YOINKER_HOME, else the XDG data directory."""
    if explicit := os.environ.get("YOINKER_HOME"):
        return Path(explicit).expanduser()
    base = os.environ.get("XDG_DATA_HOME") or "~/.local/share"
    return Path(base).expanduser() / "yoinker"


def project_root(start: Path) -> Path | None:
    """Nearest enclosing git work tree, without invoking git."""
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def resolve_dir(args: argparse.Namespace) -> tuple[Path, str, Path | None]:
    """Return (record directory, reason, project root or None)."""
    root = project_root(Path(args.project))
    if args.dir:
        return Path(args.dir).expanduser().resolve(), "named with --dir", root
    if args.shared:
        return shared_home() / "records", "per-user store requested with --shared", None
    if root is not None:
        return root / PROJECT_RECORDS, f"inside the project at {root}", root
    return shared_home() / "records", "no enclosing project, so the per-user store", None


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def forge_repo(source: str) -> tuple[str, str, str] | None:
    """(host, owner, repo) for an https URL on a known forge, else None."""
    parts = urlsplit(source)
    host = (parts.hostname or "").lower().removeprefix("www.")
    if parts.scheme != "https" or host not in FORGES:
        return None
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) < 2:
        return None
    owner, repo = segments[0], segments[1].removesuffix(".git")
    if not (SAFE_SEGMENT.fullmatch(owner) and SAFE_SEGMENT.fullmatch(repo)):
        return None
    return host, owner, repo


def record_id(source: str) -> str:
    """Stable id: the same source always maps to the same record file."""
    if repo := forge_repo(source):
        host, owner, name = repo
        return slugify(f"{host.split('.')[0]}-{owner}-{name}")
    parts = urlsplit(source)
    if parts.scheme in {"http", "https"} and parts.hostname:
        host = parts.hostname.lower().removeprefix("www.")
        return slugify(f"web-{host}-{parts.path}")[:96].rstrip("-") or "web"
    return f"question-{slugify(source)[:80].rstrip('-') or 'untitled'}"


def pin_revision(source: str, timeout: float = 20) -> tuple[str | None, str]:
    """Ask the forge for the default-branch commit. Returns (sha, note)."""
    repo = forge_repo(source)
    if repo is None:
        return None, "not pinned: not a repository on a known forge; record a version or access date"
    host, owner, name = repo
    url = f"https://{host}/{owner}/{name}"
    command = [
        "git",
        "-c", "protocol.allow=never",
        "-c", "protocol.https.allow=always",
        "ls-remote", "--", url, "HEAD",
    ]
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, env=env, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, f"not pinned: could not reach {url} ({type(error).__name__})"
    first = result.stdout.split()
    if result.returncode != 0 or not first or not SHA.fullmatch(first[0]):
        return None, f"not pinned: {url} did not return a default-branch commit"
    return first[0], "default-branch commit when the record was opened"


def template_body() -> str:
    """The decision brief without its own title line."""
    lines = TEMPLATE.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip() + "\n"


def render(title: str, source: str, revision: str | None, pin_note: str, today: str) -> str:
    is_question = record_id(source).startswith("question-")
    head = [f"# {title}", ""]
    head.append(f"- {'Question' if is_question else 'Source'}: {source}")
    if not is_question:
        pinned = f"`{revision}` ({pin_note})" if revision else pin_note
        head.append(f"- Pinned revision: {pinned}")
    head += [f"- Record opened: {today}", "- Status: open", ""]
    return "\n".join(head) + "\n" + template_body()


def index_path() -> Path:
    return shared_home() / "index.jsonl"


def read_index() -> list[dict[str, str]]:
    path = index_path()
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict):
            entries.append(entry)
    return entries


def append_index(entry: dict[str, str]) -> None:
    path = index_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def matches(path: Path, needles: list[str]) -> bool:
    name = path.stem.lower()
    if any(needle in name for needle in needles):
        return True
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:2000].lower()
    except OSError:
        return False
    return any(needle in head for needle in needles)


def cmd_where(args: argparse.Namespace) -> int:
    directory, reason, _ = resolve_dir(args)
    print(directory)
    print(f"reason: {reason}", file=sys.stderr)
    return 0


def cmd_find(args: argparse.Namespace) -> int:
    query = args.query.strip()
    needles = sorted({query.lower(), record_id(query)} - {""})
    directory, _, _ = resolve_dir(args)
    found: dict[Path, str] = {}
    for place, label in ((directory, "here"), (shared_home() / "records", "per-user store")):
        if place.is_dir():
            for path in sorted(place.glob("*.md")):
                if matches(path, needles):
                    found.setdefault(path.resolve(), label)
    missing = []
    for entry in read_index():
        haystack = f"{entry.get('id', '')} {entry.get('source', '')}".lower()
        if not any(needle in haystack for needle in needles):
            continue
        path = Path(entry.get("record", ""))
        if path.is_file():
            found.setdefault(path.resolve(), "indexed from another project")
        else:
            missing.append(entry)
    for path, label in found.items():
        print(f"{path}\t{label}")
    for entry in missing:
        print(
            f"indexed but no longer present: {entry.get('record')} "
            f"(opened {entry.get('opened', 'unknown')})",
            file=sys.stderr,
        )
    if not found:
        print("no earlier record found", file=sys.stderr)
        return 1
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    source = args.source.strip()
    directory, reason, root = resolve_dir(args)
    identifier = record_id(source)
    path = directory / f"{identifier}.md"
    if path.exists():
        print(path)
        print("a record already exists; update it instead of opening another", file=sys.stderr)
        return 2
    if args.no_pin:
        revision, note = None, "not pinned: pinning was skipped; record a version or access date"
    else:
        revision, note = pin_revision(source)
    today = dt.date.today().isoformat()
    directory.mkdir(parents=True, exist_ok=True)
    path.write_text(render(args.title or source, source, revision, note, today), encoding="utf-8")
    append_index(
        {
            "id": identifier,
            "source": source,
            "record": str(path),
            "project": str(root) if root else "",
            "revision": revision or "",
            "opened": today,
        }
    )
    print(path)
    print(f"record opened {reason}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--project", default=".", help="directory inside the project (default: .)")
    common.add_argument("--dir", help="record directory the project already uses")
    common.add_argument("--shared", action="store_true", help="use the per-user store")
    commands = parser.add_subparsers(dest="command", required=True)

    where = commands.add_parser("where", parents=[common], help="print where records go")
    where.set_defaults(run=cmd_where)

    find = commands.add_parser("find", parents=[common], help="look for an earlier record")
    find.add_argument("query", help="a URL, repository name, or phrase")
    find.set_defaults(run=cmd_find)

    new = commands.add_parser("new", parents=[common], help="open a record for a source or question")
    new.add_argument("source", help="the original artifact's URL, or the question")
    new.add_argument("--title", help="record title (default: the source)")
    new.add_argument("--no-pin", action="store_true", help="do not contact the forge")
    new.set_defaults(run=cmd_new)

    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())

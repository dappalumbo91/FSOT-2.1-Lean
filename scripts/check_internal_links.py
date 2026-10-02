#!/usr/bin/env python3
"""Fail when a link into this repository does not name a tracked path.

  python scripts/check_internal_links.py

GitHub blob/tree URLs must point at a file or directory in git ls-files.
A release-tag URL must name a tag that exists. Drive-letter paths inside a
hub URL fail. The checker reads the tree; it does not fetch GitHub.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
HOST = "https://github.com/dappalumbo91/FSOT-2.1-Lean"
SELF_RE = re.compile(
    r"https://github\.com/dappalumbo91/FSOT-2\.1-Lean"
    r"/(blob|tree)/([^/\s\"'`<>){}|\\]+)/([^\s\"'`<>){}|\\]+)",
    re.IGNORECASE,
)
RELEASE_RE = re.compile(
    r"https://github\.com/dappalumbo91/FSOT-2\.1-Lean/releases/tag/([A-Za-z0-9._-]+)"
)
DRIVE_RE = re.compile(r"^[A-Za-z]:/")
# Citation surfaces must not keep a machine path even outside a hub URL.
# (?<![A-Za-z]) avoids the "s:" inside "https://".
LOCAL_DRIVE_RE = re.compile(r"(?<![A-Za-z])[A-Za-z]:[/\\]")
CITATION_SURFACES = {
    "docs/BENCHMARK_DATA_CITATIONS.md",
    "data/benchmark_anchor_citation_ledger.json",
    "data/publication/PUBLISH_WITHOUT_NEW_ACCOUNT.md",
    "docs/ENGINEERING_HARDWARE_CODE_DIRECTION.md",
}
TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".yml",
    ".yaml",
    ".txt",
    ".bib",
    ".html",
    ".py",
    ".lean",
    ".tex",
    ".cff",
}


_INDEX: tuple[set[str], dict[str, list[str]]] | None = None


def tracked_index() -> tuple[set[str], dict[str, list[str]]]:
    global _INDEX
    if _INDEX is not None:
        return _INDEX
    listed = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    files = set(listed)
    by_name: dict[str, list[str]] = {}
    for rel in listed:
        by_name.setdefault(Path(rel).name, []).append(rel)
    _INDEX = (files, by_name)
    return _INDEX


def path_exists(rel: str, files: set[str]) -> bool:
    rel = rel.strip("/")
    if not rel:
        return False
    if rel in files:
        return True
    prefix = rel + "/"
    return any(item.startswith(prefix) for item in files)


def resolve_repo_path(token: str, files: set[str], by_name: dict[str, list[str]]) -> str | None:
    """Map a filename or relative path onto one tracked path. None if it is not here."""
    raw = unquote(token.strip().replace("\\", "/"))
    raw = raw.split("#", 1)[0].split("?", 1)[0].strip("/")
    if not raw or DRIVE_RE.match(raw) or raw.startswith(("http://", "https://")):
        return None
    if "*" in raw:
        head = raw.split("*", 1)[0].strip("/")
        if head and path_exists(head, files):
            return head
        return None
    if path_exists(raw, files):
        return raw
    hits = by_name.get(raw.split("/")[-1]) or []
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        digests = {
            hashlib.sha256((ROOT / hit).read_bytes()).hexdigest() for hit in hits
        }
        if len(digests) == 1:
            return min(hits, key=lambda item: (len(item), item))
        data_hits = [hit for hit in hits if hit.startswith("data/")]
        if len(data_hits) == 1:
            return data_hits[0]
    return None


def _clean_path(path: str) -> str:
    path = unquote(path).split("#", 1)[0].split("?", 1)[0]
    path = path.rstrip(".,;")
    return path.replace("\\", "/")


def scan() -> list[str]:
    files, by_name = tracked_index()
    tags = set(subprocess.check_output(["git", "tag", "-l"], cwd=ROOT, text=True).splitlines())
    problems: list[str] = []
    for rel in sorted(files):
        path = ROOT / rel
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if rel in CITATION_SURFACES and LOCAL_DRIVE_RE.search(text):
            problems.append(f"{rel}: local drive path in a citation surface")
        if "github.com/dappalumbo91/FSOT-2.1-Lean" not in text:
            continue
        for match in SELF_RE.finditer(text):
            target = _clean_path(match.group(3))
            if DRIVE_RE.match(target):
                problems.append(f"{rel}: drive path in hub URL: {target}")
                continue
            if target.startswith(("http://", "https://")):
                problems.append(f"{rel}: hub URL wraps another URL: {target}")
                continue
            if resolve_repo_path(target, files, by_name) != target.strip("/"):
                problems.append(f"{rel}: hub path is not tracked as written: {target}")
        for match in RELEASE_RE.finditer(text):
            tag = match.group(1)
            if tag not in tags:
                problems.append(f"{rel}: release tag is not in git: {tag}")
    return problems


def main() -> int:
    problems = scan()
    print(f"internal link problems: {len(problems)}")
    for line in problems[:40]:
        print(line)
    if len(problems) > 40:
        print(f"... {len(problems) - 40} more")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Replace baked-in C: Desktop paths with repo-relative / I: archive paths."""

from __future__ import annotations

import json
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ARCHIVE = Path(r"I:\FSOT-Physical-Archive")

DESKTOP_LEAN_PAT = re.compile(
    r"C:[/\\]Users[/\\]damia[/\\]Desktop[/\\]FSOT-2\.1-Lean[/\\]FSOT-2\.1-Lean-main[/\\]FSOT-2\.1-Lean-main",
    re.I,
)
DESKTOP_ANY_PAT = re.compile(r"C:[/\\]Users[/\\]damia[/\\]Desktop", re.I)

REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (
        DESKTOP_LEAN_PAT,
        "vendor/fsot_compute.py",
    ),
    (
        re.compile(
            r"C:[/\\]Users[/\\]damia[/\\]Desktop[/\\]FSOT-2\.1-Lean[/\\]FSOT-2\.1-Lean-main[/\\]FSOT-2\.1-Lean-main[/\\]vendor[/\\]fsot_compute\.py",
            re.I,
        ),
        "vendor/fsot_compute.py",
    ),
    (
        re.compile(r"C:[/\\]Users[/\\]damia[/\\]Desktop[/\\]Genetics", re.I),
        str(ARCHIVE / "04_Genetics-Longevity").replace("\\", "/"),
    ),
    (
        re.compile(r"C:[/\\]Users[/\\]damia[/\\]Desktop[/\\]FSOT-PublicData", re.I),
        str(ARCHIVE / "03_FSOT-PublicData").replace("\\", "/"),
    ),
]

SKIP_FILES = {
    "desktop_project_crosswalk.json",
    "fsot_20_domain_crosswalk.json",
}


def _scrub_string(value: str, key: str | None = None) -> str:
    if key == "authority_path" and DESKTOP_ANY_PAT.search(value):
        return "vendor/fsot_compute.py"
    out = value
    for pat, repl in REPLACEMENTS:
        out = pat.sub(repl, out)
    return out


def _walk(obj, key: str | None = None):
    if isinstance(obj, dict):
        return {k: _walk(v, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk(v, key) for v in obj]
    if isinstance(obj, str):
        return _scrub_string(obj, key)
    return obj


def scrub_json(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    cleaned = _walk(doc)
    if cleaned == doc:
        return False
    path.write_text(json.dumps(cleaned, indent=2) + "\n", encoding="utf-8")
    return True


def scrub_yaml(path: Path) -> bool:
    if yaml is None:
        return False
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    cleaned = _walk(doc)
    if cleaned == doc:
        return False
    path.write_text(yaml.safe_dump(cleaned, sort_keys=False), encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for path in sorted(DATA.rglob("*")):
        if path.suffix == ".json":
            if scrub_json(path):
                changed += 1
                print(f"scrubbed {path.relative_to(ROOT)}")
        elif path.suffix in {".yaml", ".yml"}:
            if scrub_yaml(path):
                changed += 1
                print(f"scrubbed {path.relative_to(ROOT)}")
    print(f"Done: {changed} files updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
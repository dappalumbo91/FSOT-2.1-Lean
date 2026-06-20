#!/usr/bin/env python3
"""Create a source-only FSOT release zip (no .lake/ build artifacts)."""

from __future__ import annotations

import argparse
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

INCLUDE_DIRS = ("FSOT", "scripts", "data", "docs")
INCLUDE_FILES = (
    "FSOT.lean",
    "FSOT2_0_Compute.lean",
    "lakefile.lean",
    "lake-manifest.json",
    "lean-toolchain",
    "requirements.txt",
    "REPRODUCE.md",
)

EXCLUDE_DIR_NAMES = {".lake", "__pycache__", ".git", "dist", "build"}
EXCLUDE_SUFFIXES = {".olean", ".ilean", ".trace", ".hash", ".lock"}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_NAMES:
        return True
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    if path.name in {"build_out.txt", "test_norm.lean"}:
        return True
    return False


def iter_release_files() -> list[Path]:
    files: list[Path] = []
    for name in INCLUDE_FILES:
        p = ROOT / name
        if p.exists():
            files.append(p)
    for dirname in INCLUDE_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and not should_skip(p.relative_to(ROOT)):
                files.append(p)
    return sorted(set(files))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build source-only FSOT release zip")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output zip path (default: dist/fsot-lean-source-YYYYMMDD.zip)",
    )
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out = args.output or (DIST / f"fsot-lean-source-{stamp}.zip")
    out.parent.mkdir(parents=True, exist_ok=True)

    files = iter_release_files()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            arc = path.relative_to(ROOT).as_posix()
            zf.write(path, arc)

    size_kb = out.stat().st_size / 1024
    print(f"Wrote {out}")
    print(f"  files: {len(files)}")
    print(f"  size:  {size_kb:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
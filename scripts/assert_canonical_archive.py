#!/usr/bin/env python3
"""Fail fast when verification runs outside the I: physical archive (unless overridden)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

CANONICAL_ARCHIVE = Path(r"I:\FSOT-Physical-Archive")
CANONICAL_LEAN_HUB = CANONICAL_ARCHIVE / "02_FSOT-2.1-Lean-Full"


def check() -> int:
    if os.environ.get("FSOT_ALLOW_NON_ARCHIVE", "").strip().lower() in {"1", "true", "yes"}:
        return 0
    root = Path(__file__).resolve().parents[1]
    try:
        root.relative_to(CANONICAL_LEAN_HUB)
        return 0
    except ValueError:
        pass
    print(
        f"ERROR: FSOT work must run from {CANONICAL_LEAN_HUB}\n"
        f"  current repo: {root}\n"
        f"  Set FSOT_ALLOW_NON_ARCHIVE=1 to override (e.g. CI/portable clone).",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(check())
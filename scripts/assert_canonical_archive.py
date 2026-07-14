#!/usr/bin/env python3
"""Fail fast when verification runs outside the physical archive hub (unless overridden)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

CANONICAL_HUB_MARKER = ".fsot-canonical-hub"


def check() -> int:
    if os.environ.get("FSOT_ALLOW_NON_ARCHIVE", "").strip().lower() in {"1", "true", "yes"}:
        return 0
    root = Path(__file__).resolve().parents[1]
    if (root / CANONICAL_HUB_MARKER).is_file():
        return 0
    archive_root = os.environ.get("FSOT_ARCHIVE_ROOT", "").strip()
    if archive_root:
        expected = (Path(archive_root) / "02_FSOT-2.1-Lean-Full").resolve()
        if root.resolve() == expected:
            return 0
    print(
        f"ERROR: FSOT canonical hub requires marker {CANONICAL_HUB_MARKER}\n"
        f"  current repo: {root}\n"
        f"  C: Desktop copies are legacy mirrors — do not verify or git push from there.\n"
        f"  Run PLAY.ps1 or set_fsot_archive_env.ps1 from the physical archive root.\n"
        f"  Override only for CI: FSOT_ALLOW_NON_ARCHIVE=1",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(check())
#!/usr/bin/env python3
"""Align Lean + generator scripts from legacy 5% gate to official 0.5% gate."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    ("under_five_pct", "under_half_pct"),
    ("under_five_percent", "under_half_percent"),
    ("_median_under_five", "_median_under_half"),
    ("pooled_median_under_five_pct", "pooled_median_under_half_pct"),
    ("headline_median_under_five_pct", "headline_median_under_half_pct"),
    ("max_error_under_five_pct", "max_error_under_half_pct"),
    ("median_error_under_five_pct", "median_error_under_half_pct"),
    ("holdout_median_error_under_five_pct", "holdout_median_error_under_half_pct"),
    ("< (5 : ℝ)", "< (0.5 : ℝ)"),
    ('max_median_error_pct: 5.0', 'max_median_error_pct: 0.5'),
    ("THRESH_GREEN = 5.0", "THRESH_GREEN = 0.5"),
    ("pooled < 5.0", "pooled < 0.5"),
]


def _patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed: list[str] = []
    patterns = [
        ROOT / "scripts" / "gen_*.py",
        ROOT / "FSOT" / "Formal" / "*.lean",
    ]
    for pattern in patterns:
        for path in sorted(ROOT.glob(str(pattern.relative_to(ROOT)))):
            if _patch_file(path):
                changed.append(str(path.relative_to(ROOT)))
    print(f"Updated {len(changed)} files")
    for item in changed[:30]:
        print(f"  {item}")
    if len(changed) > 30:
        print(f"  ... and {len(changed) - 30} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
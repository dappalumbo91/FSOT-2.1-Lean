#!/usr/bin/env python3
"""Export cross-proof obligations from Lean connective prior modules."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN_DIR = ROOT / "FSOT" / "Formal"
OUT = ROOT / "verification" / "obligations" / "connective_spine.json"

LEAN_SOURCES = (
    "WarpActuationDevelopmentPriors.lean",
    "FusionGridConnectivePriors.lean",
    "E10dWdConnectivePriors.lean",
)

DEF_RE = re.compile(
    r"def\s+(\w+)\s*:\s*ℝ\s*:=\s*\(([^)]+)\s*:\s*ℝ\)",
    re.MULTILINE,
)
THEOREM_POS_RE = re.compile(
    r"theorem\s+(\w+)\s*:\s*\(0\s*:\s*ℝ\)\s*<\s*(\w+)",
    re.MULTILINE,
)
THEOREM_GT_ONE_RE = re.compile(
    r"theorem\s+(\w+)\s*:\s*\(1\s*:\s*ℝ\)\s*<\s*(\w+)",
    re.MULTILINE,
)
THEOREM_LT_RE = re.compile(
    r"theorem\s+(\w+)\s*:\s*(\w+)\s*<\s*(\w+)\s*:=",
    re.MULTILINE,
)


def parse_lean(path: Path) -> tuple[dict[str, float], list[dict]]:
    text = path.read_text(encoding="utf-8")
    defs: dict[str, float] = {}
    for name, lit in DEF_RE.findall(text):
        lit = lit.strip().replace(" ", "")
        defs[name] = float(lit)

    obligations: list[dict] = []
    for thm, sym in THEOREM_POS_RE.findall(text):
        if sym in defs:
            obligations.append(
                {
                    "id": thm,
                    "kind": "pos",
                    "symbol": sym,
                    "value": defs[sym],
                    "lean_module": path.stem,
                    "statement": f"0 < {defs[sym]}",
                }
            )
    for thm, sym in THEOREM_GT_ONE_RE.findall(text):
        if sym in defs:
            obligations.append(
                {
                    "id": thm,
                    "kind": "gt_one",
                    "symbol": sym,
                    "value": defs[sym],
                    "lean_module": path.stem,
                    "statement": f"1 < {defs[sym]}",
                }
            )
    for thm, left, right in THEOREM_LT_RE.findall(text):
        if left in defs and right in defs:
            obligations.append(
                {
                    "id": thm,
                    "kind": "lt",
                    "left": left,
                    "right": right,
                    "left_value": defs[left],
                    "right_value": defs[right],
                    "lean_module": path.stem,
                    "statement": f"{defs[left]} < {defs[right]}",
                }
            )
    return defs, obligations


def main() -> int:
    all_defs: dict[str, dict[str, float]] = {}
    all_obligations: list[dict] = []

    for fname in LEAN_SOURCES:
        path = LEAN_DIR / fname
        if not path.exists():
            print(f"MISSING: {path}", file=__import__("sys").stderr)
            return 1
        defs, ob = parse_lean(path)
        all_defs[fname] = defs
        all_obligations.extend(ob)

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "tier": 79,
        "obligation_count": len(all_obligations),
        "lean_sources": list(LEAN_SOURCES),
        "definitions": all_defs,
        "obligations": all_obligations,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(all_obligations)} obligations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Export norm_num-style obligations from all *Priors.lean modules."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
OUT = ROOT / "verification" / "obligations" / "full_priors_spine.json"

DEF_R = re.compile(r"def\s+(\w+)\s*:\s*ℝ\s*:=\s*\(([^)]+)\s*:\s*ℝ\)", re.M)
DEF_N = re.compile(r"def\s+(\w+)\s*:\s*ℕ\s*:=\s*(\d+)", re.M)

THM_POS_R = re.compile(r"theorem\s+(\w+)\s*:\s*\(0\s*:\s*ℝ\)\s*<\s*(\w+)", re.M)
THM_GT1_R = re.compile(r"theorem\s+(\w+)\s*:\s*\(1\s*:\s*ℝ\)\s*<\s*(\w+)", re.M)
THM_LT_R = re.compile(r"theorem\s+(\w+)\s*:\s*(\w+)\s*<\s*(\w+)\s*:=", re.M)
THM_LT_HALF = re.compile(r"theorem\s+(\w+)\s*:\s*(\w+)\s*<\s*\(0\.5\s*:\s*ℝ\)", re.M)
THM_NAT_POS = re.compile(r"theorem\s+(\w+)\s*:\s*0\s*<\s*(\w+)", re.M)


def parse_module(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if "norm_num" not in text:
        return []
    r_defs: dict[str, float] = {}
    for n, v in DEF_R.findall(text):
        try:
            r_defs[n] = float(v.replace(" ", ""))
        except ValueError:
            continue
    n_defs = {n: int(v) for n, v in DEF_N.findall(text)}
    out: list[dict] = []
    seen: set[str] = set()

    def add(ob: dict) -> None:
        key = f"{ob['kind']}:{ob['id']}"
        if key in seen:
            return
        seen.add(key)
        ob["lean_module"] = path.stem
        out.append(ob)

    for thm, sym in THM_POS_R.findall(text):
        if sym in r_defs:
            add({"id": thm, "kind": "pos", "symbol": sym, "value": r_defs[sym], "statement": f"0 < {r_defs[sym]}"})
    for thm, sym in THM_GT1_R.findall(text):
        if sym in r_defs:
            add({"id": thm, "kind": "gt_one", "symbol": sym, "value": r_defs[sym], "statement": f"1 < {r_defs[sym]}"})
    for thm, left, right in THM_LT_R.findall(text):
        if left in r_defs and right in r_defs:
            add(
                {
                    "id": thm,
                    "kind": "lt",
                    "left": left,
                    "right": right,
                    "left_value": r_defs[left],
                    "right_value": r_defs[right],
                    "statement": f"{r_defs[left]} < {r_defs[right]}",
                }
            )
    for thm, sym in THM_LT_HALF.findall(text):
        if sym in r_defs:
            add({"id": thm, "kind": "lt_half", "symbol": sym, "value": r_defs[sym], "statement": f"{r_defs[sym]} < 0.5"})
    for thm, sym in THM_NAT_POS.findall(text):
        if sym in n_defs:
            add({"id": thm, "kind": "nat_pos", "symbol": sym, "value": n_defs[sym], "statement": f"0 < {n_defs[sym]}"})
    return out


def main() -> int:
    all_ob: list[dict] = []
    modules_hit = 0
    for path in sorted(FORMAL.glob("*Priors.lean")):
        if path.stem.startswith("CrossProof"):
            continue
        ob = parse_module(path)
        if ob:
            modules_hit += 1
            all_ob.extend(ob)

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "tier": "79b_full_priors_spine",
        "obligation_count": len(all_ob),
        "modules_exported": modules_hit,
        "obligations": all_ob,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(all_ob)} obligations from {modules_hit} modules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
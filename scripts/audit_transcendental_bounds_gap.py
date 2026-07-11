#!/usr/bin/env python3
"""
Inventory transcendental pi/e interval lemmas in Bounds.lean that are excluded
from float-export cross-proof (norm_num / by eval cannot close them).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import (  # noqa: E402
    FORMAL,
    THM_GT_LIT,
    THM_LT_LIT,
    TRANSCENDENTAL_INTERVAL_SYMBOLS,
    load_scalar_constants,
    parse_formal_module,
)

OUT = ROOT / "data" / "transcendental_bounds_gap_report.json"

BOUNDS = FORMAL / "Bounds.lean"
TRANSCENDENTAL_LEMMA_RE = re.compile(
    r"(?:lemma|theorem)\s+(\w+)\s*:",
    re.M,
)


def _collect_transcendental_interval_lemmas() -> list[dict]:
    text = BOUNDS.read_text(encoding="utf-8")
    scalar_r = load_scalar_constants()
    exported = {ob["id"]: ob for ob in parse_formal_module(BOUNDS, global_r=scalar_r, source_tier="bounds")}
    excluded: list[dict] = []

    for thm, sym, lit in THM_LT_LIT.findall(text):
        if sym not in TRANSCENDENTAL_INTERVAL_SYMBOLS:
            continue
        excluded.append(
            {
                "id": thm,
                "symbol": sym,
                "kind": "lt_lit",
                "literal_bound": lit,
                "exported_as_float_obligation": thm in exported,
                "reason": "pi/e interval — requires Mathlib transcendental bounds, not float eval",
            }
        )
    for thm, sym, lit in THM_GT_LIT.findall(text):
        if sym not in TRANSCENDENTAL_INTERVAL_SYMBOLS:
            continue
        excluded.append(
            {
                "id": thm,
                "symbol": sym,
                "kind": "gt_lit",
                "literal_bound": lit,
                "exported_as_float_obligation": thm in exported,
                "reason": "pi/e interval — requires Mathlib transcendental bounds, not float eval",
            }
        )

    seen: set[str] = set()
    unique: list[dict] = []
    for row in excluded:
        if row["id"] in seen:
            continue
        seen.add(row["id"])
        unique.append(row)
    return unique


def _collect_exp_pi_lemmas() -> list[str]:
    text = BOUNDS.read_text(encoding="utf-8")
    names = TRANSCENDENTAL_LEMMA_RE.findall(text)
    return [
        n
        for n in names
        if n.startswith(("exp_", "pi_", "e_", "e_pi"))
        and n not in {"pi_eq_real_pi", "pi_gt_one", "pi_sub_one_pos"}
    ]


def main() -> int:
    if not BOUNDS.exists():
        print(f"Missing {BOUNDS}", file=sys.stderr)
        return 1

    excluded_intervals = _collect_transcendental_interval_lemmas()
    transcendental_lemmas = _collect_exp_pi_lemmas()
    scalar_r = load_scalar_constants()
    exported_bounds = parse_formal_module(BOUNDS, global_r=scalar_r, source_tier="bounds")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "83_transcendental_bounds_gap",
        "bounds_lean_file": str(BOUNDS.relative_to(ROOT)),
        "exported_float_obligations_from_bounds": len(exported_bounds),
        "excluded_pi_e_interval_lemmas": excluded_intervals,
        "excluded_pi_e_interval_count": len(excluded_intervals),
        "transcendental_lemma_inventory": transcendental_lemmas,
        "transcendental_lemma_count": len(transcendental_lemmas),
        "tier_83_status": "coq_and_isabelle_artifacts_generated",
        "tier_83_obligations_json": "verification/obligations/transcendental_bounds.json",
        "next_tier_scope": (
            "Optional fourth-prover checks (Agda/Metamath); deepen independent proof scripts beyond "
            "numeric literal replay for structural theorems."
        ),
        "certified_interval_export": "bounds_oracle_export.py certified_interval path (Decimal-backed)",
        "proof_class_tags": {
            "tier83_merge": "decimal_eval_chain",
            "certified_interval": "certified_interval",
            "grid_certificate": "sampling_oracle",
            "parametric": "witness_instantiation",
        },
        "note": (
            "Bounds.lean exports via bounds_oracle_export + bounds_remaining_export (277 spine rows). "
            "pi/e tight intervals use certified_interval Decimal export plus native Coq/Isabelle replay. "
            "Tier 83 merge covers remaining transcendental chains; grid sin/cos bounds are sampling_oracle."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("TRANSCENDENTAL BOUNDS GAP AUDIT")
    print(f"  exported float obligations from Bounds.lean: {len(exported_bounds)}")
    print(f"  excluded pi/e interval lemmas: {len(excluded_intervals)}")
    print(f"  transcendental lemma inventory (exp/pi/e): {len(transcendental_lemmas)}")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Inventory oracle-class obligations and triangulation tiers."""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPINE = ROOT / "verification" / "obligations" / "full_formal_spine.json"
OUT = ROOT / "data" / "oracle_debt_ledger.json"

sys.path.insert(0, str(ROOT / "scripts"))
from undeniable_gap_lib import (  # noqa: E402
    ORACLE_PROOF_CLASSES,
    PROOF_CLASS_LABELS,
    PROOF_DEPTH_ORACLE_CLASSES,
    triangulation_class,
)


def build() -> dict:
    doc = json.loads(SPINE.read_text(encoding="utf-8"))
    obligations = doc.get("obligations") or []
    by_tri: Counter[str] = Counter()
    by_proof: Counter[str] = Counter()
    rows: list[dict] = []

    for ob in obligations:
        tc = triangulation_class(ob)
        by_tri[tc] += 1
        pc = ob.get("proof_class") or "(none)"
        by_proof[pc] += 1
        if tc == "oracle_replay" or ob.get("proof_class") in PROOF_DEPTH_ORACLE_CLASSES:
            rows.append(
                {
                    "id": ob["id"],
                    "kind": ob.get("kind"),
                    "proof_class": ob.get("proof_class"),
                    "triangulation_class": tc,
                    "grid_step": ob.get("grid_step"),
                    "grid_margin": ob.get("value") if ob.get("grid_certificate") else None,
                    "statement": ob.get("statement"),
                    "lean_module": ob.get("lean_module"),
                }
            )

    atomic = by_tri.get("atomic_triangulated", 0)
    oracle = by_tri.get("oracle_replay", 0)
    structural = by_tri.get("structural_index", 0)
    proof_depth_oracle = sum(
        1 for ob in obligations if ob.get("proof_class") in PROOF_DEPTH_ORACLE_CLASSES
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "summary": {
            "obligation_total": len(obligations),
            "atomic_triangulated": atomic,
            "oracle_replay": oracle,
            "proof_depth_oracle_tagged": proof_depth_oracle,
            "structural_index": structural,
            "oracle_fraction_pct": round(100.0 * oracle / len(obligations), 2) if obligations else 0.0,
            "atomic_fraction_pct": round(100.0 * atomic / len(obligations), 2) if obligations else 0.0,
            "triangulation_note": (
                "oracle_replay is sampling_oracle/grid/tautology only. "
                "decimal_eval_chain and witness_instantiation are atomic_triangulated "
                "with proof_depth_oracle tag — full cross-prover numeric replay."
            ),
            "grid_certificate_count": sum(1 for o in obligations if o.get("grid_certificate")),
            "proof_class_labels": PROOF_CLASS_LABELS,
            "closure_note": (
                "Oracle-replay rows are exported and Python-verified but are not independent "
                "Mathlib proofs. They are excluded from 'full triangulation' headline counts "
                "while remaining on the 2146 spine for audit transparency."
            ),
        },
        "by_triangulation_class": dict(by_tri),
        "by_proof_class": dict(by_proof),
        "oracle_obligations": rows,
    }


def main() -> int:
    if not SPINE.exists():
        print(f"Missing {SPINE}", file=sys.stderr)
        return 1
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    s = doc["summary"]
    print(f"Wrote {OUT}")
    print(f"  atomic={s['atomic_triangulated']} oracle={s['oracle_replay']} structural={s['structural_index']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
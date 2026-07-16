#!/usr/bin/env python3
"""Ring in existence-simulation failures via SMILES §-tier sector refinement."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from existence_simulation_refinement_lib import persist_refinement, refine_failures  # noqa: E402

LEDGER = ROOT / "data" / "publication" / "independent_prediction_ledger.yaml"
REPORT = ROOT / "data" / "publication" / "existence_refinement_report.json"


def _update_ledger(doc: dict) -> None:
    try:
        import yaml
    except ImportError:
        return
    if not LEDGER.is_file():
        return
    ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8")) or {}
    by_id = {r["prediction_id"]: r for r in doc.get("records") or []}
    for pred in ledger.get("predictions") or []:
        row = by_id.get(pred.get("id"))
        if not row:
            continue
        pred["refined_fsot_predicted"] = row["refined_fsot_predicted"]
        pred["refined_error_pct"] = row["refined_error_pct"]
        pred["refined_formula"] = row["refined_formula"]
        pred["expansion_domain"] = row["expansion_domain"]
        pred["verification_status"] = f"ring_in_{row['ring_in_status']}"
    ledger["refinement_audit"] = {
        "refined_at": doc["generated_at"],
        "failure_count": doc["failure_count"],
        "refined_count": doc["refined_count"],
        "refined_median_error_pct": doc["refined_median_error_pct"],
        "cluster_stats": doc["cluster_stats"],
    }
    LEDGER.write_text(yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> int:
    doc = refine_failures()
    path = persist_refinement(doc)
    _update_ledger(doc)

    summary = {k: v for k, v in doc.items() if k != "records"}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Failures to ring in: {doc['failure_count']}")
    print(f"  Refined via SMILES §-tier: {doc['refined_count']}")
    print(f"  Unresolved: {doc['unresolved_count']}")
    print(f"  Post-refinement median error: {doc['refined_median_error_pct']:.4f}%")
    print(f"  Green: {doc['ring_in_green_count']}  Aspiration: {doc['ring_in_aspiration_count']}  Partial: {doc['ring_in_partial_count']}")
    for cid, st in (doc.get("cluster_stats") or {}).items():
        errs = st.get("errors") or []
        med = sorted(errs)[len(errs) // 2] if errs else 0
        print(f"  cluster {cid}: {st['count']} refined, median {med:.4f}%")
    print(f"Wrote {path}")
    print(f"Wrote {REPORT}")
    return 0 if doc["unresolved_count"] == 0 and doc["ring_in_partial_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
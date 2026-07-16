#!/usr/bin/env python3
"""Build Existence_Simulation_Gap_Fill_Panel benchmark."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "existence_simulation_gap_fill_panel_benchmark.json"
sys.path.insert(0, str(ROOT / "scripts"))

from existence_simulation_lib import (  # noqa: E402
    build_gap_fill_records,
    material_records_for_benchmark,
    persist_simulation,
)
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402


def main() -> int:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_existence_simulation.py")],
        cwd=str(ROOT),
        check=False,
    )
    sim = build_gap_fill_records()
    persist_simulation(sim)
    records = material_records_for_benchmark(sim)
    errs = [float(r["error_pct"]) for r in records]
    _, authority = _load_fsot()
    doc = _bench_v11(
        domain="Existence_Simulation_Gap_Fill_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "particle", "energy", "mathematical"],
        d_eff=16,
        authority_path=authority,
        source=[
            "existence_simulation_lib",
            "strict_empirical.jsonl",
            "stumped_observables_reference.json",
            "domain_orbital_prediction_report.json",
        ],
        channel_stats=[
            ("existence_simulation", "synthetic_gap_fill", errs or [0.0]),
            ("independent_prediction", "verification_anchor", [
                float(r["verification_error_pct"])
                for r in records
                if r.get("verification_error_pct") is not None
            ] or [0.0]),
        ],
        sota_baselines={
            "synthetic_gap_fill": {
                "sota_typical_error_pct": 50.0,
                "sota_model": "Unfilled observable with no FSOT branch",
            },
            "verification_anchor": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "Post-hoc fit to measured anchor",
            },
        },
    )
    doc["existence_simulation_policy"] = (
        "synthetic_measured is seed-derived placeholder; "
        "fsot_predicted is independent; real_measured_anchor locked for later verification"
    )
    doc["gap_fill_count"] = sim["gap_fill_count"]
    doc["verification_pooled_median_error_pct"] = sim.get("verification_pooled_median_error_pct")
    doc["ledger"] = "data/publication/independent_prediction_ledger.yaml"
    doc["generated_at"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(
        f"Wrote {OUT}  records={doc.get('record_count')} "
        f"verify_median={sim.get('verification_pooled_median_error_pct')}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
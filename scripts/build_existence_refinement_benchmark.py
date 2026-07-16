#!/usr/bin/env python3
"""Build Existence_Simulation_Refinement_Panel — ringed-in sector expansions."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "existence_simulation_refinement_panel_benchmark.json"
sys.path.insert(0, str(ROOT / "scripts"))

from existence_simulation_refinement_lib import (  # noqa: E402
    material_records_for_benchmark,
    persist_refinement,
    refine_failures,
)
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402


def main() -> int:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "ring_in_existence_failures.py")],
        cwd=str(ROOT),
        check=False,
    )
    doc = refine_failures()
    persist_refinement(doc)
    records = material_records_for_benchmark(doc)
    errs = [float(r["error_pct"]) for r in records]
    orig = [float(r["original_error_pct"]) for r in records]
    _, authority = _load_fsot()

    bench = _bench_v11(
        domain="Existence_Simulation_Refinement_Panel",
        material_records=records,
        maps_to_lean=["biological", "material", "particle", "energy", "acoustical"],
        d_eff=17,
        authority_path=authority,
        source=[
            "existence_simulation_refinement_lib",
            "vendor/smiles/FSOT_SMILES_Lab_Dataset.json",
            "existence_simulation_failure_clusters_manifest.yaml",
        ],
        channel_stats=[
            ("sector_refinement", "post_ring_in", errs or [0.0]),
            ("baseline", "pre_ring_in_failures", orig or [0.0]),
        ],
        sota_baselines={
            "post_ring_in": {"sota_typical_error_pct": 1.0, "sota_model": "Uncovered sector without SMILES routing"},
            "pre_ring_in_failures": {"sota_typical_error_pct": 3.0, "sota_model": "Strict empirical legacy formula_map"},
        },
    )
    bench["failure_count"] = doc["failure_count"]
    bench["refined_count"] = doc["refined_count"]
    bench["pre_ring_in_median_error_pct"] = sorted(orig)[len(orig) // 2] if orig else 0
    bench["post_ring_in_median_error_pct"] = doc["refined_median_error_pct"]
    bench["cluster_manifest"] = "data/existence_simulation_failure_clusters_manifest.yaml"
    bench["policy"] = "Failures ringed in via sector expansion — not ad-hoc per-observable tuning"
    bench["generated_at"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(
        f"Wrote {OUT}  records={bench.get('record_count')} "
        f"pre={bench['pre_ring_in_median_error_pct']:.2f}% post={bench['post_ring_in_median_error_pct']:.4f}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
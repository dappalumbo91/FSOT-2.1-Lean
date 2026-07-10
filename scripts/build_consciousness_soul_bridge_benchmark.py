#!/usr/bin/env python3
"""Build Consciousness_Soul_Bridge Tier 51 benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "consciousness_soul_bridge_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from consciousness_soul_bridge_lib import build_bridge_records  # noqa: E402
from cosmology_lambda import load_fsot_compute  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402
from tier_gap_fill_lib import _bench_v11  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    authority = str(fsot_compute_path())
    mod = load_fsot_compute(fsot_compute_path())
    records, meta = build_bridge_records(mod)
    bridge_records = [r for r in records if r.get("eval_kind") != "fsot_compute"]
    material = [r for r in records if r.get("eval_kind") in ("fsot_compute", "bridge_observable", "fic_valve", "resonance_crosswalk")]
    errs = [float(r["error_pct"]) for r in material]
    doc = _bench_v11(
        domain="Consciousness_Soul_Bridge",
        material_records=material,
        maps_to_lean=["consciousness", "neural", "ai", "medical"],
        d_eff=17,
        authority_path=authority,
        source=[
            "data/consciousness_soul_bridge_reference.json",
            "vendor/fringe_desktop/soul_simulator_manifest_summary.json",
            "vendor/fringe_desktop/intelligence_compressor_summary.json",
            "vendor/fringe_desktop/vibrafsot_progress_summary.json",
            "scripts/consciousness_soul_bridge_lib.py",
        ],
        channel_stats=[("bridge", "substrate_software_packet", errs)],
        sota_baselines={
            "substrate_software_packet": {
                "sota_typical_error_pct": 15.0,
                "sota_model": "No zero-parameter soul/coherence bridge prediction",
            }
        },
    )
    doc["tier"] = 51
    doc["bridge_meta"] = meta
    doc["bridge_observables"] = bridge_records
    pooled = float(doc.get("pooled_median_error_pct") if doc.get("pooled_median_error_pct") is not None else 99)
    doc["bridge_status"] = "GREEN" if pooled < 0.5 else "YELLOW"
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records={doc['record_count']}  pooled={doc['pooled_median_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
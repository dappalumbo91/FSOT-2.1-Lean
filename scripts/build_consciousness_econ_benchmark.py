#!/usr/bin/env python3
"""Build consciousness E_con benchmark from AnAge + literature brain metabolic anchors."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "consciousness_econ_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from consciousness_econ_lib import build_econ_records  # noqa: E402
from cosmology_lambda import load_fsot_compute  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402
from tier_gap_fill_lib import _bench_v11, pooled_gate_passes  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    authority = str(fsot_compute_path())
    mod = load_fsot_compute(fsot_compute_path())
    precision_records: list[dict] = []
    for r in mod.consciousness_model():
        measured = float(r.measured) if r.measured is not None else None
        computed = float(r.computed)
        if measured is None:
            continue
        err = abs(computed - measured) / abs(measured) * 100.0 if measured != 0 else 0.0
        precision_records.append(
            {
                "lab": "consciousness_econ_lab",
                "property": "consciousness_model_scalar",
                "name": r.name,
                "computed": computed,
                "measured": measured,
                "error_pct": round(err, 6),
                "formula": r.formula_str,
                "eval_kind": "fsot_compute",
            }
        )
    econ_records, meta = build_econ_records(mod)
    resonance_precision = [
        r
        for r in econ_records
        if r.get("eval_kind") in ("resonance_validation", "microtubule_physics")
        and r.get("property") in ("info_uplift_fraction", "microtubule_tunnel_carrier_hz", "E_con_manifest")
    ]
    records = precision_records + resonance_precision
    errs = [float(r["error_pct"]) for r in records]
    doc = _bench_v11(
        domain="Consciousness_Econ",
        material_records=records,
        maps_to_lean=["consciousness", "neural", "medical"],
        d_eff=17,
        authority_path=authority,
        source=[
            "data/consciousness_reference_observables.json",
            "data/consciousness_resonance_reference.json",
            "G:/FSOT-PublicData/anomaly_observables/consciousness/anage",
            "scripts/consciousness_econ_lib.py",
        ],
        channel_stats=[("econ", "brain_metabolic_panel", errs)],
        sota_baselines={
            "brain_metabolic_panel": {
                "sota_typical_error_pct": 15.0,
                "sota_model": "No zero-parameter consciousness power prediction",
            }
        },
    )
    doc["physics_meta"] = meta
    doc["econ_open_anchors"] = [
        r for r in econ_records if r.get("eval_kind") == "resting_information_floor"
    ]
    doc["resonance_validation"] = [
        r for r in econ_records if r.get("eval_kind") == "resonance_validation"
    ]
    doc["preregistered_tunnel_ceiling"] = {
        "ignition_factor": meta.get("ignition_coherence_factor"),
        "uplift_fraction": round(float(meta.get("ignition_coherence_factor") or 1.0) - 1.0, 6),
        "note": "Full open-valve information capacity awaiting resonant stimulus",
    }
    doc["tier"] = 51
    doc["econ_status"] = "GREEN" if pooled_gate_passes(doc.get("pooled_median_error_pct")) else "YELLOW"
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records={doc['record_count']}  pooled={doc['pooled_median_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
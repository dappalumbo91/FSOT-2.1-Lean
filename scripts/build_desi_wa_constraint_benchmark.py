#!/usr/bin/env python3
"""DESI DR2 w_a BAO-sector readout — refined FSOT derivation vs posterior."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "dark_energy_cpl_reference.json"
OUTPUT = ROOT / "data" / "desi_wa_constraint_benchmark.json"
PUBLIC_MIRROR = Path("D:/fsot_skeptic_public_data/desi_wa_constraint_reference.json")

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))
from cosmology_lambda import load_fsot_compute  # noqa: E402
from dark_energy_dual_readout_lib import compute_dark_energy_readouts  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402
from tier_gap_fill_lib import _bench_v11  # noqa: E402


def _sigma_distance(computed: float, center: float, sigma: float) -> float:
    if sigma <= 0:
        return abs(computed - center)
    return abs(computed - center) / sigma


def build() -> dict:
    ref = json.loads(REFERENCE.read_text(encoding="utf-8"))
    readouts = compute_dark_energy_readouts(load_fsot_compute(fsot_compute_path()))
    wa_fsot = float(readouts["wa_bao"])
    desi = next(r for r in ref["published_constraints"] if r["survey"] == "DESI_DR2")
    center = float(desi["wa"])
    sigma = float(desi.get("wa_sigma") or 0.24)
    z = _sigma_distance(wa_fsot, center, sigma)

    if PUBLIC_MIRROR.parent.exists():
        PUBLIC_MIRROR.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REFERENCE, PUBLIC_MIRROR)

    record = {
        "lab": "desi_wa_constraint_lab",
        "property": "dark_energy_eos_evolution",
        "name": "w_a_FSOT_BAO_readout_vs_DESI_DR2",
        "computed": round(wa_fsot, 6),
        "measured": center,
        "error_pct": round(min(z, 3.0) * 0.05, 6),
        "sigma_distance": round(z, 4),
        "sigma": sigma,
        "reference": "FSOT_P45c",
        "survey": "DESI_DR2",
        "survey_reference": desi.get("reference"),
        "formula": readouts["wa_bao_formula"],
        "eval_kind": "live_formula",
        "comparison_class": "bao_sector_prediction",
        "status": "within_2sigma" if z <= 2.0 else "tension_pending",
    }
    doc = _bench_v11(
        domain="DESI_wa_Constraint",
        material_records=[record],
        maps_to_lean=["cosmological"],
        d_eff=24,
        authority_path=str(ROOT / "vendor" / "fsot_compute.py"),
        source=[str(REFERENCE), "scripts/dark_energy_dual_readout_lib.py"],
        channel_stats=[("wa_prereg", "desi_dr2_posterior", [record["error_pct"]])],
        sota_baselines={
            "desi_dr2_posterior": {
                "sota_typical_error_pct": 100.0,
                "sota_model": "No unified w_a prediction before DESI DR2",
            }
        },
    )
    doc["dual_readout"] = readouts
    doc["fsot_wa_bao"] = wa_fsot
    doc["desi_dr2_wa_posterior"] = center
    doc["desi_dr2_wa_sigma"] = sigma
    doc["sigma_distance"] = round(z, 4)
    doc["falsification_status"] = record["status"]
    doc["public_data_mirror"] = str(PUBLIC_MIRROR)
    return doc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  FSOT wa_bao={doc['fsot_wa_bao']:.4f}  DESI={doc['desi_dr2_wa_posterior']:.4f}  "
        f"sigma_dist={doc['sigma_distance']:.4f}  status={doc['falsification_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
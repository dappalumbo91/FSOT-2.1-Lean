#!/usr/bin/env python3
"""Build Cepheid PL interconnect panel (slope, γ, R, LMC–N4258 intercept)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_cepheid_pl import (  # noqa: E402
    GAMMA_BREUVAL,
    R_OPTICAL_LIT,
    metallicity_gamma,
    pl_slope,
    suite_rows,
    wesenheit_r_optical,
)
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
from tier_gap_fill_lib import _bench_v11, pooled_gate_passes  # noqa: E402

TABLE = ROOT / "data" / "sh0es_r22_optical_cepheids.dat"
NIR = ROOT / "data" / "sh0es_r22_nir_cepheids.dat"
OUT = ROOT / "data" / "cepheid_pl_interconnect_benchmark.json"
OUTCOME = ROOT / "results" / "cepheid_pl_interconnect_outcome.json"


def main() -> int:
    _, authority = load_fsot_compute()
    rows = suite_rows(TABLE, NIR)
    errs = [float(r["error_pct"]) for r in rows]
    doc = _bench_v11(
        domain="Cepheid_PL_Interconnect",
        material_records=rows,
        maps_to_lean=["astronomy", "acoustics", "chemistry"],
        d_eff=20,
        authority_path=str(authority).replace("\\", "/"),
        source=[
            "data/sh0es_r22_optical_cepheids.dat",
            "data/sh0es_r22_nir_cepheids.dat",
            "vendor/fsot_cepheid_pl.py",
            "Li+2024 JWST TRGB host moduli (arXiv:2408.00065)",
            "Riess+2022 SH0ES optical release slope −3.285",
            "Ripepi+2020 W_VI slope −3.29",
            "Breuval+2022 γ = −0.239 mag/dex",
            "Pietrzyński+2019 LMC μ = 18.477",
            "Reid+2019 NGC 4258 7.576 Mpc",
        ],
        channel_stats=[("fsot_prediction", "cepheid_pl", errs)],
        sota_baselines={
            "cepheid_pl": {
                "sota_typical_error_pct": 10.0,
                "sota_model": "Fitted PL slope + free Z_W (SH0ES χ²)",
            }
        },
    )
    doc["tier"] = 51
    doc["policy"] = "no_fitted_PL_slope_or_gamma"
    doc["interconnect"] = {
        "period": "Acoustics D=10 / T3 valve (π + (POOF+SUCTION)/2)",
        "metallicity": "Chemistry D=8 opacity; two He zones → η_eff/2",
        "wesenheit_R": "EM look-path 1+π·SUCTION",
        "crowding": "T1 observer — not a stellar residual in this panel",
        "gamma_fsot": metallicity_gamma(),
        "gamma_breuval": GAMMA_BREUVAL,
        "gamma_sigma": 0.069,
        "R_fsot": wesenheit_r_optical(),
        "R_cardelli_class": R_OPTICAL_LIT,
        "slope_fsot": pl_slope(),
    }
    doc["cepheid_status"] = (
        "GREEN" if pooled_gate_passes(doc.get("pooled_median_error_pct")) else "YELLOW"
    )
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    outcome = {
        "pin": "D1D38A",
        "rows": [
            {"name": r["name"], "computed": r["computed"], "measured": r["measured"], "error_pct": r["error_pct"]}
            for r in rows
        ],
        "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
        "status": doc["cepheid_status"],
        "kill": "pooled median > 0.5% or anyone fits a PL slope/γ to the R22 table",
    }
    OUTCOME.parent.mkdir(parents=True, exist_ok=True)
    OUTCOME.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUTCOME}")
    for r in rows:
        print(f"  {r['name']}: {r['computed']:.5f} vs {r['measured']} ({r['error_pct']:.3f}%)")
    print(f"  pooled={doc.get('pooled_median_error_pct')} {doc['cepheid_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

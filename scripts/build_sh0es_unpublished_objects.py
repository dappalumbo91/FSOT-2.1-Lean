#!/usr/bin/env python3
"""Full 37-host NIR sample + unpublished cz/d ensemble.

Does not retune predictions/sector_h0_seed.json.
Does not treat lstsq_results.txt fitted μ as measured.
Per-host H0=cz/d is labeled peculiar-velocity noise; the gated
PL rows are Table 2 intercepts. Ensemble cz/d is a literature band.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
from fsot_cepheid_pl import full_sample_suite_rows  # noqa: E402
from tier_gap_fill_lib import _bench_v11, pooled_gate_passes  # noqa: E402

FULL = ROOT / "data" / "sh0es_r22_full_nir_cepheids.dat"
ZPATH = ROOT / "data" / "sh0es_host_redshifts.json"
OUT = ROOT / "data" / "sh0es_full_sample_benchmark.json"
OUTCOME = ROOT / "results" / "sh0es_unpublished_objects_outcome.json"


def main() -> int:
    if not FULL.is_file():
        raise SystemExit(f"missing {FULL}; run scripts/ingest_sh0es_full_sample.py")
    _, authority = load_fsot_compute()
    rows, diag = full_sample_suite_rows(FULL, ZPATH)
    tight = [r for r in rows if r.get("record_kind") == "scalar"]
    errs = [float(r["error_pct"]) for r in tight]
    doc = _bench_v11(
        domain="SH0ES_Full_Sample",
        material_records=rows,
        maps_to_lean=["astronomy", "acoustics", "chemistry", "cosmological"],
        d_eff=20,
        authority_path=str(authority).replace("\\", "/"),
        source=[
            "data/sh0es_r22_full_nir_cepheids.dat",
            "data/sh0es_host_redshifts.json",
            "Riess+2022 Table 2 (PantheonPlusSH0ES/DataRelease)",
            "Riess+2022 Table 3 / Table 6",
            "Pantheon+ zCMB (Scolnic+2022, Carr+2022)",
            "Li+2024 JWST TRGB (arXiv:2408.00065)",
            "vendor/fsot_cepheid_pl.py",
        ],
        channel_stats=[("fsot_prediction", "full_nir_pl", errs)],
        sota_baselines={
            "full_nir_pl": {
                "sota_typical_error_pct": 10.0,
                "sota_model": "Fitted PL + free Z_W on orig-19 only",
            }
        },
    )
    doc["tier"] = 51
    doc["policy"] = [
        "no_fitted_PL_slope_or_gamma",
        "no_lstsq_mu_as_measured",
        "no_rho_retune",
        "per_host_cz_d_is_flow_noise",
    ]
    doc["unpublished_fill"] = {
        "full_42_host_nir": "Table 2 37 SN hosts + N4258/M31/LMC/SMC; orig-19 .dat is the R16 subset",
        "per_host_H0_cz_d": "not in Riess; ensemble from seed-closed μ × Pantheon+ zCMB",
    }
    doc["cz_d_diagnostic"] = diag.get("cz_d")
    doc["vs_table6"] = diag.get("vs_table6")
    status = "GREEN" if pooled_gate_passes(doc.get("pooled_median_error_pct")) else "YELLOW"
    doc["full_sample_status"] = status
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    cz = diag.get("cz_d") or {}
    outcome = {
        "pin": "D1D38A",
        "rows": [
            {
                "name": r["name"],
                "computed": r["computed"],
                "measured": r["measured"],
                "error_pct": r["error_pct"],
                "record_kind": r.get("record_kind"),
            }
            for r in rows
        ],
        "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
        "status": status,
        "inventory": {
            "table2_file": "data/sh0es_r22_full_nir_cepheids.dat",
            "n_tight_scalars": len(tight),
        },
        "cz_d": {
            "published_by_riess": False,
            "H0_ivw": cz.get("H0_ivw"),
            "H0_median": cz.get("H0_median"),
            "sigma_ivw_vpec": cz.get("sigma_ivw_vpec"),
            "measured_sh0es": cz.get("measured"),
            "n_hosts": cz.get("n"),
            "n_flow_noise": cz.get("n_flow_noise"),
            "note": (
                "Individual H0_i = cz_cmb/d(μ_FSOT) is peculiar-velocity noise "
                "at 10–40 Mpc. Ensemble is inverse-variance weighted by σ_v=250 km/s. "
                "This is not the SH0ES Hubble-flow estimator and is not a 0.5% central."
            ),
            "hosts": cz.get("hosts"),
        },
        "vs_table6": diag.get("vs_table6"),
        "kill": (
            "tight-scalar median > 0.5%, or anyone treats lstsq μ as measured, "
            "or anyone 0.5%-gates an individual nearby cz/d H0, "
            "or anyone retunes ρ to hit 73.04"
        ),
    }
    OUTCOME.parent.mkdir(parents=True, exist_ok=True)
    OUTCOME.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUTCOME}")
    for r in rows:
        print(
            f"  {r['name']}: {r['computed']:.5f} vs {r['measured']} "
            f"({r['error_pct']:.3f}%) [{r.get('record_kind')}]"
        )
    print(f"  pooled={doc.get('pooled_median_error_pct')} {status}")
    if cz:
        print(
            f"  cz/d IVW {cz.get('H0_ivw')} vs 73.04  "
            f"n={cz.get('n')} flow_noise={cz.get('n_flow_noise')} "
            f"sig_pv={cz.get('sigma_ivw_vpec')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

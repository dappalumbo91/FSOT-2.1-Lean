#!/usr/bin/env python3
"""FRB DM excess × catalog-normalized local_sky_density.

Same kernel as the H0 ladder (θ0 = 180°/φ²). This is a *same-kernel*
bridge, not a 0.5% residual of 200·(1+density) on the 10-row seed —
that residual is ~70% and is reported honestly, not stuffed.

PRED-076 locks the shared kernel. PRED-052 keeps the 200 pc cm⁻³ class.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from bubble_bleed_physics import local_sky_density, sky_kernel_theta0_deg  # noqa: E402

FRB = ROOT / "data" / "frb_repeater_cache.json"
NEB = ROOT / "data" / "nebula_lensing_cache.json"
OUT = ROOT / "results" / "frb_sky_density_bridge_outcome.json"
DM_CLASS = 200.0


def main() -> int:
    frbs = json.loads(FRB.read_text(encoding="utf-8")).get("frbs") or []
    nebulae = json.loads(NEB.read_text(encoding="utf-8")).get("nebulae") or []
    rows = []
    for i, row in enumerate(frbs):
        ra = row.get("ra_deg")
        if ra is None:
            continue
        others = [x for j, x in enumerate(frbs) if j != i]
        dens = local_sky_density(float(ra), float(row.get("dec_deg") or 0.0), nebulae, others)
        ex = row.get("dm_excess_pc")
        pred = DM_CLASS * (1.0 + dens)
        err = None
        if ex not in (None, 0):
            err = abs(pred - float(ex)) / abs(float(ex)) * 100.0
        rows.append(
            {
                "name": row.get("name"),
                "ra_deg": float(ra),
                "density_sky": round(dens, 6),
                "dm_pc": row.get("dm_pc"),
                "dm_excess_pc": ex,
                "predicted_excess_200x1pdens": round(pred, 3),
                "error_pct_vs_excess": None if err is None else round(err, 4),
            }
        )
    with_ex = [r for r in rows if r["error_pct_vs_excess"] is not None]
    errs = sorted(float(r["error_pct_vs_excess"]) for r in with_ex)
    hi = [r for r in with_ex if float(r["density_sky"]) >= 0]
    lo = [r for r in with_ex if float(r["density_sky"]) < 0]
    med_err = median(errs) if errs else None
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "kernel_theta0_deg": sky_kernel_theta0_deg(),
        "policy": [
            "same_kernel_as_h0_local_sky_density",
            "do_not_stuff_70pct_into_0_5pct_gate",
            "pred_052_keeps_200_class",
        ],
        "n_frb": len(frbs),
        "n_with_ra": len(rows),
        "n_with_dm_excess": len(with_ex),
        "median_error_pct_200x1pdens": med_err,
        "high_density_n": len(hi),
        "low_density_n": len(lo),
        "high_density_median_excess": median([float(r["dm_excess_pc"]) for r in hi]) if hi else None,
        "low_density_median_excess": median([float(r["dm_excess_pc"]) for r in lo]) if lo else None,
        "verdict": (
            "NOT_A_0_5PCT_CENTRAL"
            if (med_err is None or med_err > 0.5)
            else "WITHIN_GREEN_GATE"
        ),
        "lock": (
            "PRED-076 same-kernel classifier + PRED-052 200 pc cm-3 class. "
            "Do not 0.5%-gate 200*(1+density) on this 10-row seed."
        ),
        "rows": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  n_excess={len(with_ex)} median_err_pct={med_err} verdict={doc['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

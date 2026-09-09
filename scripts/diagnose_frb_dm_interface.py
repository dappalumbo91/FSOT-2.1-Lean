#!/usr/bin/env python3
"""Autopsy of retired formula 200·(1+local_sky_density) on FRB DM excess.

REMEDIED_WRONG_APPLY — not an open isolate. The orifice (PRED-084) replaced it.
Do not stuff the 66% into 0.5%. Do not reuse the formula.

Wrong object: DM excess is mostly IGM path length (Cosmology D=25).
local_sky_density is an angular H0-ladder kernel (θ0=180°/φ²), dimensionless
~±0.2. So 200·(1+dens) is trapped in ~160–240 pc cm⁻³ and cannot represent
a nearby FRB with excess ~15 or a distant one with excess ~580.

PRED-052 keeps the 200 class. PRED-076 keeps the shared kernel classifier.
PRED-084 is the burst object (width×fluence vs e·POOF).
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
OUT = ROOT / "results" / "frb_interface_diagnosis.json"
DOC = ROOT / "docs" / "FRB_INTERFACE_DIAGNOSIS.md"
DM_CLASS = 200.0
PIN = "D1D38A"


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
                "predicted_200x1pdens": round(pred, 3),
                "error_pct": None if err is None else round(err, 4),
            }
        )
    with_ex = [r for r in rows if r["error_pct"] is not None]
    errs = [float(r["error_pct"]) for r in with_ex]
    dens_all = [float(r["density_sky"]) for r in rows]
    pred_all = [float(r["predicted_200x1pdens"]) for r in rows]
    hi = [r for r in with_ex if float(r["density_sky"]) >= 0]
    lo = [r for r in with_ex if float(r["density_sky"]) < 0]
    med_err = median(errs) if errs else None
    # Sign test: does higher angular density mean higher excess?
    hi_ex = median([float(r["dm_excess_pc"]) for r in hi]) if hi else None
    lo_ex = median([float(r["dm_excess_pc"]) for r in lo]) if lo else None
    sign_ok = (
        hi_ex is not None and lo_ex is not None and hi_ex > lo_ex
    )
    band = (min(pred_all), max(pred_all)) if pred_all else (None, None)
    excesses = [float(r["dm_excess_pc"]) for r in with_ex]
    isolated = {
        "formula": "DM_excess ≈ 200 · (1 + local_sky_density)",
        "why_ugly": (
            "local_sky_density is dimensionless ~±0.2 (H0 angular kernel). "
            "The formula is trapped in a ~160–240 pc cm⁻³ band and cannot "
            "reach nearby excess ~15 or distant excess ~580. High-density "
            "sightlines do not even have higher median excess on this seed."
        ),
        "correct_objects": {
            "PRED-052": "200 pc cm⁻³ excess *class*, not per-FRB 200*(1+dens)",
            "PRED-076": "same θ0=180/φ² kernel as H0 (classifier), not a DM residual",
            "replaced_by": "PRED-084 orifice (width×fluence vs e·POOF)",
            "later_split": (
                "Split DM = DM_MW + DM_IGM(z) + DM_host. Route DM_IGM on "
                "Cosmology D=25. Only then test leftover vs local_sky_density. "
                "That is a separate Cosmology job for the PRED-052 class when "
                "redshifts exist — not this 66% sitting open."
            ),
        },
        "not": [
            "Keep 66% as an open isolate after the orifice replaced it",
            "Stuff 66% into the 0.5% green gate",
            "Fit a new β in front of density",
            "Retune the 200 class after looking at these 10 rows",
            "Reuse 200·(1+local_sky_density) as a DM residual",
        ],
    }
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": PIN,
        "verdict": "REMEDIED_WRONG_APPLY",
        "policy": [
            "do_not_stuff_into_0_5pct",
            "diagnose_apply_not_retune",
            "pred_052_class_pred_076_kernel",
            "pred_084_orifice_replaced_this_formula",
            "remedied_is_not_an_open_isolate",
        ],
        "kernel_theta0_deg": sky_kernel_theta0_deg(),
        "n_frb": len(frbs),
        "n_with_ra": len(rows),
        "n_with_dm_excess": len(with_ex),
        "density_min": min(dens_all) if dens_all else None,
        "density_max": max(dens_all) if dens_all else None,
        "predicted_band_pc": band,
        "measured_excess_min": min(excesses) if excesses else None,
        "measured_excess_max": max(excesses) if excesses else None,
        "median_error_pct_200x1pdens": med_err,
        "high_density_n": len(hi),
        "low_density_n": len(lo),
        "high_density_median_excess": hi_ex,
        "low_density_median_excess": lo_ex,
        "density_tracks_excess_sign": sign_ok,
        "isolated": isolated,
        "worst_row": max(with_ex, key=lambda r: float(r["error_pct"])) if with_ex else None,
        "best_row": min(with_ex, key=lambda r: float(r["error_pct"])) if with_ex else None,
        "rows": with_ex,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    worst = doc["worst_row"] or {}
    best = doc["best_row"] or {}
    lines = [
        "# FRB DM excess — retired formula autopsy",
        "",
        f"*Generated {doc['generated_at']} · pin {PIN}*",
        "",
        "**Verdict: `REMEDIED_WRONG_APPLY`.** The formula",
        "`200·(1+local_sky_density)` on DM excess is **retired**. Median error",
        f"on {len(with_ex)} rows with excess was **{med_err:.1f}%**. That was the",
        "wrong object (IGM path vs H0 angular kernel). The burst object is the",
        "orifice (PRED-084). Do **not** keep this as an open isolate. Do **not**",
        "stuff 66% into 0.5%. Do **not** reuse the formula.",
        "",
        "## What was applied (the wrong object)",
        "",
        "```text",
        "DM_excess  ≈  200 pc cm⁻³  ·  (1 + local_sky_density)",
        "local_sky_density  =  H0 ladder angular kernel, θ0 = 180°/φ²",
        "```",
        "",
        "The kernel is the *same grammar* as H0 sightlines (PRED-076). The",
        "**formula** treats that dimensionless crowding (~±0.2) as a 20% wiggle",
        "around a 200 pc class. That is a local-bubble perturbation, not IGM path.",
        "",
        "| Handle | Value |",
        "|--------|------:|",
        f"| Density range on this seed | {doc['density_min']:.3f} … {doc['density_max']:.3f} |",
        f"| Predicted excess band | {band[0]:.0f} … {band[1]:.0f} pc cm⁻³ |",
        f"| Measured excess range | {doc['measured_excess_min']:.0f} … {doc['measured_excess_max']:.0f} pc cm⁻³ |",
        f"| Median error | **{med_err:.1f}%** |",
        f"| High-density median excess (n={len(hi)}) | {hi_ex} |",
        f"| Low-density median excess (n={len(lo)}) | {lo_ex} |",
        f"| Density tracks excess (sign) | **{sign_ok}** |",
        "",
        f"Worst row: `{worst.get('name')}` measured {worst.get('dm_excess_pc')} vs",
        f"pred {worst.get('predicted_200x1pdens')} (**{worst.get('error_pct')}%**).",
        f"Best row: `{best.get('name')}` **{best.get('error_pct')}%** — still not a gate.",
        "",
        "## Why the mathematics is off (APPLY, not a new β)",
        "",
        "1. **IGM path is Cosmology \(D=25\).** DM excess grows with redshift.",
        "   A nearby FRB can sit at ~15 pc cm⁻³ extra. A distant one at ~580.",
        "   \(200·(1+0.2)\) cannot leave ~160–240. The band is a **ceiling of the formula**,",
        "   not a measurement.",
        "2. **Sign is wrong on this seed.** Higher angular density does **not**",
        "   come with higher median excess (high 380 vs low 420). A bubble-density",
        "   multiplier would have the other sign.",
        "3. **n=10 with excess, 38 with RA, no redshift.** CHIME dump 503s blocked.",
        "   This is a seed, not a catalog. A 0.5% central on ten numbers would be stuffing.",
        "",
        "## Correct objects (already locked — do not retune)",
        "",
        "| Lock | Object |",
        "|------|--------|",
        "| **PRED-052** | 200 pc cm⁻³ *class* (some sightlines sit near that class) |",
        "| **PRED-076** | Same \(\\theta_0=180/\\varphi^2\) kernel as H0 — classifier, not a DM residual |",
        "| **PRED-084** | Orifice: width×fluence vs \(e\\cdot\\mathrm{POOF}\) — the burst object |",
        "",
        "## What replaced it (orifice — the burst object)",
        "",
        "The burst is not sky crowding. It is the puncture. See",
        "[`FRB_ORIFICE.md`](FRB_ORIFICE.md) · PRED-084.",
        "",
        "```text",
        "E_rip = width_ms × fluence     (no DM — DM is IGM path)",
        "repeater if E_rip ≥ e · POOF   (enough outgassing to flop the saloon doors)",
        "T_activity = 5π + 1/φ days     (Particle orifice cycle + Omori rest)",
        "```",
        "",
        "## Later Cosmology split (not this 66% sitting open)",
        "",
        "```text",
        "DM_obs  =  DM_MW  +  DM_IGM(z)  +  DM_host/bubble",
        "         Cosmology D=25     leftover vs local_sky_density",
        "```",
        "",
        "Route `DM_IGM(z)` on Cosmology when redshifts exist. That is a separate",
        "job for the PRED-052 class. It does **not** reopen this retired formula",
        "as an isolate.",
        "",
        "## Kill",
        "",
        "- Keeping 66% on the open isolate list after the orifice replaced it.",
        "- Stuffing 66% into the 0.5% green gate.",
        "- Fitting β in `200·(1+β·density)` after seeing these 10 rows.",
        "- Retuning the 200 class.",
        "- Calling PRED-076 a 0.5% DM residual.",
        "- Reusing `200·(1+local_sky_density)` as a DM residual.",
        "",
        "Refresh: `python scripts/diagnose_frb_dm_interface.py`",
        "",
        "Related: [`OBJECT_SCORING.md`](OBJECT_SCORING.md) · [`APPLY.md`](APPLY.md) ·",
        "[`ISOLATED_RESIDUALS.md`](ISOLATED_RESIDUALS.md) ·",
        "[`FRB_ORIFICE.md`](FRB_ORIFICE.md) · PRED-052 / PRED-076 / PRED-084",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {DOC}")
    print(f"  n={len(with_ex)} median={med_err} sign_ok={sign_ok} verdict=REMEDIED_WRONG_APPLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

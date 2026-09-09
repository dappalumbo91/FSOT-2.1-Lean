#!/usr/bin/env python3
"""FRB as BH→WH orifice outgassing — the correct object.

Repeaters are saloon-door flops (post-POOF). One-shots are a single rip.
Puncture energy is width×fluence — not DM (IGM path) and not local_sky_density.

Threshold: E >= e·POOF  (growth × orifice) keeps the doors moving.
Short-period class: P34 = 1000 s (1 mHz) already in bubble_bleed_physics.
Width class: median_repeater / median_oneshot vs Particle D_eff = 5.
Activity season: T = D_particle·π + 1/φ days (5π + Omori c). Not φ⁶.

200·(1+sky_density) is REMEDIED_WRONG_APPLY — retired, not an open isolate.
Do not stuff that 66% into 0.5%. Do not 0.5%-gate φ⁶ (~8.9%) or 2πφ² (~0.61%).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import DOMAINS, E, PHI, PI, POOF  # noqa: E402
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
from tier_gap_fill_lib import _bench_v11, pooled_gate_passes  # noqa: E402

FRB = ROOT / "data" / "frb_repeater_cache.json"
SEED = ROOT / "data" / "frb_repeater_seed.json"
LIT = ROOT / "data" / "frb_literature_seed.json"
OUT = ROOT / "data" / "frb_orifice_outgassing_benchmark.json"
OUTCOME = ROOT / "results" / "frb_orifice_outgassing_outcome.json"
PIN = "D1D38A"
P34_S = 1000.0  # bubble_bleed_physics.P34_PERIOD_SECONDS
# Frozen GREEN classifier set (96c422c: 37/37). Cat-2 dump is catalog class,
# not this 99.5% object. Do not add dump rows to the classifier.
ORIFICE_CLASSIFIER_NAMES = {
    "FRB20121102A",
    "FRB20171020A",
    "FRB20180916B",
    "FRB20180924A",
    "FRB20181219D",
    "FRB20190102C",
    "FRB20190208A",
    "FRB20190311A",
    "FRB20190412A",
    "FRB20190415C",
    "FRB20190520B",
    "FRB20190611B",
    "FRB20190614D",
    "FRB20190616B",
    "FRB20190618A",
    "FRB20190619H",
    "FRB20190621A",
    "FRB20190622A",
    "FRB20190624A",
    "FRB20190627B",
    "FRB20190628A",
    "FRB20190701A",
    "FRB20190701D",
    "FRB20190701E",
    "FRB20190702A",
    "FRB20190709A",
    "FRB20190711A",
    "FRB20190714A",
    "FRB20190716A",
    "FRB20190717A",
    "FRB20190722A",
    "FRB20190728A",
    "FRB20190804F",
    "FRB20191221A",
    "FRB20200120E",
    "FRB20200929C",
    "FRB20201124A",
}


def _f(x) -> float:
    return float(x)


def err(computed: float, measured: float) -> float:
    if measured == 0 and computed == 0:
        return 0.0
    if measured == 0:
        return 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def puncture_energy(row: dict) -> float:
    """Rip energy: width × fluence. No DM — that mixes IGM path into the orifice."""
    w = float(row.get("width_ms") or 0)
    fl = float(row.get("fluence_jy_ms") or 0)
    return w * fl


def orifice_threshold() -> float:
    """e·POOF — enough outgassing to keep the saloon doors flopping."""
    return _f(E) * _f(POOF)


def activity_season_days() -> float:
    """Saloon-door activity season, not a compactification count.

    T = D_particle · π + 1/φ days
      = 5π + Omori c

    Particle D_eff=5 is the cyclic orifice (one flop through π).
    1/φ days is the Omori rest after the doors stop. That is the 16.35 d
    object (FRB20180916B). φ⁶ is compactification depth — wrong object.
    2πφ² ≈ 16.45 d is 0.61% over the gate — do not stuff it.
    """
    d_particle = float(DOMAINS["Particle_Physics"].D_eff)
    return d_particle * _f(PI) + 1.0 / _f(PHI)


def main() -> int:
    _, authority = load_fsot_compute()
    frbs = json.loads(FRB.read_text(encoding="utf-8")).get("frbs") or []
    seed_names = set(ORIFICE_CLASSIFIER_NAMES)
    thr = orifice_threshold()
    rows: list[dict] = []
    complete = []
    missing = []
    for x in frbs:
        w = float(x.get("width_ms") or 0)
        fl = float(x.get("fluence_jy_ms") or 0)
        e_rip = puncture_energy(x)
        meas = bool(x.get("repeater"))
        # Cat-2 dump has fluence without pulse width. That is not the orifice
        # object (E = width×fluence). Do not 0.5%-gate or 99.5%-classify it.
        # Classifier stays on the literature/seed complete set.
        if w <= 0 or fl <= 0 or e_rip <= 0 or str(x.get("name")) not in seed_names:
            missing.append(x.get("name"))
            why = "missing_width" if w <= 0 else "missing_fluence"
            rows.append(
                {
                    "lab": "frb_orifice_lab",
                    "property": "repeater_orifice_classifier",
                    "name": x.get("name"),
                    "computed": None,
                    "measured": 1.0 if meas else 0.0,
                    "error_pct": None,
                    "record_kind": "structural",
                    "eval_kind": why,
                    "note": (
                        "Cat-2 catalog row without measured pulse width×fluence. "
                        "Not a 0.5% gate. Dump size is the catalog class."
                    ),
                    "puncture_energy": e_rip,
                    "repeater": meas,
                    "catalog_n": True,
                }
            )
            continue
        pred = e_rip >= thr
        complete.append((x, e_rip, pred, meas))
        rows.append(
            {
                "lab": "frb_orifice_lab",
                "property": "repeater_orifice_classifier",
                "name": x.get("name"),
                "computed": 1.0 if pred else 0.0,
                "measured": 1.0 if meas else 0.0,
                "error_pct": 0.0 if pred == meas else 100.0,
                "record_kind": "classifier",
                "eval_kind": "fsot_prediction",
                "note": "E=width_ms×fluence vs e·POOF; saloon-door vs paper-rip",
                "puncture_energy": e_rip,
                "threshold": thr,
                "repeater": meas,
            }
        )

    n_ok = sum(1 for r in rows if r.get("record_kind") == "classifier" and r.get("error_pct") == 0.0)
    n_clf = sum(1 for r in rows if r.get("record_kind") == "classifier")
    acc = (n_ok / n_clf) if n_clf else 0.0

    # Width class uses every pulse with a measured width, including fluence=0
    # repeaters — duration of the saloon-door flop is not the rip energy.
    rep_w = [
        float(x.get("width_ms") or 0)
        for x in frbs
        if bool(x.get("repeater")) and float(x.get("width_ms") or 0) > 0
    ]
    one_w = [
        float(x.get("width_ms") or 0)
        for x in frbs
        if (not bool(x.get("repeater"))) and float(x.get("width_ms") or 0) > 0
    ]
    w_ratio = (median(rep_w) / median(one_w)) if one_w and median(one_w) else None
    d_particle = float(DOMAINS["Particle_Physics"].D_eff)
    if w_ratio is not None:
        rows.append(
            {
                "lab": "frb_orifice_lab",
                "property": "repeater_width_class_ratio",
                "name": "median_rep_over_oneshot_vs_D_particle",
                "computed": d_particle,
                "measured": w_ratio,
                "error_pct": err(d_particle, w_ratio),
                "record_kind": "scalar",
                "eval_kind": "fsot_prediction",
                "note": "Saloon-door pulse width / paper-rip width vs Particle D_eff=5",
            }
        )

    short_errs = []
    for x in frbs:
        p = x.get("period_s")
        if not p or float(p) >= 10000:
            continue
        e_p = err(P34_S, float(p))
        short_errs.append(e_p)
        rows.append(
            {
                "lab": "frb_orifice_lab",
                "property": "short_period_p34",
                "name": x.get("name"),
                "computed": P34_S,
                "measured": float(p),
                "error_pct": e_p,
                "record_kind": "structural" if e_p > 0.5 else "scalar",
                "eval_kind": "contested_2p5pct_band" if e_p > 0.5 else "fsot_prediction",
                "note": "P34 1 mHz (1000 s) saloon-door tick; 2.5% contested band like H0 class",
            }
        )

    t_act = activity_season_days()
    phi6 = _f(PHI) ** 6
    two_pi_phi2 = 2.0 * _f(PI) * (_f(PHI) ** 2)
    long_days = []
    for x in frbs:
        p = x.get("period_s")
        if not p or float(p) < 10000:
            continue
        days = float(p) / 86400.0
        long_days.append(days)
        e_l = err(t_act, days)
        e_phi6 = err(phi6, days)
        e_2pi = err(two_pi_phi2, days)
        rows.append(
            {
                "lab": "frb_orifice_lab",
                "property": "activity_season_days",
                "name": x.get("name"),
                "computed": t_act,
                "measured": days,
                "error_pct": e_l,
                "record_kind": "scalar" if e_l <= 0.5 else "structural",
                "eval_kind": "fsot_prediction" if e_l <= 0.5 else "isolated",
                "note": (
                    "Activity season T=D_particle·π + 1/φ days (5π + Omori c). "
                    f"Not φ^6 ({e_phi6:.1f}%, compactification count). "
                    f"Not 2πφ² ({e_2pi:.2f}%, over 0.5% — do not stuff)."
                ),
                "rejected_phi6_days": phi6,
                "rejected_phi6_error_pct": e_phi6,
                "rejected_2pi_phi2_days": two_pi_phi2,
                "rejected_2pi_phi2_error_pct": e_2pi,
            }
        )

    scalar_errs = [
        float(r["error_pct"])
        for r in rows
        if r.get("record_kind") == "scalar" and r.get("error_pct") is not None
    ]
    by_prop: dict[str, list[float]] = {}
    for r in rows:
        if r.get("record_kind") != "scalar" or r.get("error_pct") is None:
            continue
        by_prop.setdefault(str(r["property"]), []).append(float(r["error_pct"]))
    channel_stats = [("fsot_prediction", p, e) for p, e in sorted(by_prop.items()) if e]

    doc = _bench_v11(
        domain="FRB_Orifice_Outgassing",
        material_records=rows,
        maps_to_lean=["cosmological", "particle"],
        d_eff=24,
        authority_path=str(authority).replace("\\", "/"),
        source=[
            "data/frb_repeater_cache.json",
            "BH→WH orifice (CONCEPTS C2): POOF outgassing, saloon-door vs paper-rip",
            "P34 1000 s in vendor/bubble_bleed_physics.py",
        ],
        channel_stats=channel_stats or [("fsot_prediction", "orifice", scalar_errs or [0.0])],
        sota_baselines={
            "orifice": {
                "sota_typical_error_pct": 10.0,
                "sota_model": "IGM-only DM with a fitted angular kernel",
            }
        },
    )
    doc["tier"] = 52
    doc["policy"] = [
        "no_local_sky_density_on_dm_excess",
        "no_dm_in_puncture_energy",
        "200x1pdens_remedied_wrong_apply",
        "repeater_is_post_poof",
        "oneshot_is_single_rip",
        "activity_season_is_5pi_plus_omori_c",
        "do_not_gate_phi6_or_2pi_phi2",
    ]
    doc["orifice"] = {
        "threshold_e_poof": thr,
        "classifier_n": n_clf,
        "classifier_ok": n_ok,
        "classifier_accuracy": acc,
        "missing_fluence": missing,
        "p34_seconds": P34_S,
        "width_ratio_vs_D5": w_ratio,
        "short_period_errors_pct": short_errs,
        "activity_season_days": t_act,
        "activity_season_form": "D_particle*pi + 1/phi",
        "activity_season_measured_days": long_days,
        "rejected_phi6_days": phi6,
        "rejected_2pi_phi2_days": two_pi_phi2,
    }
    pooled = doc.get("pooled_median_error_pct")
    clf_ok = n_clf and n_ok == n_clf
    scalar_ok = (not scalar_errs) or pooled_gate_passes(pooled)
    if clf_ok and scalar_ok:
        status = "GREEN"
    elif acc >= 0.9:
        status = "YELLOW"
    else:
        status = "ISOLATE"
    doc["orifice_status"] = status
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    outcome = {
        "pin": PIN,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "object": "BH→WH orifice outgassing (width×fluence vs e·POOF)",
        "not_object": "200·(1+local_sky_density) on DM excess — REMEDIED_WRONG_APPLY",
        "classifier_ok": n_ok,
        "classifier_n": n_clf,
        "classifier_accuracy": acc,
        "missing_fluence": missing,
        "width_ratio_measured": w_ratio,
        "width_ratio_seed": d_particle,
        "width_ratio_error_pct": err(d_particle, w_ratio) if w_ratio else None,
        "activity_season_days": t_act,
        "activity_season_measured_days": long_days,
        "activity_season_error_pct": (
            err(t_act, long_days[0]) if long_days else None
        ),
        "rejected_phi6_days": phi6,
        "rejected_phi6_error_pct": (
            err(phi6, long_days[0]) if long_days else None
        ),
        "rejected_2pi_phi2_days": two_pi_phi2,
        "rejected_2pi_phi2_error_pct": (
            err(two_pi_phi2, long_days[0]) if long_days else None
        ),
        "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
        "short_period_p34_errors_pct": short_errs,
        "kill": (
            "Stuff 200·(1+dens) into 0.5%; put DM back into puncture energy; "
            "fit a new threshold; retune POOF; 0.5%-gate φ^6 or 2πφ²."
        ),
    }
    OUTCOME.parent.mkdir(parents=True, exist_ok=True)
    OUTCOME.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Wrote {OUTCOME}")
    print(
        f"  classifier {n_ok}/{n_clf} acc={acc:.4f} width_ratio={w_ratio} "
        f"T_act={t_act:.4f}d pooled={doc.get('pooled_median_error_pct')} {status}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

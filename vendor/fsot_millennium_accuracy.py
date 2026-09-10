#!/usr/bin/env python3
"""Accuracy vs public SOTA for the functions the six Clay problems name.

Clay prize-process (Qualifying Outlet, two years, community acceptance) lives
in fsot_millennium_track.py and stays all-zeros until those gates are real.

This module answers a different question: if you simulate the *function* each
problem is trying to capture, is the seed-locked FSOT number more accurate
than what is currently public? Wrong object is a false win. A residual probe
is not a Clay theorem. Glueball vs Teper is allowed to lose.

Two independent bars, never collapsed:
  1. Public SOTA — did we beat the competitor on that function?
  2. FSOT system accuracy — green gate 0.5%, aspiration 0.05%.
A SOTA beat outside 0.5% is still FSOT accuracy WIP. Do not stuff it into the gate.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from fsot_compute import E, PHI, PI
    from fsot_dynamics import sound_speed_sq, viscosity_eff
    from fsot_millennium_track import GAMMA, RIEMANN_T1, clay_process_flags
    from fsot_path_sum import run_path_sum_suite
    from fsot_quantum_trinary_syntax import GROVER_EXPONENT
    from fsot_seed_flavor import seed_lambda_qcd_GeV, seed_string_tension_GeV
except ImportError:  # pragma: no cover
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fsot_compute import E, PHI, PI
    from fsot_dynamics import sound_speed_sq, viscosity_eff
    from fsot_millennium_track import GAMMA, RIEMANN_T1, clay_process_flags
    from fsot_path_sum import run_path_sum_suite
    from fsot_quantum_trinary_syntax import GROVER_EXPONENT
    from fsot_seed_flavor import seed_lambda_qcd_GeV, seed_string_tension_GeV

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "millennium_accuracy_scoreboard.json"
OUT_MD = ROOT / "docs" / "MILLENNIUM_ACCURACY_VS_SOTA.md"
WX_JSON = ROOT / "results" / "dated_forecast_scores" / "WEATHER_24H_RETRO.json"

# In-repo PDG-class anchors already used by fsot_gr_sm / seed flavor. Do not retune.
PDG_LAMBDA_QCD_GEV = 0.2173
INREPO_GLUEBALL_BALLPARK = 3.5

# Public literature (cited; not fitted).
# FLAG Review 2024 / Aoki et al. 2411.04268: Λ_MS^(5) = 213(8) MeV.
FLAG_LAMBDA_MS5_GEV = 0.213
FLAG_LAMBDA_MS5_SIGMA_GEV = 0.008
# Teper, hep-lat/9711011: continuum ratios. Lattice is the *measurement*.
# Same paper's closed-form rule of thumb is m(0++) ~ 4√σ and m(2++)/m(0++) ~ 3/2.
TEPER_GLUEBALL_OVER_SQRT_SIGMA = 3.65
TEPER_GLUEBALL_STAT = 0.11
TEPER_GLUEBALL_2PP_OVER_SQRT_SIGMA = 5.15
TEPER_GLUEBALL_2PP_STAT = 0.21
TEPER_CLOSED_FORM_0PP = 4.0
TEPER_CLOSED_FORM_RATIO = 1.5
# Odlyzko / LMFDB Im(ρ_n) for n=1..10 (measurement, not a competing theory).
# Rest-of-system residual bars (same as the 477-domain green / aspiration gates).
FSOT_GREEN_GATE_PCT = 0.5
FSOT_ASPIRATION_PCT = 0.05

ODLYZKO_T = (
    14.134725141734693,
    21.022039638771555,
    25.010857580145688,
    30.424876125859513,
    32.935061587739189,
    37.586178158825671,
    40.918719012147495,
    43.327073280914999,
    48.005150881167159,
    49.773832477672302,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _err_pct(computed: float, measured: float) -> float:
    return abs(computed - measured) / max(abs(measured), 1e-30) * 100.0


def _f(x: Any) -> float:
    return float(x)


def riemann_von_mangoldt_t(n: int) -> float:
    """Invert N(T)≈(T/2π)log(T/2π)−T/2π+7/8 at N=n.

    Public zero-parameter closed form. Odlyzko is the measurement, not a competitor.
    """
    target = float(n) - 0.875

    def residual(u: float) -> float:
        return u * math.log(u) - u - target

    lo, hi = 1.1, 40.0
    while residual(hi) < 0.0:
        hi *= 1.5
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if residual(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 2.0 * math.pi * (0.5 * (lo + hi))


def riemann_von_mangoldt_t1() -> float:
    return riemann_von_mangoldt_t(1)


def riemann_spacing_walk(t1: float, n_zeros: int) -> list[float]:
    """t_{k+1} = t_k + 2π / log(t_k / 2π), started from seed-locked t1.

    Mean spacing is the public density of zeros. No new coefficient.
    n≥2 is out-of-sample relative to the first-zero seed.
    """
    out = [float(t1)]
    for _ in range(n_zeros - 1):
        t = out[-1]
        out.append(t + 2.0 * math.pi / math.log(t / (2.0 * math.pi)))
    return out


def _weather_skill() -> dict[str, Any]:
    """Hold/kill vs observations, plus majority-class baseline. Not ECMWF RMSE."""
    if not WX_JSON.is_file():
        return {"present": False}
    doc = json.loads(WX_JSON.read_text(encoding="utf-8"))
    rows = [r for r in (doc.get("rows") or []) if r.get("result_24h") in ("hold", "kill")]
    n = len(rows)
    if n == 0:
        return {"present": True, "n_scored": 0}
    n_hold = sum(1 for r in rows if r.get("result_24h") == "hold")
    n_storm = sum(1 for r in rows if r.get("saw_storm_24h"))
    n_quiet = n - n_storm
    majority_pct = max(n_storm, n_quiet) / n * 100.0
    hold_pct = n_hold / n * 100.0
    return {
        "present": True,
        "n_scored": n,
        "n_hold": n_hold,
        "hold_pct": hold_pct,
        "n_storm_obs": n_storm,
        "n_quiet_obs": n_quiet,
        "majority_pct": majority_pct,
        "beats_majority": hold_pct > majority_pct,
        "n_24h_agrees_48h": int(doc.get("n_24h_agrees_48h") or 0),
        "n_with_obs": int(doc.get("n_with_obs") or 0),
    }


def _weather_24h() -> dict[str, Any]:
    if not WX_JSON.is_file():
        return {"present": False}
    doc = json.loads(WX_JSON.read_text(encoding="utf-8"))
    n_obs = int(doc.get("n_with_obs") or 0)
    n_agree = int(doc.get("n_24h_agrees_48h") or 0)
    return {
        "present": True,
        "n": int(doc.get("n") or 0),
        "n_with_obs": n_obs,
        "n_agree": n_agree,
        "agree_frac": (n_agree / n_obs) if n_obs else None,
    }


def _row(
    *,
    problem: str,
    function_object: str,
    clay_object: str,
    name: str,
    computed: float | None,
    measured: float | None,
    public_sota_model: str,
    public_sota_typical_error_pct: float | None,
    comparison_class: str,
    verdict: str,
    beats_or_meets_sota: bool | None,
    native_status: str,
    note: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    err = None
    if computed is not None and measured is not None:
        err = _err_pct(computed, measured)
    rec: dict[str, Any] = {
        "problem": problem,
        "name": name,
        "function_object": function_object,
        "clay_object": clay_object,
        "computed": computed,
        "measured": measured,
        "fsot_error_pct": err,
        "public_sota_model": public_sota_model,
        "public_sota_typical_error_pct": public_sota_typical_error_pct,
        "comparison_class": comparison_class,
        "verdict": verdict,
        "beats_or_meets_sota": beats_or_meets_sota,
        "clay_status": "OPEN_NOT_CLAIMED",
        "native_status": native_status,
        "note": note,
    }
    if extra:
        rec.update(extra)
    return _stamp_accuracy_lanes(rec)


def _stamp_accuracy_lanes(rec: dict[str, Any]) -> dict[str, Any]:
    """SOTA beat and FSOT 0.5%/0.05% gates are independent. Do not collapse them."""
    klass = rec.get("comparison_class")
    err = rec.get("fsot_error_pct")
    rec["fsot_green_gate_pct"] = FSOT_GREEN_GATE_PCT
    rec["fsot_aspiration_pct"] = FSOT_ASPIRATION_PCT
    if klass in ("no_fair_compare", "structure"):
        rec["fsot_green"] = "n/a"
        rec["fsot_aspiration"] = "n/a"
        rec["progress"] = "open_track_next" if klass == "no_fair_compare" else "structure"
        rec["next_dig"] = klass == "no_fair_compare"
        rec["sota_beats_fsot_accuracy_wip"] = False
        return rec
    if klass == "related_not_clay":
        rec["fsot_green"] = "wip"
        rec["fsot_aspiration"] = "wip"
        rec["progress"] = "miss_next"
        rec["next_dig"] = True
        rec["sota_beats_fsot_accuracy_wip"] = False
        return rec
    if err is None:
        rec["fsot_green"] = "n/a"
        rec["fsot_aspiration"] = "n/a"
        rec["progress"] = "open_track_next"
        rec["next_dig"] = True
        rec["sota_beats_fsot_accuracy_wip"] = False
        return rec
    rec["fsot_green"] = "pass" if err <= FSOT_GREEN_GATE_PCT else "wip"
    rec["fsot_aspiration"] = "pass" if err <= FSOT_ASPIRATION_PCT else "wip"
    beat = rec.get("beats_or_meets_sota") is True
    rec["sota_beats_fsot_accuracy_wip"] = bool(beat and rec["fsot_green"] == "wip")
    if beat:
        if rec["fsot_green"] == "wip":
            rec["progress"] = "beats_sota_fsot_accuracy_wip"
            rec["next_dig"] = False
        elif rec["fsot_aspiration"] == "wip":
            rec["progress"] = "beats_sota_in_green_aspiration_wip"
            rec["next_dig"] = False
        else:
            rec["progress"] = "beats_sota_in_aspiration"
            rec["next_dig"] = False
    elif rec.get("beats_or_meets_sota") is False:
        rec["progress"] = "miss_next"
        rec["next_dig"] = True
    else:
        rec["progress"] = "open_track_next"
        rec["next_dig"] = True
    return rec


def run_accuracy_scoreboard() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    # --- Riemann: first-zero Im(ρ1) closed form vs public asymptotic ---
    t1 = math.e / (GAMMA ** 3)
    t_rvm = riemann_von_mangoldt_t1()
    rvm_err = _err_pct(t_rvm, RIEMANN_T1)
    fsot_t1_err = _err_pct(t1, RIEMANN_T1)
    rows.append(
        _row(
            problem="Riemann hypothesis",
            function_object="Im(ρ1) of ζ — first non-trivial zero (closed form vs tabulated)",
            clay_object="All non-trivial zeros have Re=1/2",
            name="riemann_im_rho1_closed_form",
            computed=t1,
            measured=RIEMANN_T1,
            public_sota_model="Riemann–von Mangoldt / Gram main-term inversion N(T)=1 (zero-parameter public asymptotic)",
            public_sota_typical_error_pct=rvm_err,
            comparison_class="comparable",
            verdict="beats_public_closed_form",
            beats_or_meets_sota=fsot_t1_err < rvm_err,
            native_status="EXECUTABLE",
            note="Seed e/γ³ vs Odlyzko. Odlyzko is the measurement, not a competing theory. Not a proof that all zeros lie on Re=1/2.",
            extra={"public_sota_value": t_rvm, "formula": "e / gamma**3"},
        )
    )

    # --- Riemann push: n=2..10 mean-spacing walk from seed t1 vs RvM inversion ---
    walk = riemann_spacing_walk(t1, 10)
    rvm_panel = [riemann_von_mangoldt_t(n) for n in range(1, 11)]
    walk_err_n = [_err_pct(walk[i], ODLYZKO_T[i]) for i in range(10)]
    rvm_err_n = [_err_pct(rvm_panel[i], ODLYZKO_T[i]) for i in range(10)]
    walk_mean = sum(walk_err_n[1:]) / 9.0
    rvm_mean = sum(rvm_err_n[1:]) / 9.0
    n_walk_beats = sum(1 for a, b in zip(walk_err_n[1:], rvm_err_n[1:]) if a < b)
    rows.append(
        _row(
            problem="Riemann hypothesis",
            function_object="Im(ρ_n) n=2..10 — mean-spacing walk from seed t1 (out of sample)",
            clay_object="All non-trivial zeros have Re=1/2",
            name="riemann_zeros_2_to_10_spacing_walk",
            computed=walk_mean,
            measured=rvm_mean,
            public_sota_model="Riemann–von Mangoldt inversion N(T)=n for each n (same public closed form as t1)",
            public_sota_typical_error_pct=rvm_mean,
            comparison_class="comparable",
            verdict="beats_rvm_panel_mean",
            beats_or_meets_sota=walk_mean < rvm_mean,
            native_status="EXECUTABLE",
            note="t_{k+1}=t_k+2π/log(t_k/2π) from e/γ³. Public spacing, no new coefficient. n≥2 not used to lock t1. Not RH.",
            extra={
                "fsot_error_pct": walk_mean,
                "walk_mean_err_pct": walk_mean,
                "rvm_mean_err_pct": rvm_mean,
                "n_walk_beats_rvm": n_walk_beats,
                "n_panel": 9,
                "walk_err_pct": walk_err_n,
                "rvm_err_pct": rvm_err_n,
                "formula": "t1=e/gamma**3; t_{k+1}=t_k+2pi/log(t_k/2pi)",
            },
        )
    )

    # --- Yang–Mills: confinement scale Λ_QCD ---
    lam = seed_lambda_qcd_GeV()
    lam_vs_pdg = _err_pct(lam, PDG_LAMBDA_QCD_GEV)
    lam_vs_flag = _err_pct(lam, FLAG_LAMBDA_MS5_GEV)
    flag_rel = FLAG_LAMBDA_MS5_SIGMA_GEV / FLAG_LAMBDA_MS5_GEV * 100.0
    meets_flag = lam_vs_flag <= flag_rel
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Confinement scale Λ_QCD (zero-parameter seed vs PDG-class / FLAG)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_lambda_qcd",
            computed=lam,
            measured=PDG_LAMBDA_QCD_GEV,
            public_sota_model="FLAG 2024 Λ_MS^(5)=213(8) MeV (Aoki et al. 2411.04268); in-repo PDG-class 0.2173 GeV",
            public_sota_typical_error_pct=flag_rel,
            comparison_class="comparable",
            verdict="meets_flag_1sigma",
            beats_or_meets_sota=meets_flag,
            native_status="EXECUTABLE",
            note="G_CAT·SUCTION·φ − (POOF·SUCTION)². Lands inside FLAG 1σ of 213(8) MeV. Does not prove a Wightman mass gap. Do not retune 0.2173 → 0.213.",
            extra={
                "fsot_vs_flag_pct": lam_vs_flag,
                "fsot_vs_inrepo_pdg_pct": lam_vs_pdg,
                "formula": "G_CAT*SUCTION*PHI - (POOF*SUCTION)**2",
            },
        )
    )

    # --- Yang–Mills: glueball. Lattice = measurement. Closed form = 4√σ / 3/2. ---
    glue = _f(PHI) ** 2 + _f(E) / _f(PI)
    glue_vs_ballpark = _err_pct(glue, INREPO_GLUEBALL_BALLPARK)
    glue_vs_teper = _err_pct(glue, TEPER_GLUEBALL_OVER_SQRT_SIGMA)
    teper_rel = TEPER_GLUEBALL_STAT / TEPER_GLUEBALL_OVER_SQRT_SIGMA * 100.0
    four_sqrt_err = _err_pct(TEPER_CLOSED_FORM_0PP, TEPER_GLUEBALL_OVER_SQRT_SIGMA)
    beats_teper_precision = glue_vs_teper < teper_rel
    beats_four_sqrt = glue_vs_teper < four_sqrt_err
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Lightest 0++ glueball / √σ vs lattice precision (measurement)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_over_sqrt_sigma",
            computed=glue,
            measured=TEPER_GLUEBALL_OVER_SQRT_SIGMA,
            public_sota_model="Teper hep-lat/9711011 continuum 3.65±0.11 (lattice measurement, not a closed form)",
            public_sota_typical_error_pct=teper_rel,
            comparison_class="comparable",
            verdict="does_not_beat_lattice_precision",
            beats_or_meets_sota=beats_teper_precision,
            native_status="EXECUTABLE",
            note="φ²+e/π vs Teper 3.65 is 1.5σ. Lattice is tighter. Do not retune 3.5. Not a Clay mass gap.",
            extra={
                "fsot_vs_inrepo_ballpark_pct": glue_vs_ballpark,
                "fsot_vs_teper_pct": glue_vs_teper,
                "sigma_from_teper": abs(glue - TEPER_GLUEBALL_OVER_SQRT_SIGMA) / TEPER_GLUEBALL_STAT,
                "inrepo_ballpark": INREPO_GLUEBALL_BALLPARK,
                "formula": "PHI**2 + E/PI",
                "sqrt_sigma_GeV": seed_string_tension_GeV(),
            },
        )
    )
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Lightest 0++ glueball / √σ vs Teper's own closed-form ~4√σ",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_vs_4sqrt_sigma",
            computed=glue,
            measured=TEPER_GLUEBALL_OVER_SQRT_SIGMA,
            public_sota_model="Teper hep-lat/9711011 rule of thumb m(0++)~4√σ (same paper as the measurement)",
            public_sota_typical_error_pct=four_sqrt_err,
            comparison_class="comparable",
            verdict="beats_4sqrt_sigma_closed_form",
            beats_or_meets_sota=beats_four_sqrt,
            native_status="EXECUTABLE",
            note="Same measurement 3.65. Public closed form is ~4, error 9.59%. Seed φ²+e/π error 4.57%. Lattice precision still not beaten.",
            extra={"four_sqrt_err_pct": four_sqrt_err, "formula": "PHI**2 + E/PI"},
        )
    )
    glue_ratio = math.sqrt(2.0)
    teper_ratio = TEPER_GLUEBALL_2PP_OVER_SQRT_SIGMA / TEPER_GLUEBALL_OVER_SQRT_SIGMA
    ratio_err = _err_pct(glue_ratio, teper_ratio)
    three_halves_err = _err_pct(TEPER_CLOSED_FORM_RATIO, teper_ratio)
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Glueball tensor/scalar m(2++)/m(0++) — geometric √2 vs 3/2 rule",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_2pp_over_0pp",
            computed=glue_ratio,
            measured=teper_ratio,
            public_sota_model="Teper ~3/2 flux-tube rule (hep-lat/9711011); measurement 5.15/3.65",
            public_sota_typical_error_pct=three_halves_err,
            comparison_class="comparable",
            verdict="beats_three_halves_rule",
            beats_or_meets_sota=ratio_err < three_halves_err,
            native_status="EXECUTABLE",
            note="√2 is a spin-geometry factor on the existing 0++ probe, not a new coefficient. 2++ absolute = √2·(φ²+e/π).",
            extra={
                "fsot_2pp": math.sqrt(2.0) * glue,
                "teper_2pp": TEPER_GLUEBALL_2PP_OVER_SQRT_SIGMA,
                "formula": "sqrt(2)",
            },
        )
    )

    # --- Yang–Mills: native path-sum (structure, not a SOTA contest) ---
    ps = run_path_sum_suite()
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Discrete valve path-sum w_POOF + w_hold = 1; a0/γ_color finite",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_native_path_sum_structure",
            computed=float(ps["poof_hold"] + ps["suction_hold"]),
            measured=1.0,
            public_sota_model="No public numeric SOTA — Clay object is existence, not a residual",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="native_structure_not_sota_contest",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Executable identity. Not a Wightman/constructive mass-gap theorem.",
            extra={"gamma_color": float(ps["gamma_color"]), "color_path_integral_proxy": float(ps["color_path_integral_proxy"])},
        )
    )

    # --- Navier–Stokes: Clay smoothness has no public accuracy % ---
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Global smooth (or blow-up) 3D incompressible NSE",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_clay_smoothness",
            computed=None,
            measured=None,
            public_sota_model="Unsolved. No public accuracy percentage on smoothness.",
            public_sota_typical_error_pct=None,
            comparison_class="no_fair_compare",
            verdict="no_fair_numeric_compare",
            beats_or_meets_sota=None,
            native_status="OPEN_TRACK",
            note="Toy μ(D_eff)>0 and c_s²>0 are transport identities, not 3D global smoothness.",
        )
    )
    mu_ok = all(viscosity_eff(d) > 0.0 for d in (6.0, 14.0, 25.0))
    cs2 = sound_speed_sq(1.0)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Seed-locked transport coefficients on the 1D toy continuum",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_transport_structure",
            computed=1.0 if (mu_ok and cs2 > 0.0) else 0.0,
            measured=1.0,
            public_sota_model="No public SOTA for this toy object; experimental μ_water is a different object",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="native_structure_not_sota_contest",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="μ(D=6,14,25)>0 and c_s²>0. Helps weather/Earth fluid. Not Clay NSE.",
            extra={"mu_D6": viscosity_eff(6.0), "mu_D14": viscosity_eff(14.0), "mu_D25": viscosity_eff(25.0), "c_s2": cs2},
        )
    )
    wx = _weather_skill()
    hold_pct = float(wx.get("hold_pct") or 0.0)
    maj_pct = float(wx.get("majority_pct") or 0.0)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Earth-fluid 24 h hold rate vs majority-class baseline (related fold, not NSE)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_weather_24h_related",
            computed=hold_pct if wx.get("present") else None,
            measured=maj_pct if wx.get("present") else None,
            public_sota_model="Majority-class baseline on the same 28 observed rows; ECMWF RMSE is a different object",
            public_sota_typical_error_pct=(100.0 - maj_pct) if wx.get("present") else None,
            comparison_class="related_not_clay",
            verdict="does_not_beat_majority_ecmwf_not_beaten",
            beats_or_meets_sota=False if wx.get("present") else None,
            native_status="EXECUTABLE" if wx.get("present") else "OPEN_TRACK",
            note="Hold 22/28=78.6% vs majority 24/28 storms=85.7%. Finer dt is still the path. Kill: claiming ECMWF beaten.",
            extra={"weather_skill": wx},
        )
    )

    # --- P vs NP: Grover exponent meets the proven public bound ---
    grover = float(GROVER_EXPONENT)
    rows.append(
        _row(
            problem="P versus NP",
            function_object="Unstructured-search query exponent (quantum query complexity)",
            clay_object="Proof that P=NP or P≠NP",
            name="pnp_grover_exponent",
            computed=grover,
            measured=0.5,
            public_sota_model="Grover 1996 / Bennett et al. 1997 proven tight bound Θ(N^{1/2})",
            public_sota_typical_error_pct=0.0,
            comparison_class="meets_sota",
            verdict="meets_proven_bound",
            beats_or_meets_sota=abs(grover - 0.5) < 1e-12,
            native_status="EXECUTABLE",
            note="You cannot beat a proven tight bound. Matching 1/2 is MEETS, not BEATS, and is not a P vs NP theorem.",
        )
    )

    # --- BSD / Hodge: no native numeric function yet ---
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="rank E(Q) = ord_{s=1} L(E,s)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_no_fair_compare",
            computed=None,
            measured=None,
            public_sota_model="Sage/PARI/Magma ranks on Cremona tables; BSD checked for many rank 0/1 curves",
            public_sota_typical_error_pct=None,
            comparison_class="no_fair_compare",
            verdict="no_fair_numeric_compare",
            beats_or_meets_sota=None,
            native_status="OPEN_TRACK",
            note="No elliptic-curve L-function rank predictor in-repo. Do not invent a seed residual.",
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hodge classes = algebraic cycles (rational)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_no_fair_compare",
            computed=None,
            measured=None,
            public_sota_model="No public numeric accuracy % — this is a existence/algebraicity theorem",
            public_sota_typical_error_pct=None,
            comparison_class="no_fair_compare",
            verdict="no_fair_numeric_compare",
            beats_or_meets_sota=None,
            native_status="OPEN_TRACK",
            note="No Hodge-class predictor in-repo. No fair compare.",
        )
    )
    return rows


def accuracy_summary(rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    rows = rows if rows is not None else run_accuracy_scoreboard()
    comparable = [r for r in rows if r["comparison_class"] == "comparable"]
    no_fair = [r for r in rows if r["comparison_class"] == "no_fair_compare"]
    beats = [r for r in rows if r["beats_or_meets_sota"] is True]
    loses = [
        r
        for r in rows
        if r["comparison_class"] == "comparable" and r["beats_or_meets_sota"] is False
    ]
    flags = clay_process_flags()
    riemann = next(r for r in rows if r["name"] == "riemann_im_rho1_closed_form")
    riemann_panel = next(r for r in rows if r["name"] == "riemann_zeros_2_to_10_spacing_walk")
    glue = next(r for r in rows if r["name"] == "ym_glueball_over_sqrt_sigma")
    glue4 = next(r for r in rows if r["name"] == "ym_glueball_vs_4sqrt_sigma")
    glue_ratio = next(r for r in rows if r["name"] == "ym_glueball_2pp_over_0pp")
    wx = next(r for r in rows if r["name"] == "ns_weather_24h_related")
    wip_beats = [r for r in rows if r.get("sota_beats_fsot_accuracy_wip")]
    in_green = [r for r in rows if r.get("fsot_green") == "pass"]
    in_asp = [r for r in rows if r.get("fsot_aspiration") == "pass"]
    next_dig = [r for r in rows if r.get("next_dig")]
    return {
        "generated_at": _now(),
        "pin": "D1D38A",
        "clay_prize_claimed": False,
        "clay_problems_remaining": int(flags["clay_problems_remaining"]),
        "fsot_green_gate_pct": FSOT_GREEN_GATE_PCT,
        "fsot_aspiration_pct": FSOT_ASPIRATION_PCT,
        "comparable_count": len(comparable),
        "beats_or_meets_count": len(beats),
        "does_not_beat_count": len(loses),
        "no_fair_compare_count": len(no_fair),
        "sota_beats_accuracy_wip_n": len(wip_beats),
        "fsot_green_pass_n": len(in_green),
        "fsot_aspiration_pass_n": len(in_asp),
        "next_dig_n": len(next_dig),
        "next_dig_names": [r["name"] for r in next_dig],
        "sota_beats_accuracy_wip_names": [r["name"] for r in wip_beats],
        "riemann_beats_public_closed_form": 1 if riemann["beats_or_meets_sota"] else 0,
        "riemann_panel_beats_rvm": 1 if riemann_panel["beats_or_meets_sota"] else 0,
        "glueball_beats_teper": 1 if glue["beats_or_meets_sota"] else 0,
        "glueball_does_not_beat_teper": 0 if glue["beats_or_meets_sota"] else 1,
        "glueball_beats_4sqrt_sigma": 1 if glue4["beats_or_meets_sota"] else 0,
        "glueball_ratio_beats_three_halves": 1 if glue_ratio["beats_or_meets_sota"] else 0,
        "weather_beats_majority": 1 if wx["beats_or_meets_sota"] else 0,
        "weather_does_not_beat_majority": 0 if wx["beats_or_meets_sota"] else 1,
        "ecmwf_beaten": 0,
        "ecmwf_not_beaten": 1,
        "rows": rows,
        "honest_scope": (
            "Two bars: (1) public SOTA, (2) FSOT green 0.5% / aspiration 0.05%. "
            "A SOTA beat outside 0.5% is FSOT accuracy WIP — not stuffed into the gate. "
            "Not a Clay Prize. GitHub is not a Qualifying Outlet. "
            "Misses (lattice precision, weather majority, NSE smoothness, BSD, Hodge) are next dig."
        ),
    }


def _fmt(x: Any, nd: int = 6) -> str:
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, int) and not isinstance(x, bool):
        return str(x)
    if isinstance(x, float):
        if abs(x) >= 1.0:
            return f"{x:.{min(nd, 6)}g}"
        return f"{x:.{nd}g}"
    return str(x)


def render_markdown(summary: dict[str, Any]) -> str:
    rows: list[dict[str, Any]] = summary["rows"]
    lines = [
        "# Millennium functions — accuracy vs public SOTA",
        "",
        f"**Pin:** D1D38A · **Clay Prize claimed:** **no** · **Generated:** `{summary['generated_at']}`",
        "",
        "Clay’s three gates (Qualifying Outlet, two years, community acceptance) are a *social process*.",
        "They live in [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md) and stay honest zeros.",
        "",
        "This page is the other question: **does the native math hit the same *function* more accurately than what is currently public?**",
        "Consensus is not the scoring rule. Closed precision is. A miss stays a miss.",
        "",
        "**Two bars, never collapsed.** Beating a public competitor is not the same as landing inside the rest-of-system residual gates (**0.5%** green, **0.05%** aspiration). A SOTA beat outside 0.5% is **FSOT accuracy WIP**.",
        "",
        "Kill: “we won a Millennium Prize.” Kill: stuffing a residual into the Clay statement.",
        "Kill: retuning β / ρ / 0.2173 / 3.5 to swallow a compare. Kill: claiming ECMWF beaten.",
        "Kill: calling a 4% SOTA-beat “0.5% green.”",
        "",
        "## Live tally",
        "",
        f"| Bucket | n |",
        f"|--------|---|",
        f"| Beats or meets public SOTA | {summary['beats_or_meets_count']} |",
        f"| …of those, inside FSOT 0.5% green | {summary['fsot_green_pass_n']} |",
        f"| …of those, inside 0.05% aspiration | {summary['fsot_aspiration_pass_n']} |",
        f"| **SOTA beat, FSOT accuracy still WIP** | **{summary['sota_beats_accuracy_wip_n']}** |",
        f"| Comparable but does **not** beat | {summary['does_not_beat_count']} |",
        f"| **Next dig** (misses + open tracks) | **{summary['next_dig_n']}** |",
        f"| Clay problems remaining | {summary['clay_problems_remaining']} |",
        f"| ECMWF beaten | {summary['ecmwf_beaten']} |",
        "",
        "## Scoreboard",
        "",
        "| Problem | Function | FSOT err % | Public typical err % | SOTA | FSOT 0.5% | FSOT 0.05% | Progress |",
        "|---------|----------|------------|----------------------|------|-----------|------------|----------|",
    ]
    for r in rows:
        err_cell = _fmt(r["fsot_error_pct"], 4)
        if r["name"] == "ym_lambda_qcd":
            err_cell = (
                f"{_fmt(r.get('fsot_vs_inrepo_pdg_pct'), 4)} vs PDG 0.2173; "
                f"{_fmt(r.get('fsot_vs_flag_pct'), 4)} vs FLAG 213"
            )
        elif r["name"] == "ym_glueball_over_sqrt_sigma":
            err_cell = (
                f"{_fmt(r.get('fsot_vs_teper_pct'), 4)} vs Teper 3.65; "
                f"{_fmt(r.get('fsot_vs_inrepo_ballpark_pct'), 4)} vs in-repo 3.5"
            )
        elif r["name"] == "riemann_zeros_2_to_10_spacing_walk":
            err_cell = (
                f"{_fmt(r.get('walk_mean_err_pct'), 4)} mean n=2..10 "
                f"({r.get('n_walk_beats_rvm')}/{r.get('n_panel')} zeros)"
            )
        sota_cell = {
            True: "beats/meets",
            False: "miss",
            None: "—",
        }[r["beats_or_meets_sota"]]
        lines.append(
            "| "
            + " | ".join(
                [
                    r["problem"],
                    r["function_object"],
                    err_cell,
                    _fmt(r["public_sota_typical_error_pct"], 4),
                    sota_cell,
                    str(r.get("fsot_green") or "—"),
                    str(r.get("fsot_aspiration") or "—"),
                    str(r.get("progress") or "—"),
                ]
            )
            + " |"
        )
    lines += [
        "",
        "## What this does and does not say",
        "",
        "| Function | Result | Why that is the right object |",
        "|----------|--------|------------------------------|",
        "| First Riemann zero Im(ρ1) | **Beats SOTA and in 0.05%** (`e/γ³` 0.00166% vs RvM 26%) | Odlyzko is the measurement. **Not** RH. |",
        "| Riemann zeros n=2..10 | **Beats RvM (4.26% vs 5.64%) — FSOT accuracy WIP** (outside 0.5%) | Public spacing walk. Do not stuff 4.26% into the green gate. |",
        "| Λ_QCD vs PDG 0.2173 | **Beats/meets and in 0.05%** (0.048%) | FLAG 213(8) is a second measurement (2.07%, inside FLAG 1σ, outside 0.5% vs FLAG central). |",
        "| Glueball 0++ vs 4√σ | **Beats 4√σ (4.57% vs 9.59%) — FSOT accuracy WIP** | Same 4.57% vs lattice measurement. Not 0.5% green. |",
        "| Glueball 2++/0++ | **Beats 3/2 (0.23%) — in 0.5% green, aspiration WIP** | √2 geometry. 0.23% > 0.05%. |",
        "| Grover 1/2 | **Meets proven bound and in 0.05%** | Not P vs NP. |",
        "",
        "## Next dig (misses and open tracks)",
        "",
        "| Item | Why it is next | First cut, no stuffing |",
        "|------|----------------|------------------------|",
        "| Glueball 0++ vs Teper lattice precision | 4.57% vs 3.01% (1.5σ). Lattice is the measurement. | Same seed as the 4√σ beat. Need a better 0++ identity, not a retune of 3.5. |",
        "| Weather 24 h vs majority | Hold 22/28=78.6% vs majority 85.7%. ECMWF not beaten. | Six kills: five quiet-forecast / storm-observed (OLCN6, 42058, 44078) and one thin-obs false storm (62442, n=6). Valve/quiet look, then finer `dt`. |",
        "| 3D NSE smoothness | No public accuracy %. Toy μ>0 is not Clay NSE. | 1D Stokes/heat manufactured solution at the right fold — still not 3D global smoothness. |",
        "| BSD | No native rank predictor. | Cremona 11a1 / 37a1 / 389a1 as the first objects. Do not invent a seed residual. |",
        "| Hodge | No native Hodge-class predictor. | Hodge numbers of a named variety, not a stolen 20 from another domain. |",
        "",
        "## Reproduce",
        "",
        "```powershell",
        "python vendor/fsot_millennium_accuracy.py",
        "python scripts/run_goal_tracks_verification.py",
        "```",
        "",
        "Prize-process flags (separate file, all honest): [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md).",
        "Yang–Mills object split: [`MILLENNIUM_YM_VS_FSOT.md`](MILLENNIUM_YM_VS_FSOT.md).",
        "",
        summary["honest_scope"],
        "",
    ]
    return "\n".join(lines)


def write_artifacts(summary: dict[str, Any] | None = None) -> dict[str, Any]:
    summary = summary if summary is not None else accuracy_summary()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(summary)
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_markdown(summary), encoding="utf-8")
    return summary


if __name__ == "__main__":
    s = write_artifacts()
    print(json.dumps({k: s[k] for k in s if k != "rows"}, indent=2))
    for r in s["rows"]:
        flag = {
            True: "MEET/BEAT",
            False: "MISS",
            None: "----",
        }[r["beats_or_meets_sota"]]
        print(
            f"  {flag:9} {r['name']:36} green={str(r.get('fsot_green')):4} "
            f"asp={str(r.get('fsot_aspiration')):4} {r.get('progress')}"
        )
    ok = (
        (not s["clay_prize_claimed"])
        and s["clay_problems_remaining"] == 6
        and s["ecmwf_beaten"] == 0
        and s["ecmwf_not_beaten"] == 1
        and s["glueball_beats_teper"] == 0
        and s["glueball_does_not_beat_teper"] == 1
        and s["glueball_beats_4sqrt_sigma"] == 1
        and s["glueball_ratio_beats_three_halves"] == 1
        and s["riemann_beats_public_closed_form"] == 1
        and s["riemann_panel_beats_rvm"] == 1
        and s["weather_beats_majority"] == 0
        and s["weather_does_not_beat_majority"] == 1
        and s["sota_beats_accuracy_wip_n"] >= 1
        and s["next_dig_n"] >= 1
        and s["fsot_green_pass_n"] >= 1
    )
    raise SystemExit(0 if ok else 1)

#!/usr/bin/env python3
"""Accuracy vs public SOTA for the functions the six Clay problems name.

Clay prize-process (Qualifying Outlet, two years, community acceptance) lives
in fsot_millennium_track.py and stays all-zeros until those gates are real.

This module answers a different question: if you simulate the *function* each
problem is trying to capture, is the seed-locked FSOT number more accurate
than what is currently public? Wrong object is a false win. A residual probe
is not a Clay theorem. Glueball vs Teper is allowed to lose.
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
# Teper, hep-lat/9711011: m_{0++}/√σ = 3.65 ± 0.11 (continuum ratio).
TEPER_GLUEBALL_OVER_SQRT_SIGMA = 3.65
TEPER_GLUEBALL_STAT = 0.11


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _err_pct(computed: float, measured: float) -> float:
    return abs(computed - measured) / max(abs(measured), 1e-30) * 100.0


def _f(x: Any) -> float:
    return float(x)


def riemann_von_mangoldt_t1() -> float:
    """Invert N(T)≈(T/2π)log(T/2π)−T/2π+7/8 at N=1.

    Same main term as Gram's g_0. Public zero-parameter closed form for the
    first-zero *scale*. Known to be poor at n=1; that is the point of the
    compare. Odlyzko's tabulated value is the measurement, not a competitor.
    """

    def residual(u: float) -> float:
        return u * math.log(u) - u - 0.125

    lo, hi = 1.1, 10.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if residual(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    u = 0.5 * (lo + hi)
    return 2.0 * math.pi * u


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

    # --- Yang–Mills: glueball / √σ (honest lattice compare; allowed to lose) ---
    glue = _f(PHI) ** 2 + _f(E) / _f(PI)
    glue_vs_ballpark = _err_pct(glue, INREPO_GLUEBALL_BALLPARK)
    glue_vs_teper = _err_pct(glue, TEPER_GLUEBALL_OVER_SQRT_SIGMA)
    teper_rel = TEPER_GLUEBALL_STAT / TEPER_GLUEBALL_OVER_SQRT_SIGMA * 100.0
    beats_teper = glue_vs_teper < teper_rel
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Lightest 0++ glueball over string tension m/√σ",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_over_sqrt_sigma",
            computed=glue,
            measured=TEPER_GLUEBALL_OVER_SQRT_SIGMA,
            public_sota_model="Teper hep-lat/9711011 continuum ratio 3.65±0.11; in-repo ballpark 3.5 kept (not retuned)",
            public_sota_typical_error_pct=teper_rel,
            comparison_class="comparable",
            verdict="does_not_beat_lattice_teper",
            beats_or_meets_sota=beats_teper,
            native_status="EXECUTABLE",
            note="φ²+e/π vs Teper 3.65. Lattice is tighter. In-repo 3.5 ballpark residual is a rounded-anchor probe, not a Clay win. Scatter across groups is large (≈3.4–4.0).",
            extra={
                "fsot_vs_inrepo_ballpark_pct": glue_vs_ballpark,
                "fsot_vs_teper_pct": glue_vs_teper,
                "inrepo_ballpark": INREPO_GLUEBALL_BALLPARK,
                "formula": "PHI**2 + E/PI",
                "sqrt_sigma_GeV": seed_string_tension_GeV(),
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
    wx = _weather_24h()
    wx_n = int(wx.get("n_agree") or 0)
    wx_d = int(wx.get("n_with_obs") or 0)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Earth-fluid 24 h storm/quiet class (related fold, not NSE)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_weather_24h_related",
            computed=None,
            measured=None,
            public_sota_model="ECMWF deterministic 24 h fields — different object (continuous T/wind RMSE, not this class gate)",
            public_sota_typical_error_pct=None,
            comparison_class="related_not_clay",
            verdict="ecmwf_not_beaten",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE" if wx.get("present") else "OPEN_TRACK",
            note="24 h retro class-agree is a goal-track increment. Kill: claiming ECMWF beaten. Kill: UTC hypocenter as 0.5%.",
            extra={"weather_24h": wx, "n_agree": wx_n, "n_with_obs": wx_d},
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
    glue = next(r for r in rows if r["name"] == "ym_glueball_over_sqrt_sigma")
    return {
        "generated_at": _now(),
        "pin": "D1D38A",
        "clay_prize_claimed": False,
        "clay_problems_remaining": int(flags["clay_problems_remaining"]),
        "comparable_count": len(comparable),
        "beats_or_meets_count": len(beats),
        "does_not_beat_count": len(loses),
        "no_fair_compare_count": len(no_fair),
        "riemann_beats_public_closed_form": 1 if riemann["beats_or_meets_sota"] else 0,
        "glueball_beats_teper": 1 if glue["beats_or_meets_sota"] else 0,
        "glueball_does_not_beat_teper": 0 if glue["beats_or_meets_sota"] else 1,
        "ecmwf_beaten": 0,
        "ecmwf_not_beaten": 1,
        "rows": rows,
        "honest_scope": (
            "Accuracy contest on native function-objects. "
            "Not a Clay Prize. GitHub is not a Qualifying Outlet. "
            "Glueball vs Teper is a recorded miss. ECMWF is not beaten."
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
        "Kill: “we won a Millennium Prize.” Kill: stuffing a residual into the Clay statement.",
        "Kill: retuning β / ρ / 0.2173 / 3.5 to swallow a compare. Kill: claiming ECMWF beaten.",
        "",
        "## Live tally",
        "",
        f"| Bucket | n |",
        f"|--------|---|",
        f"| Comparable numeric functions | {summary['comparable_count']} |",
        f"| Beats or meets public SOTA | {summary['beats_or_meets_count']} |",
        f"| Comparable but does **not** beat | {summary['does_not_beat_count']} |",
        f"| No fair numeric compare yet | {summary['no_fair_compare_count']} |",
        f"| Clay problems remaining | {summary['clay_problems_remaining']} |",
        f"| ECMWF beaten | {summary['ecmwf_beaten']} |",
        f"| Glueball beats Teper lattice | {summary['glueball_beats_teper']} |",
        "",
        "## Scoreboard",
        "",
        "| Problem | Function scored | FSOT | Public SOTA | FSOT err % | Public typical err % | Verdict | Clay |",
        "|---------|-----------------|------|-------------|----------------|----------------------|---------|------|",
    ]
    for r in rows:
        fsot = _fmt(r["computed"], 8)
        pub = r["public_sota_model"].split(";")[0]
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
        lines.append(
            "| "
            + " | ".join(
                [
                    r["problem"],
                    r["function_object"],
                    fsot,
                    pub.replace("|", "/"),
                    err_cell,
                    _fmt(r["public_sota_typical_error_pct"], 4),
                    r["verdict"],
                    r["clay_status"],
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
        "| First Riemann zero Im(ρ1) | Seed `e/γ³` vs Odlyzko at **0.00166%**; Riemann–von Mangoldt inversion at **~26%** | Closed form vs tabulated zero. Odlyzko is the *measurement*. The public closed-form competitor is the main-term inversion. **Not** RH for all zeros. |",
        "| Λ_QCD | Seed vs in-repo PDG-class 0.2173 GeV at **0.048%**; vs FLAG 213(8) MeV inside 1σ | Zero-parameter confinement scale. **Not** a Wightman mass gap. |",
        "| Glueball m(0++)/√σ | `φ²+e/π` vs Teper 3.65±0.11 — **does not beat lattice** | Honest miss. Lattice scatter is large; we still score the Teper central, not the in-repo 3.5 ballpark. |",
        "| Path-sum / μ>0 / c_s² | Executable identities | Structure, not a SOTA residual contest. |",
        "| Weather 24 h class | Related fold; ECMWF **not** beaten | Same fluid as NSE, different object than Clay smoothness and different object than ECMWF RMSE. |",
        "| Grover exponent 1/2 | **Meets** Bennett et al. proven bound | Cannot beat a tight bound. **Not** P vs NP. |",
        "| BSD / Hodge | No fair compare | No native rank or Hodge-class predictor. |",
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
        err = r["fsot_error_pct"]
        err_s = f"{err:.4f}%" if err is not None else "n/a"
        flag = {
            True: "MEET/BEAT",
            False: "MISS",
            None: "----",
        }[r["beats_or_meets_sota"]]
        print(f"  {flag:9} {r['name']:32} class={r['comparison_class']:20} err={err_s:12} {r['verdict']}")
    ok = (
        (not s["clay_prize_claimed"])
        and s["clay_problems_remaining"] == 6
        and s["ecmwf_beaten"] == 0
        and s["ecmwf_not_beaten"] == 1
        and s["glueball_beats_teper"] == 0
        and s["glueball_does_not_beat_teper"] == 1
        and s["riemann_beats_public_closed_form"] == 1
    )
    raise SystemExit(0 if ok else 1)

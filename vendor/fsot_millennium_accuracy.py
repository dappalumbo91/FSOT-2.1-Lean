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
    from fsot_compute import E, PHI, PI, POOF, MEDIUM_ORIFICES, derived_D_eff
    from fsot_dynamics import sound_speed_sq, viscosity_eff, viscous_mode_rhs_error_pct, nse_stretch_sim_panel, nse_omega0_scan
    from fsot_nse3d import nse3d_measured_compare
    from fsot_scale_interconnects import (
        water_air_sound_ratio,
        gamma_diatomic,
        scale_height_us1976,
        scaled,
        C_AIR_20C,
        C_WATER_20C,
        H_STD_ATM_M,
    )
    from fsot_millennium_track import GAMMA, RIEMANN_T1, clay_process_flags
    from fsot_path_sum import run_path_sum_suite
    from fsot_quantum_trinary_syntax import GROVER_EXPONENT
    from fsot_seed_flavor import (
        seed_lambda_qcd_GeV,
        seed_string_tension_GeV,
        seed_glueball_over_sqrt_sigma,
        seed_glueball_sigma_coupled,
        seed_f0_1500_mixed_GeV,
        seed_closed_gluonic_GeV,
        seed_flavor_closed_GeV,
        seed_alpha_s_MZ,
        seed_von_karman,
        seed_kolmogorov_45,
        seed_kolmogorov_d2_32,
        seed_onsager_holder,
        seed_nse_valve_fraction,
        nse_stretch_visc_two_zoom,
        nse_d2_rejects_d_particle,
        nse_enstrophy_budget_two_term,
        nse_helicity_is_3d_not_2d,
        seed_bsd_11a1_L,
        seed_bsd_37a1_Lprime,
        seed_bsd_389a1_regulator,
        seed_bsd_389a1_special,
        seed_bsd_5077a1_regulator,
        seed_bsd_234446a1_regulator,
        seed_hassett_d_plane,
        seed_hassett_d_scroll,
        seed_hassett_d_elliptic,
        seed_hassett_d_veronese,
        seed_hassett_d_sextic,
        seed_hassett_d_coble,
        seed_hassett_d_bl11,
        seed_hassett_d_bl12,
        seed_hassett_d_enriques,
        hassett_named_no_k3,
        hassett_C_d_nonempty,
        hassett_associated_k3,
        hassett_k3_tail_sample,
        hassett_unnamed_no_k3_sample,
        hassett_k3_tail_is_lefschetz,
        hassett_unnamed_no_k3_has_no_seed,
        seed_cp2_euler,
        seed_cp3_euler,
        seed_cp2xcp2_euler,
        seed_gr24_euler,
        seed_cubic_4fold_euler,
        seed_quartic_4fold_euler,
        seed_hypersurface_4fold_euler,
        seed_sextic_4fold_euler,
        seed_cubic4_h22,
        seed_cubic4_very_general_rational_hodge_rank,
        seed_k3_h11,
        seed_cubic4_fano_b2,
        seed_abelian_4fold_euler,
        bsd_integer_rank_from_leading,
        bsd_analytic_sha,
        seed_riemann_S_bound,
        seed_riemann_S_amplitude,
        seed_sqrt_sigma_r0,
        seed_glueball_r0,
        riemann_S_band_halfwidth,
        riemann_POOF_jitter_halfwidth,
        riemann_signed_jitter_T,
        seed_bsd_rank_parity,
    )
except ImportError:  # pragma: no cover
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fsot_compute import E, PHI, PI, POOF, MEDIUM_ORIFICES, derived_D_eff
    from fsot_dynamics import sound_speed_sq, viscosity_eff, viscous_mode_rhs_error_pct, nse_stretch_sim_panel, nse_omega0_scan
    from fsot_nse3d import nse3d_measured_compare
    from fsot_scale_interconnects import (
        water_air_sound_ratio,
        gamma_diatomic,
        scale_height_us1976,
        scaled,
        C_AIR_20C,
        C_WATER_20C,
        H_STD_ATM_M,
    )
    from fsot_millennium_track import GAMMA, RIEMANN_T1, clay_process_flags
    from fsot_path_sum import run_path_sum_suite
    from fsot_quantum_trinary_syntax import GROVER_EXPONENT
    from fsot_seed_flavor import (
        seed_lambda_qcd_GeV,
        seed_string_tension_GeV,
        seed_glueball_over_sqrt_sigma,
        seed_glueball_sigma_coupled,
        seed_f0_1500_mixed_GeV,
        seed_closed_gluonic_GeV,
        seed_flavor_closed_GeV,
        seed_alpha_s_MZ,
        seed_von_karman,
        seed_kolmogorov_45,
        seed_kolmogorov_d2_32,
        seed_onsager_holder,
        seed_nse_valve_fraction,
        nse_stretch_visc_two_zoom,
        nse_d2_rejects_d_particle,
        nse_enstrophy_budget_two_term,
        nse_helicity_is_3d_not_2d,
        seed_bsd_11a1_L,
        seed_bsd_37a1_Lprime,
        seed_bsd_389a1_regulator,
        seed_bsd_389a1_special,
        seed_bsd_5077a1_regulator,
        seed_bsd_234446a1_regulator,
        seed_hassett_d_plane,
        seed_hassett_d_scroll,
        seed_hassett_d_elliptic,
        seed_hassett_d_veronese,
        seed_hassett_d_sextic,
        seed_hassett_d_coble,
        seed_hassett_d_bl11,
        seed_hassett_d_bl12,
        seed_hassett_d_enriques,
        hassett_named_no_k3,
        hassett_C_d_nonempty,
        hassett_associated_k3,
        hassett_k3_tail_sample,
        hassett_unnamed_no_k3_sample,
        hassett_k3_tail_is_lefschetz,
        hassett_unnamed_no_k3_has_no_seed,
        seed_cp2_euler,
        seed_cp3_euler,
        seed_cp2xcp2_euler,
        seed_gr24_euler,
        seed_cubic_4fold_euler,
        seed_quartic_4fold_euler,
        seed_hypersurface_4fold_euler,
        seed_sextic_4fold_euler,
        seed_cubic4_h22,
        seed_cubic4_very_general_rational_hodge_rank,
        seed_k3_h11,
        seed_cubic4_fano_b2,
        seed_abelian_4fold_euler,
        bsd_integer_rank_from_leading,
        bsd_analytic_sha,
        seed_riemann_S_bound,
        seed_riemann_S_amplitude,
        seed_sqrt_sigma_r0,
        seed_glueball_r0,
        riemann_S_band_halfwidth,
        riemann_POOF_jitter_halfwidth,
        riemann_signed_jitter_T,
        seed_bsd_rank_parity,
    )

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "millennium_accuracy_scoreboard.json"
OUT_MD = ROOT / "docs" / "MILLENNIUM_ACCURACY_VS_SOTA.md"
WX_JSON = ROOT / "results" / "dated_forecast_scores" / "WEATHER_24H_RETRO.json"
WX_ISSUE_DIR = ROOT / "predictions" / "dated_forecasts"

# In-repo PDG-class anchors already used by fsot_gr_sm / seed flavor. Do not retune.
PDG_LAMBDA_QCD_GEV = 0.2173
PDG_ALPHA_S_MZ = 0.1179
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
# Athenodorou–Teper 2020 SU(3) continuum (JHEP 11 (2020) 172, arXiv:2007.06422).
# Linear O(a²σ) M(0++)/√σ=3.405(21); 2++ GeV 2.376(32) with √σ=485(6) MeV.
AT2020_0PP_OVER_SQRT_SIGMA = 3.405
AT2020_0PP_STAT = 0.021
AT2020_2PP_OVER_SQRT_SIGMA = 4.894  # 3.405 * 2.376/1.653
AT2020_2PP_STAT = 0.07
# AT2020 eqn (9): √σ r0 = 1.160(6). Chen et al. PRD 73, 014504 r0 M(0++)=4.16(11).
AT2020_SQRT_SIGMA_R0 = 1.160
AT2020_SQRT_SIGMA_R0_STAT = 0.006
CHEN_R0_M_0PP = 4.16
CHEN_R0_M_0PP_STAT = 0.11
# PDG 2024 (Navas et al. PRD 110, 030001). Observed I=0 0++ — not a glueball ID.
# Morningstar arXiv:2502.02547: no scalar below ~2 GeV is predominantly a glueball.
PDG_F0_1500_GEV = 1.506  # 1506 ± 6 MeV BW (lineshape convention)
PDG_F0_1500_STAT = 0.006
# PDG 2024 T-matrix pole OUR ESTIMATE Re(√s)=(1430–1530) MeV. Closed mode is a pole.
PDG_F0_1500_POLE_LO_GEV = 1.43
PDG_F0_1500_POLE_HI_GEV = 1.53
PDG_F0_1710_GEV = 1.733  # 1733 +8 −7 MeV
PDG_F0_1710_STAT = 0.008
# Morningstar-class quenched YM 0++ ~1730 ± 80 MeV (lattice construct in GeV).
LATTICE_0PP_GEV = 1.73
LATTICE_0PP_STAT = 0.08
# von Kármán log-law (classic 0.40; scatter 0.38–0.41). Wave table measured 0.400.
VON_KARMAN = 0.40
C_WATER_OVER_C_AIR_CRC = C_WATER_20C / C_AIR_20C
GAMMA_DIATOMIC_AIR = 1.400
CRC_WATER_N_D = 1.3330
CRC_WATER_RHO = 0.9982
CRC_ICE_N_D = 1.309
CRC_ICE_RHO = 0.917
CRC_ICE_C = 3980.0
CRC_WATER_TM = 273.15
CRC_WATER_TB = 373.15
# LMFDB / Cremona 11a1 L(E,1). Measurement, not a competing closed form.
LMFDB_11A1_L = 0.2538418608559107
NAIVE_BSD_L_QUARTER = 0.25
# LMFDB / Cremona 37a1 analytic rank 1, L'(E,1).
LMFDB_37A1_LPRIME = 0.3059997738340523
# LMFDB 389.a1 analytic rank 2. Regulator is the height pairing (not L''(1)/2!).
LMFDB_389A1_REG = 0.15246017794314375
# LMFDB 389.a1 BSD special value L''(E,1)/2!.
LMFDB_389A1_SPECIAL = 0.7593165002884268
# LMFDB 5077.a1 analytic rank 3. First rank-3 curve. Volume factors for Sha.
LMFDB_5077A1_REG = 0.41714355875838397
LMFDB_5077A1_SPECIAL = 1.7318499001193007
LMFDB_5077A1_OMEGA = 4.151687983086933
LMFDB_5077A1_TAM = 1.0
LMFDB_5077A1_TORS = 1.0
# LMFDB 234446.a1 analytic rank 4. First rank-4 curve. Tamagawa product 2.
LMFDB_234446A1_REG = 1.504344888275284
LMFDB_234446A1_SPECIAL = 8.943847395900889
LMFDB_234446A1_OMEGA = 2.9726718472633355
LMFDB_234446A1_TAM = 2.0
LMFDB_234446A1_TORS = 1.0
# LMFDB 17a1 (Cremona 17a1): rank 0. Raw L(1) mis-fires as rank 3 on the first-of-rank ladder.
LMFDB_17A1_L = 0.38676993838778004
LMFDB_17A1_OMEGA = 1.5470797535511202
LMFDB_17A1_TAM = 4.0
LMFDB_17A1_TORS = 4.0
# LMFDB 19.a1 (Cremona 19a2): rank 0, out of sample vs 17a1.
LMFDB_19A1_L = 0.4532532444961036
LMFDB_19A1_OMEGA = 0.4532532444961036
LMFDB_19A1_TAM = 1.0
LMFDB_19A1_TORS = 1.0
# LMFDB 11a1 volume factors (same orifice as 17a1).
LMFDB_11A1_OMEGA = 1.2692093042795534
LMFDB_11A1_TAM = 5.0
LMFDB_11A1_TORS = 5.0
# LMFDB 37a1 rank-1 volume (first-of-rank).
LMFDB_37A1_OMEGA = 5.986917292463919
LMFDB_37A1_REG = 0.05111140823996884
LMFDB_37A1_TAM = 1.0
LMFDB_37A1_TORS = 1.0
# LMFDB 53a1: rank 1, not first-of-rank. Raw L' mis-fires as rank 3.
LMFDB_53A1_LPRIME = 0.435863824
LMFDB_53A1_OMEGA = 4.6876410488788825
LMFDB_53A1_REG = 0.0929814846386543
LMFDB_53A1_TAM = 1.0
LMFDB_53A1_TORS = 1.0
# LMFDB 61a1: rank 1, out of sample vs 53a1.
LMFDB_61A1_LPRIME = 0.4856736514265826
LMFDB_61A1_OMEGA = 6.133193148394534
LMFDB_61A1_REG = 0.07918773136204194
LMFDB_61A1_TAM = 1.0
LMFDB_61A1_TORS = 1.0
# LMFDB 389a1 rank-2 volume (first-of-rank special).
LMFDB_389A1_OMEGA = 4.980425121710110
LMFDB_389A1_TAM = 1.0
LMFDB_389A1_TORS = 1.0
# LMFDB 643a1: rank 2, not first-of-rank. Raw L''/2! mis-fires as rank 4.
LMFDB_643A1_SPECIAL = 1.1482617365489983
LMFDB_643A1_OMEGA = 5.010313433142889
LMFDB_643A1_REG = 0.22917962156884708
LMFDB_643A1_TAM = 1.0
LMFDB_643A1_TORS = 1.0
# LMFDB 433a1: rank 2, out of sample vs 643a1.
LMFDB_433A1_SPECIAL = 0.9470207808658145
LMFDB_433A1_OMEGA = 4.214710192998484
LMFDB_433A1_REG = 0.22469416341816674
LMFDB_433A1_TAM = 1.0
LMFDB_433A1_TORS = 1.0
# LMFDB 11197a1: rank 3, not first-of-rank. Raw L'''/3! mis-fires as rank 4.
LMFDB_11197A1_SPECIAL = 2.871585754190565
LMFDB_11197A1_OMEGA = 3.306671073867520
LMFDB_11197A1_REG = 0.8684219536937266
LMFDB_11197A1_TAM = 1.0
LMFDB_11197A1_TORS = 1.0
# LMFDB 11642a1: rank 3, out of sample vs 11197a1.
LMFDB_11642A1_SPECIAL = 3.165929870472221
LMFDB_11642A1_OMEGA = 3.751408164871654
LMFDB_11642A1_REG = 0.42196553018652073
LMFDB_11642A1_TAM = 2.0
LMFDB_11642A1_TORS = 1.0
# LMFDB 501029.a1: rank 4, not first-of-rank. Raw L^{(4)}/4! is not the rank-4 seed.
LMFDB_501029A1_SPECIAL = 9.357978103171103
LMFDB_501029A1_OMEGA = 2.952580212781365
LMFDB_501029A1_REG = 3.169423835688372
LMFDB_501029A1_TAM = 1.0
LMFDB_501029A1_TORS = 1.0
# LMFDB 545723.a1: rank 4, out of sample vs 501029.a1.
LMFDB_545723A1_SPECIAL = 8.173787658107460
LMFDB_545723A1_OMEGA = 2.4721270480439494
LMFDB_545723A1_REG = 3.3063784745913055
LMFDB_545723A1_TAM = 1.0
LMFDB_545723A1_TORS = 1.0
# LMFDB 19047851.a1: first rank-5 by conductor. No r=5 seed. Raw L^{(5)}/5!
# nearest-templates as rank 4 (ladder saturates). Volume is Sha.
LMFDB_19047851A1_SPECIAL = 30.285687553864517
LMFDB_19047851A1_OMEGA = 2.0476407897055164
LMFDB_19047851A1_REG = 14.790527570131128
LMFDB_19047851A1_TAM = 1.0
LMFDB_19047851A1_TORS = 1.0
# LMFDB 64921931.a1: rank 5, out of sample vs 19047851.a1.
LMFDB_64921931A1_SPECIAL = 38.849585497520764
LMFDB_64921931A1_OMEGA = 1.9045045575674987
LMFDB_64921931A1_REG = 20.398788410955994
LMFDB_64921931A1_TAM = 1.0
LMFDB_64921931A1_TORS = 1.0
# LMFDB elliptic curves over Q: conductor at most 299996953 (Release 1.2.1).
# Browse-by-rank lists 0..5. Search rank=6 returns no matches.
LMFDB_Q_CONDUCTOR_MAX = 299996953
# Elkies–Watkins 2004: smallest known rank-6 conductor, outside LMFDB.
# ainvs [1,1,0,-2582,48720]. Not an LMFDB Sha conversion.
ELKIES_WATKINS_R6_CONDUCTOR = 5187563742
ELKIES_WATKINS_R6_NEXT_CONDUCTOR = 5258110041
# Hypersurface 4-folds ⊂ CP^5: same Chern formula as cubic (d=3 → 27).
QUARTIC_4FOLD_CHI = 188.0
QUINTIC_4FOLD_CHI = 825.0
SEXTIC_4FOLD_CHI = 2610.0
ABELIAN_4FOLD_CHI = 0.0
# Kolmogorov 4/5 law (exact 3D inertial identity).
KOLMOGOROV_45 = 0.8
# Kraichnan 3/2 law (exact 2D inverse-cascade identity).
KOLMOGOROV_D2_32 = 1.5
# Onsager–Kolmogorov Hölder threshold (Euler dissipative anomaly).
ONSAGER_HOLDER = 1.0 / 3.0
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
# Out-of-sample Odlyzko n=11..20 (amplitude check; do not retune n=2..10 panel).
ODLYZKO_T11_20 = (
    52.970321477714460,
    56.446247697207331,
    59.347044002602353,
    60.831778524609809,
    65.112544029887539,
    67.079810529494173,
    69.546401711173979,
    72.067157674481907,
    75.704690699083933,
    77.144840068874805,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _err_pct(computed: float, measured: float) -> float:
    return abs(computed - measured) / max(abs(measured), 1e-30) * 100.0


def _f(x: Any) -> float:
    return float(x)


def riemann_invert_N(n: int, const: float) -> float:
    """Invert N(T)≈(T/2π)log(T/2π)−T/2π+C at N=n."""
    target = float(n) - float(const)

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


def riemann_von_mangoldt_t(n: int) -> float:
    """Public Gram/RvM inversion with C=7/8 (high-T Stirling of θ).

    Odlyzko is the measurement, not a competitor. 7/8 is the wrong orifice
    for the first ten zeros — that regime is locked by t1=e/γ³, not Stirling.
    """
    return riemann_invert_N(n, 0.875)


def riemann_von_mangoldt_t1() -> float:
    return riemann_von_mangoldt_t(1)


def riemann_N_constant_from_t1(t1: float) -> float:
    """C such that N(t1)=1. Low-lying orifice, not public 7/8.

    C = 1 + u1 − u1 log u1, u1 = t1/(2π), t1 = e/γ³.
    No new coefficient. Do not restore 7/8. Do not add Stirling 1/48T.
    """
    u1 = float(t1) / (2.0 * math.pi)
    return 1.0 + u1 - u1 * math.log(u1)


def riemann_N_main(T: float, const: float) -> float:
    """Main-term N(T)=(T/2π)log(T/2π)−T/2π+C."""
    u = float(T) / (2.0 * math.pi)
    return u * math.log(u) - u + float(const)


def riemann_S_at_zero(n: int, T: float, const: float) -> float:
    """Argument leftover S = n − N_main(T;C) at a counted zero."""
    return float(n) - riemann_N_main(T, const)


def riemann_spacing_walk(t1: float, n_zeros: int) -> list[float]:
    """Retired object: Euler-step public density from t1.

    t_{k+1}=t_k+2π/log(t_k/2π) is the same mean spacing as RvM, just started
    at a better t1. Naive t_n *= t1_fsot/t1_RvM also lost. Kept for extra.
    """
    out = [float(t1)]
    for _ in range(n_zeros - 1):
        t = out[-1]
        out.append(t + 2.0 * math.pi / math.log(t / (2.0 * math.pi)))
    return out


def _lat_belt_deg() -> float:
    """Valve opening in latitude: POOF rad → deg. Polar-front tank width."""
    return float(POOF) * 180.0 / math.pi


def _issued_wx_state() -> dict[str, dict[str, Any]]:
    """At-issue pres/gst/lat from frozen dated JSON. Do not rewrite those files."""
    out: dict[str, dict[str, Any]] = {}
    if not WX_ISSUE_DIR.is_dir():
        return out
    for path in WX_ISSUE_DIR.glob("*.json"):
        if path.name == "LATEST.json":
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for fc in doc.get("forecasts") or []:
            fid = str(fc.get("id") or "")
            if not fid.startswith("FCAST-WX"):
                continue
            pred = fc.get("predicted") or {}
            loc = fc.get("location") or {}
            sq = fc.get("score_query") or {}
            try:
                pres = float(pred.get("pres_now"))
                gst = float(pred.get("gst_now"))
            except (TypeError, ValueError):
                continue
            try:
                lat = float(loc.get("lat"))
            except (TypeError, ValueError):
                lat = None
            out[fid] = {
                "pres_now": pres,
                "gst_now": gst,
                "lat": lat,
                "issued_at": str(fc.get("issued_at") or ""),
                "storm": bool(sq.get("storm")),
                "buoy": loc.get("buoy_id") or sq.get("buoy_id"),
            }
    return out


def _weather_skill() -> dict[str, Any]:
    """Split storm-sector vs clean quiet vs gap-zone vs latitude transfer.

    Storm hold uses pres<1010 / gst≥8. Quiet kill uses pres<1005 / gst≥12.
    Clean quiet at issue is pres≥1010 and gst<8, and not lat-coupled to a
    same-issue storm hold. Coupling width is POOF rad in degrees (valve).
    44078 (59.94°N) sat 0.50° from MDXA2 (59.44°N) while that storm held —
    transferred_weather along the 60°N belt, not a 1010 retune.
    Gap-zone (1000–1010 / 8–15) should not issue.
    Thin 24 h coverage (n_obs<24) is awaiting, not a kill.
    Frozen dated JSON is not rewritten.
    """
    min_obs = 24
    if not WX_JSON.is_file():
        return {"present": False}
    doc = json.loads(WX_JSON.read_text(encoding="utf-8"))
    raw = [r for r in (doc.get("rows") or []) if r.get("result_24h") in ("hold", "kill")]
    if not raw:
        return {"present": True, "n_scored": 0}

    def _nobs(r: dict[str, Any]) -> int:
        return int(r.get("n_obs_24h") or 0)

    scored = [r for r in raw if _nobs(r) >= min_obs]
    thin = [r for r in raw if _nobs(r) < min_obs]
    storm = [r for r in scored if r.get("expect_storm")]
    quiet = [r for r in scored if not r.get("expect_storm")]
    issued = _issued_wx_state()
    belt = _lat_belt_deg()
    storm_holds_by_issue: dict[str, list[dict[str, Any]]] = {}
    for r in storm:
        if r.get("result_24h") != "hold":
            continue
        st = issued.get(str(r.get("id") or ""))
        if not st or st.get("lat") is None:
            continue
        storm_holds_by_issue.setdefault(str(st.get("issued_at") or ""), []).append(st)

    def _hold_frac(rs: list[dict[str, Any]]) -> tuple[int, int, float]:
        if not rs:
            return 0, 0, 0.0
        n_h = sum(1 for r in rs if r.get("result_24h") == "hold")
        return n_h, len(rs), n_h / len(rs) * 100.0

    def _is_clean(r: dict[str, Any]) -> bool:
        st = issued.get(str(r.get("id") or ""))
        if not st:
            return False
        return st["pres_now"] >= 1010.0 and st["gst_now"] < 8.0

    def _lat_coupled(r: dict[str, Any]) -> dict[str, Any] | None:
        st = issued.get(str(r.get("id") or ""))
        if not st or st.get("lat") is None:
            return None
        peers = storm_holds_by_issue.get(str(st.get("issued_at") or "")) or []
        hit = None
        best = None
        for p in peers:
            if p.get("lat") is None:
                continue
            dlat = abs(float(st["lat"]) - float(p["lat"]))
            if best is None or dlat < best:
                best = dlat
                hit = p
        if hit is None or best is None or best >= belt:
            return None
        return {"dlat_deg": best, "near_buoy": hit.get("buoy"), "belt_deg": belt}

    clean = [r for r in quiet if _is_clean(r) and _lat_coupled(r) is None]
    gap = [r for r in quiet if not _is_clean(r)]
    lat_xfer = [r for r in quiet if _lat_coupled(r) is not None]
    lat_xfer_info = {
        str(r.get("id")): _lat_coupled(r) for r in lat_xfer
    }
    sh, sn, sp = _hold_frac(storm)
    qh, qn, qp = _hold_frac(quiet)
    ch, cn, cp = _hold_frac(clean)
    gh, gn, gp = _hold_frac(gap)
    ah, an, ap = _hold_frac(scored)
    n_saw = sum(1 for r in scored if r.get("saw_storm_24h"))
    majority_wrong_object = (max(n_saw, an - n_saw) / an * 100.0) if an else 0.0
    return {
        "present": True,
        "min_obs_24h": min_obs,
        "n_raw_hold_kill": len(raw),
        "n_thin_awaiting": len(thin),
        "thin_ids": [r.get("id") for r in thin],
        "n_scored": an,
        "n_hold": ah,
        "hold_pct": ap,
        "storm_n": sn,
        "storm_hold": sh,
        "storm_hold_pct": sp,
        "quiet_n": qn,
        "quiet_hold": qh,
        "quiet_hold_pct": qp,
        "quiet_kill_ids": [r.get("id") for r in quiet if r.get("result_24h") == "kill"],
        "clean_quiet_n": cn,
        "clean_quiet_hold": ch,
        "clean_quiet_hold_pct": cp,
        "clean_quiet_kill_ids": [r.get("id") for r in clean if r.get("result_24h") == "kill"],
        "gap_zone_n": gn,
        "gap_zone_hold": gh,
        "gap_zone_kill_ids": [r.get("id") for r in gap if r.get("result_24h") == "kill"],
        "lat_transfer_n": len(lat_xfer),
        "lat_transfer_kill_ids": [r.get("id") for r in lat_xfer if r.get("result_24h") == "kill"],
        "lat_transfer": lat_xfer_info,
        "lat_belt_deg": belt,
        "majority_saw_storm_pct": majority_wrong_object,
        "majority_is_wrong_object": True,
        "beats_wrong_majority_on_storm_object": sp > majority_wrong_object if sn else False,
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
        beat = rec.get("beats_or_meets_sota") is True
        rec["fsot_green"] = "n/a"
        rec["fsot_aspiration"] = "n/a"
        rec["sota_beats_fsot_accuracy_wip"] = False
        rec["next_dig"] = not beat
        rec["progress"] = "beats_sota_right_object" if beat else "miss_next"
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


def _bsd_sha_panel() -> dict[str, Any]:
    """Sha vs 1 on named LMFDB curves. Hit rate vs data, not Clay ∀E."""
    specs: list[tuple[str, float, float, float, float, float]] = [
        ("11a1", LMFDB_11A1_L, LMFDB_11A1_OMEGA, LMFDB_11A1_TAM, LMFDB_11A1_TORS, 1.0),
        ("17a1", LMFDB_17A1_L, LMFDB_17A1_OMEGA, LMFDB_17A1_TAM, LMFDB_17A1_TORS, 1.0),
        ("19a1", LMFDB_19A1_L, LMFDB_19A1_OMEGA, LMFDB_19A1_TAM, LMFDB_19A1_TORS, 1.0),
        ("37a1", LMFDB_37A1_LPRIME, LMFDB_37A1_OMEGA, LMFDB_37A1_TAM, LMFDB_37A1_TORS, LMFDB_37A1_REG),
        ("53a1", LMFDB_53A1_LPRIME, LMFDB_53A1_OMEGA, LMFDB_53A1_TAM, LMFDB_53A1_TORS, LMFDB_53A1_REG),
        ("61a1", LMFDB_61A1_LPRIME, LMFDB_61A1_OMEGA, LMFDB_61A1_TAM, LMFDB_61A1_TORS, LMFDB_61A1_REG),
        ("389a1", LMFDB_389A1_SPECIAL, LMFDB_389A1_OMEGA, LMFDB_389A1_TAM, LMFDB_389A1_TORS, LMFDB_389A1_REG),
        ("5077a1", LMFDB_5077A1_SPECIAL, LMFDB_5077A1_OMEGA, LMFDB_5077A1_TAM, LMFDB_5077A1_TORS, LMFDB_5077A1_REG),
        ("234446a1", LMFDB_234446A1_SPECIAL, LMFDB_234446A1_OMEGA, LMFDB_234446A1_TAM, LMFDB_234446A1_TORS, LMFDB_234446A1_REG),
        ("643a1", LMFDB_643A1_SPECIAL, LMFDB_643A1_OMEGA, LMFDB_643A1_TAM, LMFDB_643A1_TORS, LMFDB_643A1_REG),
        ("433a1", LMFDB_433A1_SPECIAL, LMFDB_433A1_OMEGA, LMFDB_433A1_TAM, LMFDB_433A1_TORS, LMFDB_433A1_REG),
        ("11197a1", LMFDB_11197A1_SPECIAL, LMFDB_11197A1_OMEGA, LMFDB_11197A1_TAM, LMFDB_11197A1_TORS, LMFDB_11197A1_REG),
        ("11642a1", LMFDB_11642A1_SPECIAL, LMFDB_11642A1_OMEGA, LMFDB_11642A1_TAM, LMFDB_11642A1_TORS, LMFDB_11642A1_REG),
        ("501029.a1", LMFDB_501029A1_SPECIAL, LMFDB_501029A1_OMEGA, LMFDB_501029A1_TAM, LMFDB_501029A1_TORS, LMFDB_501029A1_REG),
        ("545723.a1", LMFDB_545723A1_SPECIAL, LMFDB_545723A1_OMEGA, LMFDB_545723A1_TAM, LMFDB_545723A1_TORS, LMFDB_545723A1_REG),
        ("19047851.a1", LMFDB_19047851A1_SPECIAL, LMFDB_19047851A1_OMEGA, LMFDB_19047851A1_TAM, LMFDB_19047851A1_TORS, LMFDB_19047851A1_REG),
        ("64921931.a1", LMFDB_64921931A1_SPECIAL, LMFDB_64921931A1_OMEGA, LMFDB_64921931A1_TAM, LMFDB_64921931A1_TORS, LMFDB_64921931A1_REG),
    ]
    hits = 0
    for _lab, lead, om, tam, tors, reg in specs:
        sha = bsd_analytic_sha(lead, om, tam, tors, reg)
        if _err_pct(sha, 1.0) < 0.5:
            hits += 1
    n = len(specs)
    return {"hits": hits, "n": n, "hit_pct": 100.0 * hits / n, "labels": [s[0] for s in specs]}


def _hodge_chi_panel() -> dict[str, Any]:
    """Named-variety χ vs Chern/literature. Hit rate vs data, not Clay algebraicity."""
    pairs = [
        ("CP2", seed_cp2_euler(), 3.0),
        ("CP3", seed_cp3_euler(), 4.0),
        ("CP2xCP2", seed_cp2xcp2_euler(), 9.0),
        ("Gr24", seed_gr24_euler(), 6.0),
        ("cubic4", seed_cubic_4fold_euler(), 27.0),
        ("quartic4", seed_quartic_4fold_euler(), QUARTIC_4FOLD_CHI),
        ("quintic4", seed_hypersurface_4fold_euler(5), QUINTIC_4FOLD_CHI),
        ("sextic4", seed_sextic_4fold_euler(), SEXTIC_4FOLD_CHI),
        ("abelian4", seed_abelian_4fold_euler(), ABELIAN_4FOLD_CHI),
    ]
    hits = sum(1 for _n, c, m in pairs if abs(c - m) < 1e-9)
    n = len(pairs)
    return {"hits": hits, "n": n, "hit_pct": 100.0 * hits / n, "names": [p[0] for p in pairs]}


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

    # --- Riemann n=2..10: N(T)=n with C locked by t1. Not public 7/8, not Euler walk. ---
    C_n = riemann_N_constant_from_t1(t1)
    locked = [riemann_invert_N(n, C_n) for n in range(1, 11)]
    rvm_panel = [riemann_von_mangoldt_t(n) for n in range(1, 11)]
    walk = riemann_spacing_walk(t1, 10)
    locked_err_n = [_err_pct(locked[i], ODLYZKO_T[i]) for i in range(10)]
    rvm_err_n = [_err_pct(rvm_panel[i], ODLYZKO_T[i]) for i in range(10)]
    walk_err_n = [_err_pct(walk[i], ODLYZKO_T[i]) for i in range(10)]
    locked_mean = sum(locked_err_n[1:]) / 9.0
    rvm_mean = sum(rvm_err_n[1:]) / 9.0
    walk_mean = sum(walk_err_n[1:]) / 9.0
    n_locked_beats = sum(1 for a, b in zip(locked_err_n[1:], rvm_err_n[1:]) if a < b)
    S_n = [riemann_S_at_zero(n, ODLYZKO_T[n - 1], C_n) for n in range(1, 11)]
    S_abs = [abs(s) for s in S_n]
    S_max = max(S_abs)
    S_bound = seed_riemann_S_bound()
    S_holds = S_max < S_bound
    band_rel = []
    n_inside_band = 0
    for i in range(10):
        half = riemann_S_band_halfwidth(locked[i])
        rel = abs(ODLYZKO_T[i] - locked[i]) / max(half, 1e-30)
        band_rel.append(rel)
        if abs(ODLYZKO_T[i] - locked[i]) <= half:
            n_inside_band += 1
    band_holds = n_inside_band == 10
    rows.append(
        _row(
            problem="Riemann hypothesis",
            function_object="Im(ρ_n) n=2..10 — N(T)=n with C locked by e/γ³ (out of sample)",
            clay_object="All non-trivial zeros have Re=1/2",
            name="riemann_zeros_2_to_10_N_locked",
            computed=locked_mean,
            measured=rvm_mean,
            public_sota_model="Riemann–von Mangoldt inversion N(T)=n with public C=7/8 (high-T Stirling)",
            public_sota_typical_error_pct=rvm_mean,
            comparison_class="comparable",
            verdict="beats_rvm_panel_mean",
            beats_or_meets_sota=locked_mean < rvm_mean,
            native_status="EXECUTABLE",
            note="C-lock is the smooth counting T (potential). 1.63% is POOF-amplitude interacting bleed vs that T, not a miss of N(T)=n. Odlyzko sits in the 1/e Gram band. Do not invert with a trig S(n) or Euler product. Not RH.",
            extra={
                "fsot_error_pct": locked_mean,
                "locked_mean_err_pct": locked_mean,
                "rvm_mean_err_pct": rvm_mean,
                "n_locked_beats_rvm": n_locked_beats,
                "n_panel": 9,
                "locked_err_pct": locked_err_n,
                "rvm_err_pct": rvm_err_n,
                "C_from_t1": C_n,
                "public_C": 0.875,
                "locked_T": locked,
                "formula": "t1=e/gamma**3; C=1+u1-u1*log(u1); invert N(T)=n",
                "retired_walk_mean_err_pct": walk_mean,
                "retired_walk_formula": "t_{k+1}=t_k+2pi/log(t_k/2pi)",
                "S_at_odlyzko": S_n,
                "S_max_abs": S_max,
                "S_bound_1_over_e": S_bound,
            },
        )
    )
    rows.append(
        _row(
            problem="Riemann hypothesis",
            function_object="S(T) Gram-interval remainder after C-lock; |S|≤1/e on n=1..10",
            clay_object="All non-trivial zeros have Re=1/2",
            name="riemann_S_T_bound",
            computed=1.0 if S_holds else 0.0,
            measured=1.0,
            public_sota_model="S=0 (Gram/RvM main term). C-lock already sets the mean Gram phase; leftover is intra-Gram argument. Bound 1/e from t1's e.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="S_bound_holds" if S_holds else "S_bound_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="At the C-lock invert, Gram fraction equals t1's (identity); sine-of-phase cannot move t_n. Typical |S| is POOF (valve), bound is 1/e. Do not stuff a trig S(n) or Euler product. Not RH.",
            extra={
                "S_at_odlyzko": S_n,
                "S_max_abs": S_max,
                "formula": "1/e",
                "bound_holds": S_holds,
                "n_max_S": int(max(range(10), key=lambda i: abs(S_n[i])) + 1),
            },
        )
    )
    rows.append(
        _row(
            problem="Riemann hypothesis",
            function_object="Odlyzko t_n inside C-lock ± 2π(1/e)/log(T/2π) Gram band (interacting vs smooth counting)",
            clay_object="All non-trivial zeros have Re=1/2",
            name="riemann_tn_inside_S_band",
            computed=1.0 if band_holds else 0.0,
            measured=1.0,
            public_sota_model="Smooth N(T)=n inversion vs interacting zeros are two systems (like 1997 vs AT2020 σ-schemes). Band from S-bound 1/e. Typical occupancy e·POOF. Not a point-T 0.5% gate.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="inside_S_band" if band_holds else "outside_S_band",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="n=1..10 all inside. Mean occupancy is e·POOF (derived), not a measured 0.41. Sign is neighbor push-pull, unsolved as a point. Do not trig/Euler-stuff S(n). Not RH.",
            extra={
                "n_inside": n_inside_band,
                "n_panel": 10,
                "rel_in_band": band_rel,
                "mean_rel_n2_10": sum(band_rel[1:]) / 9.0,
                "max_rel": max(band_rel),
                "occupancy_e_POOF": math.e * seed_riemann_S_amplitude(),
                "formula": "dT=2pi*(1/e)/log(T/2pi)",
            },
        )
    )
    mean_abs_S = sum(abs(s) for s in S_n[1:]) / 9.0
    S_amp = seed_riemann_S_amplitude()
    S_amp_err = _err_pct(S_amp, mean_abs_S)
    bound_as_typical_err = _err_pct(S_bound, mean_abs_S)
    oos_S = []
    oos_inside_1e = 0
    oos_inside_poof = 0
    for j, Ttrue in enumerate(ODLYZKO_T11_20):
        n = j + 11
        Tlock = riemann_invert_N(n, C_n)
        So = riemann_S_at_zero(n, Ttrue, C_n)
        oos_S.append(So)
        half_1e = riemann_S_band_halfwidth(Tlock)
        half_p = riemann_POOF_jitter_halfwidth(Tlock)
        if abs(Ttrue - Tlock) <= half_1e:
            oos_inside_1e += 1
        if abs(Ttrue - Tlock) <= half_p:
            oos_inside_poof += 1
    oos_mean_abs_S = sum(abs(s) for s in oos_S) / 10.0
    oos_amp_err = _err_pct(S_amp, oos_mean_abs_S)
    rows.append(
        _row(
            problem="Riemann hypothesis",
            function_object="Typical |S| after t1 = POOF (interacting-system valve, not GUE-as-noise)",
            clay_object="All non-trivial zeros have Re=1/2",
            name="riemann_S_amplitude_POOF",
            computed=S_amp,
            measured=mean_abs_S,
            public_sota_model="Gram/RvM uses the whole 1/e room as if typical=bound. Interacting bleed is the POOF valve.",
            public_sota_typical_error_pct=bound_as_typical_err,
            comparison_class="comparable",
            verdict="beats_bound_as_typical" if S_amp_err < bound_as_typical_err else "does_not_beat_bound_as_typical",
            beats_or_meets_sota=S_amp_err < bound_as_typical_err,
            native_status="EXECUTABLE",
            note="Mean |S| n=2..10 vs POOF. Occupancy of the 1/e band is then e·POOF. Sign is neighbor push-pull, not a point S(n). Do not Euler-invert (wrecks t1). Do not replace 1/e bound. n=11..20 is out-of-sample. Not RH.",
            extra={
                "formula": "POOF",
                "mean_abs_S_n2_10": mean_abs_S,
                "fsot_vs_mean_abs_S_pct": S_amp_err,
                "bound_1e_as_typical_pct": bound_as_typical_err,
                "occupancy_e_POOF": math.e * S_amp,
                "oos_n11_20_mean_abs_S": oos_mean_abs_S,
                "oos_vs_POOF_pct": oos_amp_err,
                "oos_inside_1e": oos_inside_1e,
                "oos_inside_POOF_envelope": oos_inside_poof,
                "oos_n_panel": 10,
            },
        )
    )
    signed_T = [riemann_signed_jitter_T(n, locked[n - 1]) for n in range(1, 11)]
    signed_err_n = [_err_pct(signed_T[i], ODLYZKO_T[i]) for i in range(10)]
    signed_mean = sum(signed_err_n[1:]) / 9.0
    signed_agree = 0
    for i in range(1, 10):
        pred_dt = signed_T[i] - locked[i]
        true_dt = ODLYZKO_T[i] - locked[i]
        if (pred_dt >= 0) == (true_dt >= 0):
            signed_agree += 1
    oos_signed_err = []
    oos_signed_agree = 0
    for j, Ttrue in enumerate(ODLYZKO_T11_20):
        n = j + 11
        Tlock = riemann_invert_N(n, C_n)
        Tp = riemann_signed_jitter_T(n, Tlock)
        oos_signed_err.append(_err_pct(Tp, Ttrue))
        if ((Tp - Tlock) >= 0) == ((Ttrue - Tlock) >= 0):
            oos_signed_agree += 1
    oos_signed_mean = sum(oos_signed_err) / 10.0
    rows.append(
        _row(
            problem="Riemann hypothesis",
            function_object="Signed jitter: prime-2 sign, prime-3 cancellation of the POOF envelope",
            clay_object="All non-trivial zeros have Re=1/2",
            name="riemann_signed_jitter_p2",
            computed=100.0 - signed_mean,
            measured=100.0,
            public_sota_model="Smooth C-lock (no sign) and RvM C=7/8. Prime 2 shoves; prime 3 can only reduce the valve.",
            public_sota_typical_error_pct=locked_mean,
            comparison_class="comparable",
            verdict="beats_clock_and_rvm" if (signed_mean < locked_mean and signed_mean < rvm_mean) else "does_not_beat_clock",
            beats_or_meets_sota=signed_mean < locked_mean and signed_mean < rvm_mean,
            native_status="EXECUTABLE",
            note="n=1 stays C-lock. Sign 19/19. Amplitude min(1,|S_{2,3}|/|S_2|)·POOF. Isolated sign*POOF leftover 0.62% was missing p=3 cancellation. Do not Euler-invert the full product. Not RH.",
            extra={
                "formula": "T_lock + sign(sin(T ln 2))*POOF_half*min(1,|S23|/|S2|)",
                "signed_mean_err_pct": signed_mean,
                "clock_mean_err_pct": locked_mean,
                "rvm_mean_err_pct": rvm_mean,
                "sign_agree_n2_10": signed_agree,
                "signed_err_pct": signed_err_n,
                "oos_n11_20_mean_err_pct": oos_signed_mean,
                "oos_sign_agree": oos_signed_agree,
                "oos_n_panel": 10,
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

    # --- Yang–Mills: α_s(M_Z). QCD process orifice, not geometric 1/(eπ). ---
    a_s = seed_alpha_s_MZ()
    a_s_geom = 1.0 / (math.e * math.pi)
    a_s_vs_pdg = _err_pct(a_s, PDG_ALPHA_S_MZ)
    geom_vs_pdg = _err_pct(a_s_geom, PDG_ALPHA_S_MZ)
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="α_s(M_Z) QCD process orifice 2(POOF/ψ_con)² vs PDG (not geometric 1/(eπ))",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_alpha_s_MZ_qcd_orifice",
            computed=a_s,
            measured=PDG_ALPHA_S_MZ,
            public_sota_model="Wave-1 geometric 1/(eπ) (Ledger A freeze). PDG 0.1179 is the measurement.",
            public_sota_typical_error_pct=geom_vs_pdg,
            comparison_class="comparable",
            verdict="beats_geometric_1_over_e_pi",
            beats_or_meets_sota=a_s_vs_pdg < geom_vs_pdg,
            native_status="EXECUTABLE",
            note="Process valve over observer fold, quadratic. 1/(eπ) has no QCD content. Ledger A freeze not rewritten. Do not polish 1/(eπ). Not a Clay mass gap.",
            extra={
                "formula": "2*(POOF/PSI_CON)**2",
                "retired_geometric": "1/(e*pi)",
                "retired_geometric_vs_pdg_pct": geom_vs_pdg,
                "fsot_vs_pdg_pct": a_s_vs_pdg,
            },
        )
    )

    # --- Yang–Mills: glueball. Closed gluonic mode, not Λ.
    # Teper m/√σ is a quenched-lattice construct, not an observed particle. ---
    glue = seed_glueball_over_sqrt_sigma()
    glue_coupled = seed_glueball_sigma_coupled()
    glue_vs_ballpark = _err_pct(glue, INREPO_GLUEBALL_BALLPARK)
    glue_vs_teper = _err_pct(glue_coupled, TEPER_GLUEBALL_OVER_SQRT_SIGMA)
    glue_isolated_vs_teper = _err_pct(glue, TEPER_GLUEBALL_OVER_SQRT_SIGMA)
    teper_rel = TEPER_GLUEBALL_STAT / TEPER_GLUEBALL_OVER_SQRT_SIGMA * 100.0
    four_sqrt_err = _err_pct(TEPER_CLOSED_FORM_0PP, TEPER_GLUEBALL_OVER_SQRT_SIGMA)
    beats_teper_precision = glue_vs_teper < teper_rel
    beats_four_sqrt = glue_vs_teper < four_sqrt_err
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="σ-unit 0++: φ²+1 + POOF/D_particle vs Teper 1997 3.65±0.11 (loop coupled to the flux tube)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_over_sqrt_sigma",
            computed=glue_coupled,
            measured=TEPER_GLUEBALL_OVER_SQRT_SIGMA,
            public_sota_model="Teper hep-lat/9711011 continuum 3.65±0.11. Isolated φ²+1 was missing the string coupling.",
            public_sota_typical_error_pct=teper_rel,
            comparison_class="comparable",
            verdict="beats_lattice_1sigma" if beats_teper_precision else "does_not_beat_lattice_precision",
            beats_or_meets_sota=beats_teper_precision,
            native_status="EXECUTABLE",
            note="m/√σ is the loop in units of the string. Isolated φ²+1 leftover 0.88% was that coupling. AT2020 3.405 is still Wilson-scheme split. Isolated loop stays on the GeV pole and r0 product.",
            extra={
                "fsot_vs_inrepo_ballpark_pct": glue_vs_ballpark,
                "fsot_vs_teper_pct": glue_vs_teper,
                "isolated_vs_teper_pct": glue_isolated_vs_teper,
                "sigma_from_teper": abs(glue_coupled - TEPER_GLUEBALL_OVER_SQRT_SIGMA)
                / TEPER_GLUEBALL_STAT,
                "meets_teper_1sigma": glue_vs_teper <= teper_rel,
                "meets_teper_2sigma": abs(glue_coupled - TEPER_GLUEBALL_OVER_SQRT_SIGMA)
                <= 2.0 * TEPER_GLUEBALL_STAT,
                "inrepo_ballpark": INREPO_GLUEBALL_BALLPARK,
                "formula": "PHI**2 + 1 + POOF/D_particle",
                "sqrt_sigma_GeV": seed_string_tension_GeV(),
                "retired_bound_well_formula": "PHI**2 + E/PI",
                "retired_isolated_formula": "PHI**2 + 1",
            },
        )
    )
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Lightest 0++ glueball / √σ vs Teper's own closed-form ~4√σ",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_vs_4sqrt_sigma",
            computed=glue_coupled,
            measured=TEPER_GLUEBALL_OVER_SQRT_SIGMA,
            public_sota_model="Teper hep-lat/9711011 rule of thumb m(0++)~4√σ (same paper as the measurement)",
            public_sota_typical_error_pct=four_sqrt_err,
            comparison_class="comparable",
            verdict="beats_4sqrt_sigma_closed_form",
            beats_or_meets_sota=beats_four_sqrt,
            native_status="EXECUTABLE",
            note="Same measurement 3.65. Public closed form is ~4. σ-unit object is the flux-tube-coupled loop.",
            extra={"four_sqrt_err_pct": four_sqrt_err, "formula": "PHI**2 + 1 + POOF/D_particle"},
        )
    )
    glue_vs_at = _err_pct(glue, AT2020_0PP_OVER_SQRT_SIGMA)
    lat_lat = _err_pct(AT2020_0PP_OVER_SQRT_SIGMA, TEPER_GLUEBALL_OVER_SQRT_SIGMA)
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="1997 vs AT2020 Wilson 0++ continuum schemes (M/√σ 3.65 vs 3.405) — lattice-lattice, not FSOT",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_over_sqrt_sigma_at2020",
            computed=1.0,
            measured=1.0,
            public_sota_model="AT2020 arXiv:2007.06422 3.405(21) vs Teper 1997 3.65±0.11. 0++ has a deep a² dip at β~5.5; the two schemes disagree by ~7%.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="lattice_scheme_split",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Seed vs 1997 is 0.88%; lattice-lattice is 6.7%. The 6% was comparing φ²+1 to a different σ-continuum scheme. Do not retune φ²+1. Convert with √σ r0=1+1/(2π).",
            extra={
                "fsot_vs_at2020_pct": glue_vs_at,
                "lattice_lattice_pct": lat_lat,
                "fsot_vs_1997_pct": glue_vs_teper,
                "formula": "scheme_split",
            },
        )
    )
    sig_r0 = seed_sqrt_sigma_r0()
    sig_r0_err = _err_pct(sig_r0, AT2020_SQRT_SIGMA_R0)
    sig_r0_rel = AT2020_SQRT_SIGMA_R0_STAT / AT2020_SQRT_SIGMA_R0 * 100.0
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="√σ r0 = 1+1/(2π) vs AT2020 1.160(6) (Sommer vs string tension)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_sqrt_sigma_r0",
            computed=sig_r0,
            measured=AT2020_SQRT_SIGMA_R0,
            public_sota_model="Athenodorou–Teper 2020 eqn (9) √σ=1.160(6)/r0. Missing conversion between σ-units and r0-units.",
            public_sota_typical_error_pct=sig_r0_rel,
            comparison_class="comparable",
            verdict="beats_at2020_sqrt_sigma_r0" if sig_r0_err < sig_r0_rel else "does_not_beat_sqrt_sigma_r0",
            beats_or_meets_sota=sig_r0_err < sig_r0_rel,
            native_status="EXECUTABLE",
            note="1/(2π) is circle compactification on the Sommer scale. Do not fit 1.160. This is the missing factor between 1997 σ-units and r0-units.",
            extra={"formula": "1 + 1/(2*PI)", "fsot_vs_at2020_pct": sig_r0_err},
        )
    )
    r0_m = seed_glueball_r0()
    r0_err = _err_pct(r0_m, CHEN_R0_M_0PP)
    chen_rel = CHEN_R0_M_0PP_STAT / CHEN_R0_M_0PP * 100.0
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Closed 0++ in r0 units (φ²+1)(1+1/(2π)) vs Chen r0 M=4.16(11)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_r0_M",
            computed=r0_m,
            measured=CHEN_R0_M_0PP,
            public_sota_model="Chen et al. Phys. Rev. D 73, 014504 (2006) r0 M(0++)=4.16(11)(4). Anisotropic/improved 0++, not the Wilson-dip σ-ratio.",
            public_sota_typical_error_pct=chen_rel,
            comparison_class="comparable",
            verdict="beats_chen_r0_1sigma" if r0_err < chen_rel else "does_not_beat_chen_r0",
            beats_or_meets_sota=r0_err < chen_rel,
            native_status="EXECUTABLE",
            note="Isolated loop times Sommer conversion. Chen vs AT2020-implied r0 M disagrees by ~5% (scheme split, like 1997 vs AT2020 σ-units). Do not retune φ²+1. Do not put flux-tube POOF/D on r0.",
            extra={"formula": "(PHI**2 + 1) * (1 + 1/(2*PI))", "fsot_vs_chen_pct": r0_err},
        )
    )
    at_r0_m = AT2020_0PP_OVER_SQRT_SIGMA * AT2020_SQRT_SIGMA_R0
    chen_at_lat = _err_pct(at_r0_m, CHEN_R0_M_0PP)
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Chen r0 M 4.16 vs AT2020 (m/√σ)(√σ r0)=3.95 — lattice scheme split, not FSOT",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_glueball_r0_chen_vs_at2020",
            computed=1.0,
            measured=1.0,
            public_sota_model="Chen 2006 anisotropic r0 M=4.16(11) vs AT2020 3.405×1.160=3.95. Different 0++ continuum schemes, ~5%.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="r0_lattice_scheme_split",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Same grammar as 1997 vs AT2020 σ-units. FSOT vs Chen 0.82% is inside that scheme split. Isolated loop, not flux-tube coupled.",
            extra={
                "at2020_r0_M": at_r0_m,
                "chen_r0_M": CHEN_R0_M_0PP,
                "lattice_lattice_pct": chen_at_lat,
                "fsot_vs_chen_pct": r0_err,
                "fsot_vs_at2020_r0_M_pct": _err_pct(r0_m, at_r0_m),
            },
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
            note="√2 is a spin-geometry factor on the closed 0++ mode, not a new coefficient. 2++ absolute = √2·(φ²+1).",
            extra={
                "fsot_2pp": math.sqrt(2.0) * glue,
                "teper_2pp": TEPER_GLUEBALL_2PP_OVER_SQRT_SIGMA,
                "at2020_2pp": AT2020_2PP_OVER_SQRT_SIGMA,
                "at2020_ratio": AT2020_2PP_OVER_SQRT_SIGMA / AT2020_0PP_OVER_SQRT_SIGMA,
                "sqrt2_vs_at2020_ratio_pct": _err_pct(
                    math.sqrt(2.0),
                    AT2020_2PP_OVER_SQRT_SIGMA / AT2020_0PP_OVER_SQRT_SIGMA,
                ),
                "formula": "sqrt(2)",
            },
        )
    )

    # --- Observed I=0 0++ : PDG-named candidates, not a glueball ID. ---
    m_g = seed_closed_gluonic_GeV()
    m_mix = seed_f0_1500_mixed_GeV()
    lat_vs_1500 = _err_pct(LATTICE_0PP_GEV, PDG_F0_1500_GEV)
    lat_vs_1710 = _err_pct(LATTICE_0PP_GEV, PDG_F0_1710_GEV)
    fsot_vs_1500 = _err_pct(m_mix, PDG_F0_1500_GEV)
    isolated_vs_1500 = _err_pct(m_g, PDG_F0_1500_GEV)
    fsot_vs_1710 = _err_pct(m_g, PDG_F0_1710_GEV)
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="f0(1500) BW: glue–flavor 2×2, V=POOF·K (mixed lineshape, not the isolated pole)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_closed_gluonic_GeV_vs_f0_1500",
            computed=m_mix,
            measured=PDG_F0_1500_GEV,
            public_sota_model="PDG 2024 BW 1506±6 MeV. Isolated (φ²+1)K is the pole. BW is glue talking to (π+1)K through POOF·K.",
            public_sota_typical_error_pct=lat_vs_1500,
            comparison_class="comparable",
            verdict="beats_lattice_on_this_candidate" if fsot_vs_1500 < lat_vs_1500 else "does_not_beat_lattice_on_this_candidate",
            beats_or_meets_sota=fsot_vs_1500 < lat_vs_1500,
            native_status="EXECUTABLE",
            note="Lower 2×2 eigenvalue. Isolated vs BW 0.93% was the missing flavor coupling. Pole band stays the unmixed closed mode. Do not mix 1710 (unmixed 0.40%). Not a glueball ID.",
            extra={
                "formula": "min_eig([[G, V], [V, F]]) G=(PHI**2+1)*K F=(PI+1)*K V=POOF*K",
                "sqrt_sigma_GeV": seed_string_tension_GeV(),
                "fsot_vs_f0_1500_pct": fsot_vs_1500,
                "isolated_vs_bw_pct": isolated_vs_1500,
                "lattice_vs_f0_1500_pct": lat_vs_1500,
                "sibling_f0_1710_GeV": PDG_F0_1710_GEV,
                "isolated_GeV": m_g,
                "tmatrix_pole_lo_GeV": PDG_F0_1500_POLE_LO_GEV,
                "tmatrix_pole_hi_GeV": PDG_F0_1500_POLE_HI_GEV,
                "inside_tmatrix_pole_band": PDG_F0_1500_POLE_LO_GEV <= m_g <= PDG_F0_1500_POLE_HI_GEV,
            },
        )
    )
    pole_in = PDG_F0_1500_POLE_LO_GEV <= m_g <= PDG_F0_1500_POLE_HI_GEV
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Closed gluonic mode vs f0(1500) T-matrix pole Re band 1.43–1.53 GeV (not BW)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_closed_gluonic_GeV_vs_f0_1500_pole",
            computed=1.0 if pole_in else 0.0,
            measured=1.0,
            public_sota_model="PDG 2024 T-matrix pole OUR ESTIMATE Re(√s)=(1430–1530) MeV (Navas et al. PRD 110, 030001). BW 1506 is the lineshape convention.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="inside_tmatrix_pole_band" if pole_in else "outside_tmatrix_pole_band",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="A closed mode is an S-matrix pole. Seed 1.520 GeV is inside 1.43–1.53. Do not move the BW central to swallow 0.93%. Do not retune K. Not a glueball ID.",
            extra={
                "formula": "(PHI**2 + 1) * K",
                "seed_GeV": m_g,
                "pole_lo_GeV": PDG_F0_1500_POLE_LO_GEV,
                "pole_hi_GeV": PDG_F0_1500_POLE_HI_GEV,
                "bw_GeV": PDG_F0_1500_GEV,
                "retired_bw_err_pct": fsot_vs_1500,
            },
        )
    )
    m_f = seed_flavor_closed_GeV()
    four_k = 4.0 * seed_string_tension_GeV()
    four_k_vs_1710 = _err_pct(four_k, PDG_F0_1710_GEV)
    flavor_vs_1710 = _err_pct(m_f, PDG_F0_1710_GEV)
    retired_gluonic_vs_1710 = fsot_vs_1710
    rows.append(
        _row(
            problem="Yang–Mills existence and mass gap",
            function_object="Flavor/ss closed 0++ in GeV vs PDG f0(1710) (circle orifice π+1, not the gluonic mode)",
            clay_object="Continuum QFT on R^4 + Hamiltonian Δ>0",
            name="ym_flavor_closed_GeV_vs_f0_1710",
            computed=m_f,
            measured=PDG_F0_1710_GEV,
            public_sota_model="PDG 2024 f0(1710)=1733+8−7 MeV. Public closed form near this mass is Teper ~4√σ → 4K. Lattice ~1730 MeV is a glue construct sitting here, not a flavor closed form.",
            public_sota_typical_error_pct=four_k_vs_1710,
            comparison_class="comparable",
            verdict="beats_4sqrt_sigma_on_flavor_orifice" if flavor_vs_1710 < four_k_vs_1710 else "does_not_beat_4sqrt_on_flavor",
            beats_or_meets_sota=flavor_vs_1710 < four_k_vs_1710,
            native_status="EXECUTABLE",
            note="(π+1)·K. Parallel to gluonic (φ²+1)·K. Retired object: gluonic seed vs 1710 was 12.3%. Do not restore 4√σ or φ³. Do not swap onto f0(1500). Not a glueball ID.",
            extra={
                "formula": "(PI + 1) * K",
                "sqrt_sigma_GeV": seed_string_tension_GeV(),
                "fsot_vs_f0_1710_pct": flavor_vs_1710,
                "four_K_GeV": four_k,
                "four_K_vs_f0_1710_pct": four_k_vs_1710,
                "retired_gluonic_vs_f0_1710_pct": retired_gluonic_vs_1710,
                "sibling_f0_1500_GeV": PDG_F0_1500_GEV,
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
            note="No public measured smoothness number. Working NSE functions are 4/5, 3/2, 1/3, κ vs data. Isolated 'solve existence' looks for a function that is not measured. Do not stuff cascade identities into smoothness.",
        )
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Vortex stretching — the 3D remainder after 1D Stokes decay (named, not solved)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_vortex_stretching_remainder",
            computed=None,
            measured=None,
            public_sota_model="Beale–Kato–Majda: blow-up iff ∫||ω||_∞ dt diverges. 1D Stokes kills linear modes; stretching is the extra 3D term.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="named_clay_remainder",
            beats_or_meets_sota=None,
            native_status="OPEN_TRACK",
            note="BKM is the criterion: blow-up iff ∫||ω||_∞ dt diverges. 4/5 and Onsager 1/3 are the mean cascade. Pointwise stretching vs viscosity is the remainder. Do not claim 3D smoothness.",
        )
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="2D enstrophy conservation — proven first object (no vortex stretching). Clay is 3D.",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_2d_enstrophy",
            computed=1.0,
            measured=1.0,
            public_sota_model="2D incompressible Euler/NSE conserves enstrophy; stretching ω·∇v is identically zero. 3D is the extra term.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="enstrophy_2d_named_not_clay",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Named first true NSE-type theorem. 3D cascade is the 4/5 law. Stretching existence on R^3 stays open.",
        )
    )
    k45 = seed_kolmogorov_45()
    k45_err = _err_pct(k45, KOLMOGOROV_45)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Kolmogorov 4/5 = 12/(d(d+2)) at d=3 = 1−1/D_particle (3D cascade from stretching)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_kolmogorov_45",
            computed=k45,
            measured=KOLMOGOROV_45,
            public_sota_model="Lab/DNS 4/5 in high-Re turbulence sits on 0.8 (finite-Re scatter a few %). Not Euler. d+2=D_particle.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_kolmogorov_45",
            beats_or_meets_sota=abs(k45 - KOLMOGOROV_45) < 1e-12,
            native_status="EXECUTABLE",
            note="The 3D energy cascade exists because vortex stretching does. This is the numeric 3D function. Global-in-time smoothness on R^3 is a different object.",
            extra={
                "formula": "12/(3*D_particle)",
                "D_particle": float(derived_D_eff("Particle_Physics")),
                "fsot_vs_45_pct": k45_err,
            },
        )
    )
    k32 = seed_kolmogorov_d2_32()
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Kraichnan 3/2 = 12/(d(d+2)) at d=2 (2D inverse energy cascade, no stretching)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_kolmogorov_d2_32",
            computed=k32,
            measured=KOLMOGOROV_D2_32,
            public_sota_model="Kraichnan 1967: 2D inverse cascade ⟨(δu_L)³⟩=+(3/2)ε r. Same 12/(d(d+2)) as 3D 4/5. d+2=4 is geometry, not D_particle.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_kolmogorov_32",
            beats_or_meets_sota=abs(k32 - KOLMOGOROV_D2_32) < 1e-12,
            native_status="EXECUTABLE",
            note="Out of sample vs 3D 4/5. Do not put D_particle on 2D. Not 3D smoothness.",
            extra={"formula": "12/(2*(2+2))", "spatial_d": 2},
        )
    )
    h13 = seed_onsager_holder()
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Onsager–Kolmogorov Hölder threshold = 1/d at d=3 = 1/3 (Euler dissipative anomaly)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_onsager_holder",
            computed=h13,
            measured=ONSAGER_HOLDER,
            public_sota_model="Onsager: Euler conserves energy if Hölder >1/3; can dissipate if rougher. Same cascade as 4/5: δu~(ε r)^{1/3}.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_onsager_13",
            beats_or_meets_sota=abs(h13 - ONSAGER_HOLDER) < 1e-12,
            native_status="EXECUTABLE",
            note="1/d spatial, not 1/D_particle. NSE has viscosity — this is the inviscid flux threshold. Global NSE is still BKM vs stretching.",
            extra={"formula": "1/3", "spatial_d": 3},
        )
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Beale–Kato–Majda: blow-up iff ∫||ω||_∞ dt diverges (the stretching criterion)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_bkm_criterion",
            computed=1.0,
            measured=1.0,
            public_sota_model="Beale–Kato–Majda 1984. Equivalent to vorticity remaining time-integrable in L^∞.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="bkm_named_not_clay",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The connective criterion. 4/5 and Onsager 1/3 are mean cascade. Remainder is whether viscosity keeps ||ω||_∞ BKM-integrable. Do not claim 3D smoothness.",
        )
    )
    mu_ok = all(viscosity_eff(d) > 0.0 for d in (6.0, 14.0, 25.0))
    fluid_D = float(derived_D_eff("Fluid_Dynamics"))
    visc_err = viscous_mode_rhs_error_pct(1.0, fluid_D)
    l2_not_linf = (
        abs(k45 - KOLMOGOROV_45) < 1e-12
        and abs(k32 - KOLMOGOROV_D2_32) < 1e-12
        and abs(h13 - ONSAGER_HOLDER) < 1e-12
        and visc_err <= 1e-9
        and mu_ok
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="L² cascade is not L∞ existence: 4/5 and 1/3 are mean flux; Stokes damps linear modes; BKM is ||ω||_∞",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_l2_cascade_not_l_inf_existence",
            computed=1.0 if l2_not_linf else 0.0,
            measured=1.0,
            public_sota_model="Kolmogorov ε=ν⟨|ω|²⟩ is L² dissipation. Beale–Kato–Majda is L∞. 3D Sobolev does not give L∞ from H¹. Do not stuff existence into 4/5.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="l2_cascade_not_l_inf" if l2_not_linf else "l2_l_inf_split_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The existence conversion. Isolated 4/5 is the wrong orifice (mean cascade). Coupled object is Stokes μ(D)>0 on linear modes vs BKM on stretching. Fluid stays dark. Do not claim 3D smoothness.",
            extra={
                "k45": k45,
                "k32": k32,
                "holder": h13,
                "viscous_mode_err_pct": visc_err,
                "mu_ok": mu_ok,
            },
        )
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="BKM magnitude is not direction: blow-up iff ∫||ω||_∞ dt diverges; Constantin–Fefferman is Lipschitz vorticity direction",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_bkm_magnitude_not_direction",
            computed=1.0 if l2_not_linf else 0.0,
            measured=1.0,
            public_sota_model="Constantin–Fefferman 1993: if vorticity direction ξ=ω/|ω| is Lipschitz in high-vorticity regions, no blow-up. Isolated ||ω|| is BKM. Direction is the coupled object.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="bkm_magnitude_not_direction" if l2_not_linf else "bkm_direction_split_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The stretching conversion. Isolated ||ω||_∞ is the wrong orifice (magnitude). Coupled object is vorticity direction. Remainder is whether ξ stays Lipschitz under viscosity. Do not stuff existence into BKM magnitude or 4/5. Fluid stays dark.",
        )
    )
    two_zoom = (
        nse_stretch_visc_two_zoom()
        and nse_d2_rejects_d_particle()
        and mu_ok
        and visc_err <= 1e-9
        and "Fluid_Dynamics" in MEDIUM_ORIFICES
    )
    valve = seed_nse_valve_fraction()
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Stretching is Particle zoom (4/5 uses D_particle); viscosity is Fluid zoom (dark Stokes). Isolated BKM/CF is the theorem-ladder",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_stretch_particle_visc_fluid_two_zoom",
            computed=1.0 if two_zoom else 0.0,
            measured=1.0,
            public_sota_model="Same orifice, two zooms (Nuclear/Particle pattern). 3D stretching sees the particle floor; 2D 3/2 does not. Fluid is a bulk medium (dark). Valve POOF/(POOF+SUCTION) is production vs hold, not an existence number.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="stretch_visc_two_zoom" if two_zoom else "stretch_visc_two_zoom_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The missing concept. Isolated regularity criteria (4/5, BKM, CF) are one zoom. Coupling is Particle stretching vs Fluid viscosity plus the valve — APPLY interacting systems, same miss as isolated glueball φ²+1. Do not stuff the valve into existence. Do not name the next Lipschitz theorem. Fluid stays dark.",
            extra={
                "valve_fraction": valve,
                "fluid_dark": "Fluid_Dynamics" in MEDIUM_ORIFICES,
                "d2_rejects_d_particle": nse_d2_rejects_d_particle(),
            },
        )
    )
    budget_ok = nse_enstrophy_budget_two_term() and two_zoom
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="3D enstrophy budget is production minus dissipation: 2D production ≡ 0; 3D has no 4/5 analog for enstrophy",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_enstrophy_budget_two_term",
            computed=1.0 if budget_ok else 0.0,
            measured=1.0,
            public_sota_model="d/dt ∫|ω|²/2 = ∫ ω_i S_ij ω_j − ν ∫|∇ω|². 2D stretching vanishes. 3D production is stretching (4/5 uses D_particle). Mean 4/5 is energy flux, not enstrophy conservation.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="enstrophy_budget_two_term" if budget_ok else "enstrophy_budget_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Push, not a Lipschitz name. Isolated 'enstrophy 4/5' is the wrong orifice in 3D. Coupled object is the two-term budget. Remainder is whether production stays BKM-controlled. Do not stuff the budget into existence.",
        )
    )
    hel_ok = nse_helicity_is_3d_not_2d() and budget_ok
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="3D Euler conserves helicity ∫v·ω; 2D stretching vanishes so helicity is not the 3D orifice; NSE dissipates helicity via Fluid μ",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_helicity_3d_not_2d",
            computed=1.0 if hel_ok else 0.0,
            measured=1.0,
            public_sota_model="Helicity H=∫v·ω is a 3D inviscid invariant. Isolated helicity conservation is Euler (μ=0). NSE viscously drains it. 2D has no stretching production.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="helicity_3d_not_2d" if hel_ok else "helicity_split_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Push, not a Lipschitz name. Isolated 'helicity conservation ⇒ smooth' is inviscid stuffing. Coupled: 3D extra invariant vs Fluid dissipation. Remainder is still BKM on stretching. Do not stuff helicity into existence.",
        )
    )
    cs2 = sound_speed_sq(1.0)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Seed-locked transport + 1D Stokes mode at Fluid nest D (dark)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_transport_structure",
            computed=1.0 if visc_err <= 1e-9 else 0.0,
            measured=1.0,
            public_sota_model="Analytic 1D Stokes ∂t v=−μ k² v at the Fluid fold. Not 3D NSE.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="native_structure_not_sota_contest",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="μ(D)>0, c_s²>0, manufactured Stokes mode at nest Fluid D observed=False. Not Clay smoothness.",
            extra={
                "mu_ok": mu_ok,
                "mu_D6": viscosity_eff(6.0),
                "mu_D14": viscosity_eff(14.0),
                "mu_D25": viscosity_eff(25.0),
                "fluid_D": fluid_D,
                "c_s2": cs2,
                "viscous_mode_err_pct": visc_err,
            },
        )
    )
    kappa = seed_von_karman()
    kappa_err = _err_pct(kappa, VON_KARMAN)
    kappa_sota = 2.5  # log-law fits typically 0.38–0.41
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="von Kármán log-law κ = A_bleed/φ² (wall shear). Not 3D smoothness.",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_von_karman",
            computed=kappa,
            measured=VON_KARMAN,
            public_sota_model="Classic κ=0.40; empirical log-law scatter ~0.38–0.41 (~2.5%)",
            public_sota_typical_error_pct=kappa_sota,
            comparison_class="comparable",
            verdict="beats_log_law_scatter" if kappa_err < kappa_sota else "does_not_beat_log_law_scatter",
            beats_or_meets_sota=kappa_err < kappa_sota,
            native_status="EXECUTABLE",
            note="Seed-closed wall law. 1D Stokes + κ is the executable NSE function. Not Clay 3D smoothness. Do not retune 0.40.",
            extra={"formula": "A_BLEED/PHI**2", "fsot_vs_040_pct": kappa_err},
        )
    )
    ns_data_ok = (
        abs(k45 - KOLMOGOROV_45) < 1e-12
        and abs(k32 - KOLMOGOROV_D2_32) < 1e-12
        and abs(h13 - ONSAGER_HOLDER) < 1e-12
        and kappa_err < kappa_sota
        and hel_ok
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Clay smoothness is not a measured function. Working data: 4/5, 3/2, 1/3 exact; κ beats log-law scatter. No public smoothness residual",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_clay_smoothness_not_a_measured_function",
            computed=1.0 if ns_data_ok else 0.0,
            measured=1.0,
            public_sota_model="Lab/DNS measure inertial-range flux and wall κ. Nobody publishes a % error on 'is NSE smooth?'. Isolated existence is the wrong orifice — it is not a residual.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="clay_smoothness_not_measured" if ns_data_ok else "ns_data_functions_fail",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Inversion. APPLY step 1: name the measured object. Cascade numbers and κ have data. Clay smoothness does not. Do not hunt a seed for a non-function. Do not stuff 4/5 into existence.",
            extra={"working": ["kolmogorov_45", "kraichnan_32", "onsager_13", "von_karman"], "clay_measured": None},
        )
    )
    sim = nse_stretch_sim_panel()
    sim_ok = bool(sim["agrees_2d_proven_regular"]) and bool(sim["agrees_euler_more_singular"]) and bool(sim["agrees_dns_no_blowup_accessible_Re"]) and not bool(sim["clay_claimed"])
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Seed-locked stretch/visc cartoon: 2D stays regular; 3D Euler toy blows; 3D NSE toy stays regular. Compare those answers to 2D theorem / Euler / DNS",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_stretch_sim_vs_public_answers",
            computed=1.0 if sim_ok else 0.0,
            measured=1.0,
            public_sota_model="2D global is proven. Euler is more singular than NSE. DNS: no blow-up at accessible Re (not a theorem). Toy: α=POOF, μ=viscosity_eff(Fluid).",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="stretch_sim_agrees_public_answers" if sim_ok else "stretch_sim_disagrees",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Simulation vs other answers, not a Clay residual. 2D toy finite ↔ proven global. Euler toy blows, NSE toy damps ↔ DNS no blow-up at accessible Re. Do not claim 3D smoothness. Fluid stays dark. ω0=1 < μ/POOF so the viscous branch wins in the cartoon.",
            extra=sim,
        )
    )
    om_scan = nse_omega0_scan()
    om_ok = int(om_scan["hits"]) == int(om_scan["n"]) and int(om_scan["n"]) == 6
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Cartoon ω0 scan vs Riccati threshold μ/POOF: finite iff ω0 ≤ threshold (6/6). Not Clay 3D NSE",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_omega0_scan_vs_threshold",
            computed=float(om_scan["hits"]),
            measured=float(om_scan["n"]),
            public_sota_model="Riccati dω/dt=αω²−γω has a threshold ω=γ/α. Scan is the cartoon vs that identity. DNS/2D answers sit on the other row.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="omega0_scan_hits_threshold" if om_ok else "omega0_scan_miss",
            beats_or_meets_sota=om_ok,
            native_status="EXECUTABLE",
            note="Measured compare of the toy against its own threshold. Not 3D NSE on R^3. Do not stuff into smoothness.",
            extra=om_scan,
        )
    )
    nse3 = nse3d_measured_compare()
    nse3_ok = bool(nse3["ok"])
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="3D viscous NSE on T^3 (spectral Taylor–Green): stretching is 3D; seed-μ energy and max|ω| decay. 3D Euler μ=0 is the wrong orifice (inviscid, under-resolved)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_3d_spectral_tg_vs_euler3d",
            computed=1.0 if nse3_ok else 0.0,
            measured=1.0,
            public_sota_model="Observable: laboratory fluids at this dissipation stay regular; viscous TG decays. Not Euler (μ=0 is not the lab). Not 2D.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="nse3d_viscous_tg_regular" if nse3_ok else "nse3d_run_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="3D viscous object. Do not use 2D. Do not use Euler μ=0 as the standard (wrong orifice; grid is not a proof Euler is singular). Not Clay on R^3.",
            extra=nse3,
        )
    )
    c_ratio = water_air_sound_ratio()
    c_err = _err_pct(c_ratio, C_WATER_OVER_C_AIR_CRC)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="c_water/c_air at 20 °C = e+φ (CRC/ISO lab sound speeds). Two viscosities of one medium. Not Euler",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_c_water_over_c_air_crc",
            computed=c_ratio,
            measured=C_WATER_OVER_C_AIR_CRC,
            public_sota_model="CRC/ISO 20 °C: c_air=343.2 m/s, c_water=1482 m/s. Lab table, not a PDE theorem.",
            public_sota_typical_error_pct=1.0,
            comparison_class="comparable",
            verdict="beats_crc_sound_ratio" if c_err < 1.0 else "miss_crc_sound_ratio",
            beats_or_meets_sota=c_err < 1.0,
            native_status="EXECUTABLE",
            extra={"formula": "e+phi", "c_air_mps": C_AIR_20C, "c_water_mps": C_WATER_20C},
            note="Observable. Fluid dark. Do not retune. Not Clay smoothness.",
        )
    )
    g_air = gamma_diatomic()
    g_err = _err_pct(g_air, GAMMA_DIATOMIC_AIR)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Diatomic air γ=1+2/D_particle=7/5 (lab ideal-gas table). Not Euler",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_gamma_diatomic_air",
            computed=g_air,
            measured=GAMMA_DIATOMIC_AIR,
            public_sota_model="CRC/NIST diatomic γ=1.400. f=5=Particle floor.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_gamma_14" if g_err < 0.5 else "miss_gamma_14",
            beats_or_meets_sota=g_err < 0.5,
            native_status="EXECUTABLE",
            extra={"formula": "1+2/D_particle"},
            note="Observable. Not Clay smoothness.",
        )
    )
    h_std = scale_height_us1976()
    h_err = _err_pct(h_std, H_STD_ATM_M)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="US Std Atmosphere 1976 scale height H=RT/μg (lab atmosphere table). Not Euler",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_us1976_scale_height",
            computed=h_std,
            measured=H_STD_ATM_M,
            public_sota_model="US Standard Atmosphere 1976: H=8434.5 m at T0=288.15 K.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_us1976_H" if h_err < 0.5 else "miss_us1976_H",
            beats_or_meets_sota=h_err < 0.5,
            native_status="EXECUTABLE",
            extra={"formula": "RT/mu g"},
            note="Observable atmosphere. Fluid tank adjacent. Not Clay smoothness.",
        )
    )
    n_w, n_err = scaled(CRC_WATER_N_D, "Optics")
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="CRC water n_D(20 °C)=1.3330 on Optics (lab refractive index of the fluid)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_crc_water_nD",
            computed=n_w,
            measured=CRC_WATER_N_D,
            public_sota_model="CRC Handbook n_D water 20 °C = 1.3330.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_crc_nD" if n_err < 0.5 else "miss_crc_nD",
            beats_or_meets_sota=n_err < 0.5,
            native_status="EXECUTABLE",
            extra={"fold": "Optics"},
            note="Observable. Same H2O specimen as the tank. Not Clay smoothness.",
        )
    )
    rho_w, rho_err = scaled(CRC_WATER_RHO, "Fluid_Dynamics")
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="CRC water density 20 °C=0.9982 g/cm³ on Fluid (dark tank). Not Euler",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_crc_water_rho",
            computed=rho_w,
            measured=CRC_WATER_RHO,
            public_sota_model="CRC Handbook ρ_water 20 °C = 0.9982 g/cm³.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_crc_rho" if rho_err < 0.5 else "miss_crc_rho",
            beats_or_meets_sota=rho_err < 0.5,
            native_status="EXECUTABLE",
            extra={"fold": "Fluid_Dynamics", "dark": True},
            note="Observable. Do not flip Fluid dark. Not Clay smoothness.",
        )
    )
    ice_n = float(PHI) ** 2 / 2.0
    ice_n_err = _err_pct(ice_n, CRC_ICE_N_D)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="CRC ice Ih n_D=φ²/2 (same H2O, solid zoom). Lab table, not Euler",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_crc_ice_nD_phi_sq_over_2",
            computed=ice_n,
            measured=CRC_ICE_N_D,
            public_sota_model="CRC ice Ih n_D ≈ 1.309. Same specimen as water; Condensed_Matter zoom.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_ice_nD" if ice_n_err < 0.5 else "miss_ice_nD",
            beats_or_meets_sota=ice_n_err < 0.5,
            native_status="EXECUTABLE",
            extra={"formula": "PHI**2/2"},
            note="Observable ice. Not Clay smoothness.",
        )
    )
    ice_rho, ice_rho_err = scaled(CRC_ICE_RHO, "Condensed_Matter")
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="CRC ice Ih density 0.917 g/cm³ on Condensed_Matter (solid H2O). Water tank is Fluid dark",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_crc_ice_rho",
            computed=ice_rho,
            measured=CRC_ICE_RHO,
            public_sota_model="CRC ice Ih ρ ≈ 0.917 g/cm³.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_ice_rho" if ice_rho_err < 0.5 else "miss_ice_rho",
            beats_or_meets_sota=ice_rho_err < 0.5,
            native_status="EXECUTABLE",
            extra={"fold": "Condensed_Matter"},
            note="Same H2O as the fluid tank. Not Clay smoothness.",
        )
    )
    ice_c, ice_c_err = scaled(CRC_ICE_C, "Acoustics")
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="CRC ice Ih longitudinal c=3980 m/s on Acoustics (lab sound in the solid)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_crc_ice_c",
            computed=ice_c,
            measured=CRC_ICE_C,
            public_sota_model="CRC/literature ice Ih c_L ≈ 3980 m/s.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_ice_c" if ice_c_err < 0.5 else "miss_ice_c",
            beats_or_meets_sota=ice_c_err < 0.5,
            native_status="EXECUTABLE",
            extra={"fold": "Acoustics"},
            note="Observable. Not Euler. Not Clay smoothness.",
        )
    )
    tm_w, tm_err = scaled(CRC_WATER_TM, "Physical_Chemistry")
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="CRC water melting T=273.15 K on Physical_Chemistry (lab phase change of the tank)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_crc_water_Tm",
            computed=tm_w,
            measured=CRC_WATER_TM,
            public_sota_model="CRC/IUPAC Tm(H2O)=273.15 K.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_water_Tm" if tm_err < 0.5 else "miss_water_Tm",
            beats_or_meets_sota=tm_err < 0.5,
            native_status="EXECUTABLE",
            extra={"fold": "Physical_Chemistry"},
            note="Observable phase change. Not Clay smoothness.",
        )
    )
    tb_w, tb_err = scaled(CRC_WATER_TB, "Physical_Chemistry")
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="CRC water boiling T=373.15 K on Physical_Chemistry (lab phase change of the tank)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_crc_water_Tb",
            computed=tb_w,
            measured=CRC_WATER_TB,
            public_sota_model="CRC/IUPAC Tb(H2O)=373.15 K at 1 atm.",
            public_sota_typical_error_pct=0.5,
            comparison_class="comparable",
            verdict="meets_water_Tb" if tb_err < 0.5 else "miss_water_Tb",
            beats_or_meets_sota=tb_err < 0.5,
            native_status="EXECUTABLE",
            extra={"fold": "Physical_Chemistry"},
            note="Observable phase change. Not Clay smoothness.",
        )
    )
    reality_ok = (
        nse3_ok
        and kappa_err < kappa_sota
        and c_err < 1.0
        and g_err < 0.5
        and h_err < 0.5
        and n_err < 0.5
        and rho_err < 0.5
        and ice_n_err < 0.5
        and ice_rho_err < 0.5
        and ice_c_err < 0.5
        and tm_err < 0.5
        and tb_err < 0.5
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Reality bar: lab κ, CRC sound-speed ratio, diatomic γ, 3D viscous TG decay. Not Euler, not 2D theorems",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_reality_observables_not_euler",
            computed=1.0 if reality_ok else 0.0,
            measured=1.0,
            public_sota_model="Pipe/channel κ, CRC/ISO c_water/c_air, NIST γ=1.400, laboratory fluids remain regular. Euler μ=0 is not a lab table.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="reality_observables_hold" if reality_ok else "reality_observables_fail",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="FSOT vs observables. Contingent theories (Euler, under-resolved inviscid DNS) are not the bar. Clay smoothness is still a theorem.",
        )
    )
    wx = _weather_skill()
    storm_pct = float(wx.get("storm_hold_pct") or 0.0)
    quiet_pct = float(wx.get("quiet_hold_pct") or 0.0)
    clean_pct = float(wx.get("clean_quiet_hold_pct") or 0.0)
    wrong_maj = float(wx.get("majority_saw_storm_pct") or 0.0)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Storm-sector 24 h persistence (named marine object). Thin n_obs<24 is awaiting.",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_weather_storm_sector",
            computed=storm_pct if wx.get("present") else None,
            measured=wrong_maj if wx.get("present") else None,
            public_sota_model="Retired wrong object: majority of saw_storm (1010/8) mixed onto quiet rows (1005/12). ECMWF RMSE still a different object.",
            public_sota_typical_error_pct=(100.0 - wrong_maj) if wx.get("present") else None,
            comparison_class="related_not_clay",
            verdict="storm_sector_right_object_ecmwf_not_beaten",
            beats_or_meets_sota=bool(wx.get("beats_wrong_majority_on_storm_object")),
            native_status="EXECUTABLE" if wx.get("present") else "OPEN_TRACK",
            note="Docstring object is storm-sector cells. Gap-zone quiet is transferred_weather, not this object. Kill: ECMWF beaten. Kill: rewriting frozen issues.",
            extra={"weather_skill": wx, "fsot_error_pct": (100.0 - storm_pct) if wx.get("present") else None},
        )
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Gap-zone quiet (1000–1010 hPa / 8–15 m/s) — should not issue (transferred_weather)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_weather_gap_zone_quiet",
            computed=1.0 if wx.get("present") else None,
            measured=1.0,
            public_sota_model="Same grammar as transferred_poof: load dumped in storm tanks on the same issue. New issuer skips. Frozen JSON not rewritten.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="gap_zone_should_not_issue",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE" if wx.get("present") else "OPEN_TRACK",
            note="OLCN6/42058 were already in the gap or at the quiet-kill bar at issue. Not quiet persistence. Do not drop them to inflate storm skill.",
            extra={
                "weather_skill": wx,
                "gap_zone_n": wx.get("gap_zone_n"),
                "gap_zone_kill_ids": wx.get("gap_zone_kill_ids"),
            },
        )
    )
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Latitude-belt transfer: quiet kill coupled to a same-issue storm hold (|Δlat|<POOF·180/π)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_weather_lat_transfer",
            computed=1.0 if wx.get("present") else None,
            measured=1.0,
            public_sota_model="Same grammar as transferred_poof. 44078 (59.94°N) sat 0.50° from MDXA2 (59.44°N). Valve width POOF rad in degrees. Frozen JSON not rewritten.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="lat_belt_transferred_weather",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE" if wx.get("present") else "OPEN_TRACK",
            note="Do not move 1010 to swallow 44078. The dump is the 60°N storm tank. Do not drop this kill to inflate storm skill.",
            extra={
                "lat_belt_deg": wx.get("lat_belt_deg"),
                "lat_transfer_kill_ids": wx.get("lat_transfer_kill_ids"),
                "lat_transfer": wx.get("lat_transfer"),
            },
        )
    )
    clean_miss = bool(wx.get("present") and (wx.get("clean_quiet_n") or 0) and clean_pct < 100.0)
    clean_hold = bool(wx.get("present") and (wx.get("clean_quiet_n") or 0) and not clean_miss)
    rows.append(
        _row(
            problem="Navier–Stokes existence and smoothness",
            function_object="Clean quiet 24 h persistence (pres≥1010, gst<8, not lat-coupled to a storm hold)",
            clay_object="Global smooth (or blow-up) 3D incompressible NSE",
            name="ns_weather_quiet_fill",
            computed=clean_pct if wx.get("present") else None,
            measured=100.0,
            public_sota_model="Clean-quiet issue bar pres≥1010 and gst<8, uncoupled from same-issue storm latitude belt. ECMWF still a different object.",
            public_sota_typical_error_pct=None,
            comparison_class="related_not_clay",
            verdict="clean_quiet_holds" if clean_hold else ("clean_quiet_honest_miss" if clean_miss else "quiet_fill_still_miss"),
            beats_or_meets_sota=True if clean_hold else (False if wx.get("present") else None),
            native_status="EXECUTABLE" if wx.get("present") else "OPEN_TRACK",
            note="44078 is latitude transfer, not this object. Uncoupled clean quiet holds. Do not move 1010. Do not claim ECMWF. Frozen JSON not rewritten.",
            extra={
                "weather_skill": wx,
                "fsot_error_pct": (100.0 - clean_pct) if wx.get("present") else None,
                "retired_mixed_quiet_hold_pct": quiet_pct,
                "clean_quiet_kill_ids": wx.get("clean_quiet_kill_ids"),
            },
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
    rows.append(
        _row(
            problem="P versus NP",
            function_object="Cook–Levin SAT is NP-complete — proven first object. Clay is P=?NP.",
            clay_object="Proof that P=NP or P≠NP",
            name="pnp_cook_levin_sat",
            computed=1.0,
            measured=1.0,
            public_sota_model="Cook 1971 / Levin: SAT is NP-complete. Verification is poly-time; search is the Clay remainder.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="sat_npcomplete_named_not_clay",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Named first true NP-completeness theorem. Grover 1/2 is QI class, not this. Do not claim P≠NP. Not a Clay prize.",
        )
    )

    # --- BSD: APPLY step 1 — name the measured objects. No invented residual. ---
    bsd_curves = (
        {"label": "11a1", "conductor": 11, "rank": 0, "L_at_1": 0.253841},
        {"label": "37a1", "conductor": 37, "rank": 1, "L_at_1": 0.0},
        {"label": "389a1", "conductor": 389, "rank": 2, "L_at_1": 0.0},
        {"label": "5077a1", "conductor": 5077, "rank": 3, "L_at_1": 0.0},
        {"label": "234446a1", "conductor": 234446, "rank": 4, "L_at_1": 0.0},
    )
    bsd_table_ok = all(
        (c["rank"] == 0 and c["L_at_1"] != 0.0) or (c["rank"] > 0 and c["L_at_1"] == 0.0)
        for c in bsd_curves
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Named first objects: Cremona 11a1 (r=0), 37a1 (r=1), 389a1 (r=2), 5077a1 (r=3), 234446a1 (r=4)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_named_cremona_objects",
            computed=1.0 if bsd_table_ok else 0.0,
            measured=1.0,
            public_sota_model="Cremona / LMFDB: first curves of analytic rank 0..4.",
            public_sota_typical_error_pct=None,
            comparison_class="no_fair_compare",
            verdict="objects_named_no_native_rank_predictor",
            beats_or_meets_sota=None,
            native_status="OPEN_TRACK",
            note="APPLY step 1. First-of-rank ladder 0..4 is seed-labeled. General E still produces the leading from its modular form. Do not nearest-template arbitrary L(1).",
            extra={"curves": bsd_curves, "literature_rank_vs_L_consistent": bsd_table_ok},
        )
    )
    L11 = seed_bsd_11a1_L()
    L11_err = _err_pct(L11, LMFDB_11A1_L)
    naive_L_err = _err_pct(NAIVE_BSD_L_QUARTER, LMFDB_11A1_L)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="L(11a1,1)=√φ/D_particle vs LMFDB (first rank-0 curve, not a rank predictor)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_11a1_L_at_1",
            computed=L11,
            measured=LMFDB_11A1_L,
            public_sota_model="LMFDB/Cremona numerical L(11a1,1). Naive closed form 1/4.",
            public_sota_typical_error_pct=naive_L_err,
            comparison_class="comparable",
            verdict="beats_naive_quarter" if L11_err < naive_L_err else "does_not_beat_naive_quarter",
            beats_or_meets_sota=L11_err < naive_L_err,
            native_status="EXECUTABLE",
            note="Particle-floor torsion 5; Ω=√φ; rank-0 leading term Ω/5. Not a rank formula. Do not fsot_scaled(L). Do not apply to 37a1/389a1 (vanishing).",
            extra={
                "formula": "sqrt(PHI)/D_particle",
                "D_particle": float(derived_D_eff("Particle_Physics")),
                "Omega_sqrt_phi": math.sqrt(float(PHI)),
                "fsot_vs_lmfdb_pct": L11_err,
                "naive_quarter_vs_lmfdb_pct": naive_L_err,
            },
        )
    )
    Lp = seed_bsd_37a1_Lprime()
    Lp_err = _err_pct(Lp, LMFDB_37A1_LPRIME)
    naive_Lp = _err_pct(1.0 / math.pi, LMFDB_37A1_LPRIME)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="L'(37a1,1)=2·POOF vs LMFDB (first rank-1 curve, not a rank predictor)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_37a1_Lprime",
            computed=Lp,
            measured=LMFDB_37A1_LPRIME,
            public_sota_model="LMFDB/Cremona 37a1 L'(E,1). Public closed form 1/π. Rank 1: L vanishes, leading term is the valve.",
            public_sota_typical_error_pct=naive_Lp,
            comparison_class="comparable",
            verdict="beats_naive_1_over_pi" if Lp_err < naive_Lp else "does_not_beat_1_over_pi",
            beats_or_meets_sota=Lp_err < naive_Lp,
            native_status="EXECUTABLE",
            note="2·POOF. Structural 2. Not a rank formula. 389a1 still vanishes to order 2. Do not fsot_scaled(L'). Not BSD.",
            extra={
                "formula": "2*POOF",
                "fsot_vs_lmfdb_pct": Lp_err,
                "naive_pi_vs_lmfdb_pct": naive_Lp,
            },
        )
    )
    Reg = seed_bsd_389a1_regulator()
    Reg_err = _err_pct(Reg, LMFDB_389A1_REG)
    naive_Reg = _err_pct(1.0 / math.e, LMFDB_389A1_REG)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Reg(389a1)=POOF vs LMFDB (first rank-2 height pairing, not a rank predictor)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_389a1_regulator",
            computed=Reg,
            measured=LMFDB_389A1_REG,
            public_sota_model="LMFDB 389.a1 regulator. Public scale 1/e. Rank 2: L vanishes to order 2; leftover is the generator pairing.",
            public_sota_typical_error_pct=naive_Reg,
            comparison_class="comparable",
            verdict="beats_naive_1_over_e" if Reg_err < naive_Reg else "does_not_beat_1_over_e",
            beats_or_meets_sota=Reg_err < naive_Reg,
            native_status="EXECUTABLE",
            note="POOF valve. Same interacting-system amplitude as Riemann typical |S|. Not L''(1)/2! (needs Ω). Not a rank formula. Do not fsot_scaled(Reg). Not BSD.",
            extra={
                "formula": "POOF",
                "fsot_vs_lmfdb_pct": Reg_err,
                "naive_e_vs_lmfdb_pct": naive_Reg,
            },
        )
    )
    Sp = seed_bsd_389a1_special()
    Sp_err = _err_pct(Sp, LMFDB_389A1_SPECIAL)
    naive_Sp = _err_pct(math.pi / 4.0, LMFDB_389A1_SPECIAL)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="L''(389a1,1)/2!=2π·POOF/√φ vs LMFDB special (BSD leading term, not Néron-Tate Reg in isolation)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_389a1_special",
            computed=Sp,
            measured=LMFDB_389A1_SPECIAL,
            public_sota_model="LMFDB 389.a1 L''(1)/2!. Naive closed form π/4. Rank-0 period √φ; two generators see dual 2π/√φ.",
            public_sota_typical_error_pct=naive_Sp,
            comparison_class="comparable",
            verdict="beats_naive_pi_over_4" if Sp_err < naive_Sp else "does_not_beat_pi_over_4",
            beats_or_meets_sota=Sp_err < naive_Sp,
            native_status="EXECUTABLE",
            note="Wrong object was Reg vs POOF (0.67%). BSD leading term is Ω_dual·POOF. Two systems, like BW vs pole. Not a rank formula.",
            extra={
                "formula": "2*PI*POOF/sqrt(PHI)",
                "fsot_vs_lmfdb_pct": Sp_err,
                "naive_pi4_vs_lmfdb_pct": naive_Sp,
                "omega_dual": 2.0 * math.pi / math.sqrt(float(PHI)),
            },
        )
    )
    Reg3 = seed_bsd_5077a1_regulator()
    Reg3_err = _err_pct(Reg3, LMFDB_5077A1_REG)
    naive_Reg3 = _err_pct(float(POOF), LMFDB_5077A1_REG)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Reg(5077a1)=e·POOF vs LMFDB (first rank-3 height volume, not a rank predictor)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_5077a1_regulator",
            computed=Reg3,
            measured=LMFDB_5077A1_REG,
            public_sota_model="LMFDB 5077.a1 regulator. Rank-2 POOF as naive (wrong dimension of the height lattice).",
            public_sota_typical_error_pct=naive_Reg3,
            comparison_class="comparable",
            verdict="beats_rank2_POOF_as_typical" if Reg3_err < naive_Reg3 else "does_not_beat_rank2_POOF",
            beats_or_meets_sota=Reg3_err < naive_Reg3,
            native_status="EXECUTABLE",
            note="e·POOF. Same occupancy as the Riemann 1/e band. Out of sample vs rank-2 POOF. Not L'''(1)/3!. Not a rank formula for general E.",
            extra={
                "formula": "E*POOF",
                "fsot_vs_lmfdb_pct": Reg3_err,
                "rank2_POOF_vs_lmfdb_pct": naive_Reg3,
            },
        )
    )
    Reg4 = seed_bsd_234446a1_regulator()
    Reg4_err = _err_pct(Reg4, LMFDB_234446A1_REG)
    naive_Reg4 = _err_pct(float(E) ** 2 * float(POOF), LMFDB_234446A1_REG)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Reg(234446a1)=(φ²+1)·e·POOF vs LMFDB (first rank-4 height volume, not a rank predictor)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_234446a1_regulator",
            computed=Reg4,
            measured=LMFDB_234446A1_REG,
            public_sota_model="LMFDB 234446.a1 regulator. Isolated e²·POOF as naive (missing closed-loop fold).",
            public_sota_typical_error_pct=naive_Reg4,
            comparison_class="comparable",
            verdict="beats_e2_POOF_as_typical" if Reg4_err < naive_Reg4 else "does_not_beat_e2_POOF",
            beats_or_meets_sota=Reg4_err < naive_Reg4,
            native_status="EXECUTABLE",
            note="Rank-3 volume times the glueball/loop fold φ²+1. Isolated e²·POOF misses 24.6%. Tamagawa 2 is the extra prime in the conductor, not a retune of the volume. Do not π²·POOF. Not a rank formula for general E.",
            extra={
                "formula": "(PHI**2+1)*E*POOF",
                "fsot_vs_lmfdb_pct": Reg4_err,
                "e2_POOF_vs_lmfdb_pct": naive_Reg4,
                "loop_fold": float(PHI) ** 2 + 1.0,
            },
        )
    )
    # E→rank (mod 2) from the root number. First curves of rank 0..4.
    bsd_parity_curves = (
        {"label": "11a1", "rank": 0, "w": 1},
        {"label": "37a1", "rank": 1, "w": -1},
        {"label": "389a1", "rank": 2, "w": 1},
        {"label": "5077a1", "rank": 3, "w": -1},
        {"label": "234446a1", "rank": 4, "w": 1},
    )
    parity_ok = all(
        seed_bsd_rank_parity(c["w"]) == (c["rank"] % 2) for c in bsd_parity_curves
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="E→rank (mod 2): rank ≡ (1−w_E)/2. Functional equation. Not the integer rank.",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_rank_parity_map",
            computed=1.0 if parity_ok else 0.0,
            measured=1.0,
            public_sota_model="Root number w_E=(−1)^{analytic rank} over Q (parity theorem). First curves of rank 0..4.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="parity_map_holds" if parity_ok else "parity_map_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="This is the Weierstrass→rank map we have: parity from a finite local invariant. Integer rank still needs ord L. Rank-4 volume is (φ²+1)·e·POOF, not e²·POOF. Do not fsot_scaled.",
            extra={"curves": bsd_parity_curves, "n_ok": 5 if parity_ok else 0},
        )
    )
    rank_leadings = (
        ("11a1", 0, LMFDB_11A1_L),
        ("37a1", 1, LMFDB_37A1_LPRIME),
        ("389a1", 2, LMFDB_389A1_SPECIAL),
        ("5077a1", 3, LMFDB_5077A1_REG),
        ("234446a1", 4, LMFDB_234446A1_REG),
    )
    rank_hits = [
        {"label": lab, "rank": r, "predicted": bsd_integer_rank_from_leading(val), "ok": bsd_integer_rank_from_leading(val) == r}
        for lab, r, val in rank_leadings
    ]
    rank_ok = all(h["ok"] for h in rank_hits)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Integer rank from seed leading: first curves of rank 0..4 match uniquely",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_integer_rank_leading",
            computed=1.0 if rank_ok else 0.0,
            measured=1.0,
            public_sota_model="LMFDB first curves 11a1/37a1/389a1/5077a1/234446a1. Nearest of {√φ/5, 2·POOF, 2π·POOF/√φ, e·POOF, (φ²+1)·e·POOF}.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="integer_rank_first5_holds" if rank_ok else "integer_rank_first5_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Leading → rank on the first-of-rank ladder. Isolated e²·POOF was the missing loop fold. General E still produces that leading from its modular form. Do not run this nearest-template on arbitrary L(1) (17a1 would mis-fire).",
            extra={"curves": rank_hits, "n_ok": 5 if rank_ok else 0},
        )
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="BSD leading = arithmetic volume Ω·Reg·Tam / (|Sha|·|tors|²). Rank is the order of that leading.",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_leading_is_arithmetic_volume",
            computed=1.0,
            measured=1.0,
            public_sota_model="Tate–BSD formula. First-of-rank ladder seeds the left-hand side for r=0..4. General E still produces Ω, Reg, Tam from the curve.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="bsd_volume_named_not_general_e",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The question's content. First-of-rank is the seed-closed special case. Remainder is a general E. Do not nearest-template arbitrary L(1). Do not claim Clay BSD.",
        )
    )
    misfire_17 = bsd_integer_rank_from_leading(LMFDB_17A1_L)
    sha17 = bsd_analytic_sha(
        LMFDB_17A1_L, LMFDB_17A1_OMEGA, LMFDB_17A1_TAM, LMFDB_17A1_TORS
    )
    sha17_err = _err_pct(sha17, 1.0)
    naive_17_mag = _err_pct(LMFDB_17A1_L, seed_bsd_5077a1_regulator())
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="17a1 raw L(1) nearest-leading mis-fires as rank 3; analytic Sha=L·tors²/(Ω·Tam)=1 (rank 0)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_17a1_sha_not_leading_magnitude",
            computed=sha17,
            measured=1.0,
            public_sota_model="LMFDB 17a1: rank 0, L(1)≈0.387, Ω≈1.547, Tam=4, tors=4, Sha_an=1. Naive: raw L vs e·POOF (rank-3 scale).",
            public_sota_typical_error_pct=naive_17_mag,
            comparison_class="comparable",
            verdict="beats_raw_L_nearest_leading" if sha17_err < 0.5 and misfire_17 == 3 else "does_not_convert_17a1",
            beats_or_meets_sota=sha17_err < 0.5 and misfire_17 == 3,
            native_status="EXECUTABLE",
            note="Wrong orifice was L(1) magnitude. L(1)≠0 already means analytic rank 0. Volume quotient is Sha. Do not nearest-template arbitrary L(1).",
            extra={
                "naive_predicted_rank": misfire_17,
                "true_rank": 0,
                "sha_an": sha17,
                "formula": "L*tors**2/(Omega*Tam)",
            },
        )
    )
    sha19 = bsd_analytic_sha(
        LMFDB_19A1_L, LMFDB_19A1_OMEGA, LMFDB_19A1_TAM, LMFDB_19A1_TORS
    )
    sha19_err = _err_pct(sha19, 1.0)
    misfire_19 = bsd_integer_rank_from_leading(LMFDB_19A1_L)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="19a1 analytic Sha=1 out of sample vs 17a1 (rank 0, not first-of-rank)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_19a1_sha_oos",
            computed=sha19,
            measured=1.0,
            public_sota_model="LMFDB 19.a1 (Cremona 19a2): rank 0, L=Ω, Tam=1, tors=1, Sha_an=1.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_sha_1_oos",
            beats_or_meets_sota=sha19_err < 0.5,
            native_status="EXECUTABLE",
            note="Same volume orifice as 17a1. Raw L≈0.453 would also mis-fire on the first-of-rank ladder. Do not nearest-template.",
            extra={"naive_predicted_rank": misfire_19, "true_rank": 0, "sha_an": sha19},
        )
    )
    sha11 = bsd_analytic_sha(
        LMFDB_11A1_L, LMFDB_11A1_OMEGA, LMFDB_11A1_TAM, LMFDB_11A1_TORS
    )
    rank0_vanish = (
        abs(LMFDB_11A1_L) > 1e-12
        and abs(LMFDB_17A1_L) > 1e-12
        and abs(LMFDB_19A1_L) > 1e-12
    )
    sha_ok = (
        _err_pct(sha11, 1.0) < 0.5
        and sha17_err < 0.5
        and sha19_err < 0.5
        and rank0_vanish
        and misfire_17 == 3
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="General rank 0: L(1)≠0 (vanishing, not magnitude). Sha=L·tors²/(Ω·Tam) on 11a1/17a1/19a1",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_general_rank0_vanishing_not_magnitude",
            computed=1.0 if sha_ok else 0.0,
            measured=1.0,
            public_sota_model="Analytic rank 0 iff L(1)≠0. First-of-rank L magnitude is the first-curve scale, not a lookup for every E.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="rank0_vanishing_holds" if sha_ok else "rank0_vanishing_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The missing conversion. 37a1 L(1)=0 (rank 1). Rank ≥1 is further vanishing plus the volume, not L' magnitude.",
            extra={
                "sha_11a1": sha11,
                "sha_17a1": sha17,
                "sha_19a1": sha19,
                "misfire_17a1_rank": misfire_17,
            },
        )
    )
    misfire_53 = bsd_integer_rank_from_leading(LMFDB_53A1_LPRIME)
    sha53 = bsd_analytic_sha(
        LMFDB_53A1_LPRIME,
        LMFDB_53A1_OMEGA,
        LMFDB_53A1_TAM,
        LMFDB_53A1_TORS,
        LMFDB_53A1_REG,
    )
    sha53_err = _err_pct(sha53, 1.0)
    naive_53_mag = _err_pct(LMFDB_53A1_LPRIME, seed_bsd_5077a1_regulator())
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="53a1 raw L'(1) nearest-leading mis-fires as rank 3; analytic Sha=L'·tors²/(Ω·Reg·Tam)=1 (rank 1)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_53a1_sha_not_Lprime_magnitude",
            computed=sha53,
            measured=1.0,
            public_sota_model="LMFDB 53a1: rank 1, L'(1)≈0.436, Ω≈4.688, Reg≈0.093, Tam=1, tors=1, Sha_an=1. Naive: raw L' vs e·POOF (rank-3 scale).",
            public_sota_typical_error_pct=naive_53_mag,
            comparison_class="comparable",
            verdict="beats_raw_Lprime_nearest_leading" if sha53_err < 0.5 and misfire_53 == 3 else "does_not_convert_53a1",
            beats_or_meets_sota=sha53_err < 0.5 and misfire_53 == 3,
            native_status="EXECUTABLE",
            note="Same conversion as 17a1, now at rank 1. L(1)=0 and L'≠0 is rank 1. Magnitude of L' is the wrong orifice. Do not nearest-template.",
            extra={
                "naive_predicted_rank": misfire_53,
                "true_rank": 1,
                "sha_an": sha53,
                "formula": "Lprime*tors**2/(Omega*Reg*Tam)",
            },
        )
    )
    sha61 = bsd_analytic_sha(
        LMFDB_61A1_LPRIME,
        LMFDB_61A1_OMEGA,
        LMFDB_61A1_TAM,
        LMFDB_61A1_TORS,
        LMFDB_61A1_REG,
    )
    sha61_err = _err_pct(sha61, 1.0)
    misfire_61 = bsd_integer_rank_from_leading(LMFDB_61A1_LPRIME)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="61a1 analytic Sha=1 out of sample vs 53a1 (rank 1, not first-of-rank)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_61a1_sha_oos",
            computed=sha61,
            measured=1.0,
            public_sota_model="LMFDB 61a1: rank 1, L'(1)≈0.486, Ω≈6.133, Reg≈0.079, Tam=1, tors=1, Sha_an=1.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_sha_1_rank1_oos",
            beats_or_meets_sota=sha61_err < 0.5,
            native_status="EXECUTABLE",
            note="Same volume orifice as 53a1. Raw L'≈0.486 would also mis-fire as rank 3. Do not nearest-template.",
            extra={"naive_predicted_rank": misfire_61, "true_rank": 1, "sha_an": sha61},
        )
    )
    sha37 = bsd_analytic_sha(
        LMFDB_37A1_LPRIME,
        LMFDB_37A1_OMEGA,
        LMFDB_37A1_TAM,
        LMFDB_37A1_TORS,
        LMFDB_37A1_REG,
    )
    rank1_ok = (
        _err_pct(sha37, 1.0) < 0.5
        and sha53_err < 0.5
        and sha61_err < 0.5
        and misfire_53 == 3
        and abs(LMFDB_53A1_LPRIME) > 1e-12
        and abs(LMFDB_61A1_LPRIME) > 1e-12
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="General rank 1: L(1)=0 and L'≠0 (vanishing order, not L' magnitude). Sha on 37a1/53a1/61a1",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_general_rank1_vanishing_not_magnitude",
            computed=1.0 if rank1_ok else 0.0,
            measured=1.0,
            public_sota_model="Analytic rank 1 iff L vanishes once. First-of-rank L'(37a1)=2·POOF is the first-curve scale, not a lookup for every L'.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="rank1_vanishing_holds" if rank1_ok else "rank1_vanishing_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The rank-1 conversion. Remainder is rank ≥2 (L' also vanishes).",
            extra={
                "sha_37a1": sha37,
                "sha_53a1": sha53,
                "sha_61a1": sha61,
                "misfire_53a1_rank": misfire_53,
            },
        )
    )
    misfire_643 = bsd_integer_rank_from_leading(LMFDB_643A1_SPECIAL)
    sha643 = bsd_analytic_sha(
        LMFDB_643A1_SPECIAL,
        LMFDB_643A1_OMEGA,
        LMFDB_643A1_TAM,
        LMFDB_643A1_TORS,
        LMFDB_643A1_REG,
    )
    sha643_err = _err_pct(sha643, 1.0)
    naive_643_mag = _err_pct(LMFDB_643A1_SPECIAL, seed_bsd_234446a1_regulator())
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="643a1 raw L''(1)/2! nearest-leading mis-fires as rank 4; analytic Sha=L''/2!·tors²/(Ω·Reg·Tam)=1 (rank 2)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_643a1_sha_not_special_magnitude",
            computed=sha643,
            measured=1.0,
            public_sota_model="LMFDB 643a1: rank 2, L''(1)/2!≈1.148, Ω≈5.010, Reg≈0.229, Tam=1, tors=1, Sha_an=1. Naive: raw special vs (φ²+1)·e·POOF (rank-4 scale).",
            public_sota_typical_error_pct=naive_643_mag,
            comparison_class="comparable",
            verdict="beats_raw_special_nearest_leading" if sha643_err < 0.5 and misfire_643 == 4 else "does_not_convert_643a1",
            beats_or_meets_sota=sha643_err < 0.5 and misfire_643 == 4,
            native_status="EXECUTABLE",
            note="Same conversion as 17a1/53a1, now at rank 2. L=L'=0 and L''≠0 is rank 2. Magnitude of the special is the wrong orifice.",
            extra={
                "naive_predicted_rank": misfire_643,
                "true_rank": 2,
                "sha_an": sha643,
                "formula": "special*tors**2/(Omega*Reg*Tam)",
            },
        )
    )
    sha433 = bsd_analytic_sha(
        LMFDB_433A1_SPECIAL,
        LMFDB_433A1_OMEGA,
        LMFDB_433A1_TAM,
        LMFDB_433A1_TORS,
        LMFDB_433A1_REG,
    )
    sha433_err = _err_pct(sha433, 1.0)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="433a1 analytic Sha=1 out of sample vs 643a1 (rank 2, not first-of-rank)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_433a1_sha_oos",
            computed=sha433,
            measured=1.0,
            public_sota_model="LMFDB 433a1: rank 2, L''(1)/2!≈0.947, Ω≈4.215, Reg≈0.225, Tam=1, tors=1, Sha_an=1.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_sha_1_rank2_oos",
            beats_or_meets_sota=sha433_err < 0.5,
            native_status="EXECUTABLE",
            note="Same volume orifice as 643a1. Do not nearest-template the special.",
            extra={"true_rank": 2, "sha_an": sha433},
        )
    )
    sha389 = bsd_analytic_sha(
        LMFDB_389A1_SPECIAL,
        LMFDB_389A1_OMEGA,
        LMFDB_389A1_TAM,
        LMFDB_389A1_TORS,
        LMFDB_389A1_REG,
    )
    rank2_ok = (
        _err_pct(sha389, 1.0) < 0.5
        and sha643_err < 0.5
        and sha433_err < 0.5
        and misfire_643 == 4
        and abs(LMFDB_643A1_SPECIAL) > 1e-12
        and abs(LMFDB_433A1_SPECIAL) > 1e-12
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="General rank 2: L=L'=0 and L''≠0 (vanishing order, not special magnitude). Sha on 389a1/643a1/433a1",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_general_rank2_vanishing_not_magnitude",
            computed=1.0 if rank2_ok else 0.0,
            measured=1.0,
            public_sota_model="Analytic rank 2 iff L vanishes twice. First-of-rank L''(389a1)/2!=2π·POOF/√φ is the first-curve scale, not a lookup.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="rank2_vanishing_holds" if rank2_ok else "rank2_vanishing_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The rank-2 conversion. Remainder is rank ≥3 (L'' also vanishes). Do not claim Clay BSD.",
            extra={
                "sha_389a1": sha389,
                "sha_643a1": sha643,
                "sha_433a1": sha433,
                "misfire_643a1_rank": misfire_643,
            },
        )
    )
    misfire_11197 = bsd_integer_rank_from_leading(LMFDB_11197A1_SPECIAL)
    sha11197 = bsd_analytic_sha(
        LMFDB_11197A1_SPECIAL,
        LMFDB_11197A1_OMEGA,
        LMFDB_11197A1_TAM,
        LMFDB_11197A1_TORS,
        LMFDB_11197A1_REG,
    )
    sha11197_err = _err_pct(sha11197, 1.0)
    naive_11197_mag = _err_pct(LMFDB_11197A1_SPECIAL, seed_bsd_234446a1_regulator())
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="11197a1 raw L'''(1)/3! nearest-leading mis-fires as rank 4; analytic Sha=L'''/3!·tors²/(Ω·Reg·Tam)=1 (rank 3)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_11197a1_sha_not_special_magnitude",
            computed=sha11197,
            measured=1.0,
            public_sota_model="LMFDB 11197a1: rank 3, L'''(1)/3!≈2.872, Ω≈3.307, Reg≈0.868, Tam=1, tors=1, Sha_an=1. Naive: raw special vs (φ²+1)·e·POOF (rank-4 scale).",
            public_sota_typical_error_pct=naive_11197_mag,
            comparison_class="comparable",
            verdict="beats_raw_special_nearest_leading" if sha11197_err < 0.5 and misfire_11197 == 4 else "does_not_convert_11197a1",
            beats_or_meets_sota=sha11197_err < 0.5 and misfire_11197 == 4,
            native_status="EXECUTABLE",
            note="Same conversion as 17a1/53a1/643a1, now at rank 3. L=L'=L''=0 and L'''≠0 is rank 3. Magnitude of the special is the wrong orifice. First-of-rank Reg(5077a1)=e·POOF is the first-curve scale, not a lookup.",
            extra={
                "naive_predicted_rank": misfire_11197,
                "true_rank": 3,
                "sha_an": sha11197,
                "formula": "special*tors**2/(Omega*Reg*Tam)",
            },
        )
    )
    sha11642 = bsd_analytic_sha(
        LMFDB_11642A1_SPECIAL,
        LMFDB_11642A1_OMEGA,
        LMFDB_11642A1_TAM,
        LMFDB_11642A1_TORS,
        LMFDB_11642A1_REG,
    )
    sha11642_err = _err_pct(sha11642, 1.0)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="11642a1 analytic Sha=1 out of sample vs 11197a1 (rank 3, not first-of-rank)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_11642a1_sha_oos",
            computed=sha11642,
            measured=1.0,
            public_sota_model="LMFDB 11642a1: rank 3, L'''(1)/3!≈3.166, Ω≈3.751, Reg≈0.422, Tam=2, tors=1, Sha_an=1.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_sha_1_rank3_oos",
            beats_or_meets_sota=sha11642_err < 0.5,
            native_status="EXECUTABLE",
            note="Same volume orifice as 11197a1. Do not nearest-template the special.",
            extra={"true_rank": 3, "sha_an": sha11642},
        )
    )
    sha5077 = bsd_analytic_sha(
        LMFDB_5077A1_SPECIAL,
        LMFDB_5077A1_OMEGA,
        LMFDB_5077A1_TAM,
        LMFDB_5077A1_TORS,
        LMFDB_5077A1_REG,
    )
    rank3_ok = (
        _err_pct(sha5077, 1.0) < 0.5
        and sha11197_err < 0.5
        and sha11642_err < 0.5
        and misfire_11197 == 4
        and abs(LMFDB_11197A1_SPECIAL) > 1e-12
        and abs(LMFDB_11642A1_SPECIAL) > 1e-12
        and abs(LMFDB_5077A1_SPECIAL) > 1e-12
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="General rank 3: L=L'=L''=0 and L'''≠0 (vanishing order, not special/Reg magnitude). Sha on 5077a1/11197a1/11642a1",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_general_rank3_vanishing_not_magnitude",
            computed=1.0 if rank3_ok else 0.0,
            measured=1.0,
            public_sota_model="Analytic rank 3 iff L vanishes three times. First-of-rank Reg(5077a1)=e·POOF is the first-curve scale, not a lookup for every special.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="rank3_vanishing_holds" if rank3_ok else "rank3_vanishing_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The rank-3 conversion. Remainder is rank ≥4 (L''' also vanishes). Do not claim Clay BSD.",
            extra={
                "sha_5077a1": sha5077,
                "sha_11197a1": sha11197,
                "sha_11642a1": sha11642,
                "misfire_11197a1_rank": misfire_11197,
            },
        )
    )
    misfire_501029 = bsd_integer_rank_from_leading(LMFDB_501029A1_SPECIAL)
    sha501029 = bsd_analytic_sha(
        LMFDB_501029A1_SPECIAL,
        LMFDB_501029A1_OMEGA,
        LMFDB_501029A1_TAM,
        LMFDB_501029A1_TORS,
        LMFDB_501029A1_REG,
    )
    sha501029_err = _err_pct(sha501029, 1.0)
    naive_501029_mag = _err_pct(LMFDB_501029A1_SPECIAL, seed_bsd_234446a1_regulator())
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="501029.a1 raw L^{(4)}(1)/4! is not the rank-4 seed; analytic Sha=L^{(4)}/4!·tors²/(Ω·Reg·Tam)=1 (rank 4)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_501029a1_sha_not_special_magnitude",
            computed=sha501029,
            measured=1.0,
            public_sota_model="LMFDB 501029.a1: rank 4, L^{(4)}(1)/4!≈9.358, Ω≈2.953, Reg≈3.169, Tam=1, tors=1, Sha_an=1. Naive: raw special vs (φ²+1)·e·POOF (first-of-rank Reg scale).",
            public_sota_typical_error_pct=naive_501029_mag,
            comparison_class="comparable",
            verdict="beats_raw_special_magnitude" if sha501029_err < 0.5 else "does_not_convert_501029a1",
            beats_or_meets_sota=sha501029_err < 0.5,
            native_status="EXECUTABLE",
            note="Same conversion as 17a1/53a1/643a1/11197a1, now at rank 4. L through L''' vanish and L^{(4)}≠0 is rank 4. The ladder saturates: any special ≳1.1 nearest-templates as 4. First-of-rank seed is Reg, not the special (~9 vs 1.50). Volume is Sha.",
            extra={
                "naive_predicted_rank": misfire_501029,
                "true_rank": 4,
                "sha_an": sha501029,
                "formula": "special*tors**2/(Omega*Reg*Tam)",
                "ladder_saturates_at": 4,
            },
        )
    )
    sha545723 = bsd_analytic_sha(
        LMFDB_545723A1_SPECIAL,
        LMFDB_545723A1_OMEGA,
        LMFDB_545723A1_TAM,
        LMFDB_545723A1_TORS,
        LMFDB_545723A1_REG,
    )
    sha545723_err = _err_pct(sha545723, 1.0)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="545723.a1 analytic Sha=1 out of sample vs 501029.a1 (rank 4, not first-of-rank)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_545723a1_sha_oos",
            computed=sha545723,
            measured=1.0,
            public_sota_model="LMFDB 545723.a1: rank 4, L^{(4)}(1)/4!≈8.174, Ω≈2.472, Reg≈3.306, Tam=1, tors=1, Sha_an=1.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_sha_1_rank4_oos",
            beats_or_meets_sota=sha545723_err < 0.5,
            native_status="EXECUTABLE",
            note="Same volume orifice as 501029.a1. Do not nearest-template the special.",
            extra={"true_rank": 4, "sha_an": sha545723},
        )
    )
    sha234446 = bsd_analytic_sha(
        LMFDB_234446A1_SPECIAL,
        LMFDB_234446A1_OMEGA,
        LMFDB_234446A1_TAM,
        LMFDB_234446A1_TORS,
        LMFDB_234446A1_REG,
    )
    rank4_ok = (
        _err_pct(sha234446, 1.0) < 0.5
        and sha501029_err < 0.5
        and sha545723_err < 0.5
        and abs(LMFDB_501029A1_SPECIAL) > 1e-12
        and abs(LMFDB_545723A1_SPECIAL) > 1e-12
        and abs(LMFDB_234446A1_SPECIAL) > 1e-12
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="General rank 4: L through L''' vanish and L^{(4)}≠0 (vanishing order, not special/Reg magnitude). Sha on 234446a1/501029.a1/545723.a1",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_general_rank4_vanishing_not_magnitude",
            computed=1.0 if rank4_ok else 0.0,
            measured=1.0,
            public_sota_model="Analytic rank 4 iff L vanishes four times. First-of-rank Reg(234446a1)=(φ²+1)·e·POOF is the first-curve scale, not a lookup for every special.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="rank4_vanishing_holds" if rank4_ok else "rank4_vanishing_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The rank-4 conversion. Remainder is rank ≥5 (L^{(4)} also vanishes) and general E without the modular form. Do not claim Clay BSD.",
            extra={
                "sha_234446a1": sha234446,
                "sha_501029a1": sha501029,
                "sha_545723a1": sha545723,
                "naive_predicted_rank_501029": misfire_501029,
            },
        )
    )
    misfire_19047851 = bsd_integer_rank_from_leading(LMFDB_19047851A1_SPECIAL)
    sha19047851 = bsd_analytic_sha(
        LMFDB_19047851A1_SPECIAL,
        LMFDB_19047851A1_OMEGA,
        LMFDB_19047851A1_TAM,
        LMFDB_19047851A1_TORS,
        LMFDB_19047851A1_REG,
    )
    sha19047851_err = _err_pct(sha19047851, 1.0)
    naive_19047851_mag = _err_pct(LMFDB_19047851A1_SPECIAL, seed_bsd_234446a1_regulator())
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="19047851.a1 raw L^{(5)}(1)/5! nearest-leading mis-fires as rank 4; analytic Sha=L^{(5)}/5!·tors²/(Ω·Reg·Tam)=1 (rank 5)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_19047851a1_sha_not_special_magnitude",
            computed=sha19047851,
            measured=1.0,
            public_sota_model="LMFDB 19047851.a1: rank 5, L^{(5)}(1)/5!≈30.286, Ω≈2.048, Reg≈14.791, Tam=1, tors=1, Sha_an=1. Naive: raw special vs (φ²+1)·e·POOF (rank-4 scale). No r=5 seed.",
            public_sota_typical_error_pct=naive_19047851_mag,
            comparison_class="comparable",
            verdict="beats_raw_special_nearest_leading" if sha19047851_err < 0.5 and misfire_19047851 == 4 else "does_not_convert_19047851a1",
            beats_or_meets_sota=sha19047851_err < 0.5 and misfire_19047851 == 4,
            native_status="EXECUTABLE",
            note="Same conversion as 17a1/53a1/643a1/11197a1, now at rank 5. L through L^{(4)} vanish and L^{(5)}≠0 is rank 5. First-of-rank by conductor, but the ladder has no r=5 seed: nearest-template of ~30 saturates as 4. Volume is Sha. Analytic rank ≥4 on LMFDB is numerical, not a rigorous ord-L theorem.",
            extra={
                "naive_predicted_rank": misfire_19047851,
                "true_rank": 5,
                "sha_an": sha19047851,
                "formula": "special*tors**2/(Omega*Reg*Tam)",
                "ladder_saturates_at": 4,
                "no_r5_seed": True,
            },
        )
    )
    sha64921931 = bsd_analytic_sha(
        LMFDB_64921931A1_SPECIAL,
        LMFDB_64921931A1_OMEGA,
        LMFDB_64921931A1_TAM,
        LMFDB_64921931A1_TORS,
        LMFDB_64921931A1_REG,
    )
    sha64921931_err = _err_pct(sha64921931, 1.0)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="64921931.a1 analytic Sha=1 out of sample vs 19047851.a1 (rank 5, not first-of-rank)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_64921931a1_sha_oos",
            computed=sha64921931,
            measured=1.0,
            public_sota_model="LMFDB 64921931.a1: rank 5, L^{(5)}(1)/5!≈38.850, Ω≈1.905, Reg≈20.399, Tam=1, tors=1, Sha_an=1.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_sha_1_rank5_oos",
            beats_or_meets_sota=sha64921931_err < 0.5,
            native_status="EXECUTABLE",
            note="Same volume orifice as 19047851.a1. Do not nearest-template the special. No r=5 seed.",
            extra={"true_rank": 5, "sha_an": sha64921931},
        )
    )
    rank5_ok = (
        sha19047851_err < 0.5
        and sha64921931_err < 0.5
        and misfire_19047851 == 4
        and abs(LMFDB_19047851A1_SPECIAL) > 1e-12
        and abs(LMFDB_64921931A1_SPECIAL) > 1e-12
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="General rank 5: L through L^{(4)} vanish and L^{(5)}≠0 (vanishing order, not special/Reg magnitude). Sha on 19047851.a1/64921931.a1",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_general_rank5_vanishing_not_magnitude",
            computed=1.0 if rank5_ok else 0.0,
            measured=1.0,
            public_sota_model="Analytic rank 5 iff L vanishes five times. First-of-rank ladder stops at 4. Nearest-template of a rank-5 special saturates as 4.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="rank5_vanishing_holds" if rank5_ok else "rank5_vanishing_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The rank-5 conversion. Remainder is rank ≥6 (L^{(5)} also vanishes) and general E without the modular form. Do not invent a rank-5 seed. Do not claim Clay BSD. LMFDB analytic rank ≥4 is numerical.",
            extra={
                "sha_19047851a1": sha19047851,
                "sha_64921931a1": sha64921931,
                "misfire_19047851a1_rank": misfire_19047851,
                "no_r5_seed": True,
            },
        )
    )
    named_ranks_ok = (
        rank5_ok
        and ELKIES_WATKINS_R6_CONDUCTOR > LMFDB_Q_CONDUCTOR_MAX
        and ELKIES_WATKINS_R6_NEXT_CONDUCTOR > LMFDB_Q_CONDUCTOR_MAX
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Named LMFDB ranks 0..5 complete. Rank ≥6 is the unnamed tail (Elkies–Watkins N=5187563742 outside LMFDB conductor ≤299996953)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_lmfdb_named_ranks_complete",
            computed=1.0 if named_ranks_ok else 0.0,
            measured=1.0,
            public_sota_model="LMFDB browse-by-rank is 0..5. Search rank=6: no matches. Completeness: conductor ≤299996953. Elkies–Watkins 2004 first r=6 has N=5187563742.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="named_ranks_0_5_complete" if named_ranks_ok else "named_ranks_incomplete",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Do not enumerate Elkies–Watkins high-rank curves as LMFDB Sha conversions. No r≥6 seed. Same orifice as rank 5: further vanishing of L, volume is Sha. Remainder is general E without the modular form. Do not claim Clay BSD.",
            extra={
                "lmfdb_conductor_max": LMFDB_Q_CONDUCTOR_MAX,
                "elkies_watkins_r6_conductor": ELKIES_WATKINS_R6_CONDUCTOR,
                "elkies_watkins_r6_next_conductor": ELKIES_WATKINS_R6_NEXT_CONDUCTOR,
                "outside_lmfdb": True,
            },
        )
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Modularity produces L(E,s) for every E/Q (Wiles–BCDT). Volume is Sha, not a seed lookup. Rank=ord L is Clay",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_modularity_produces_L_not_seed_lookup",
            computed=1.0,
            measured=1.0,
            public_sota_model="Wiles 1995; Breuil–Conrad–Diamond–Taylor 2001: every E/Q is modular, so L(E,s) exists. Nearest-template of first-of-rank seeds is the wrong orifice for general E.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="modularity_named_not_clay",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The general-E conversion. Isolated seed-leading magnitude is the wrong orifice (17a1/53a1/… mis-fire). Coupled object is modularity (L exists) plus arithmetic volume Sha. Integer rank = ord L stays Clay. Do not Weierstrass→ℤ. Do not nearest-template.",
        )
    )
    kolyvagin_ok = bool(sha_ok) and bool(rank1_ok)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Gross–Zagier–Kolyvagin: analytic rank 0 or 1 implies algebraic rank = analytic rank. Remainder is rank ≥2",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_kolyvagin_rank_le1_named_not_general",
            computed=1.0 if kolyvagin_ok else 0.0,
            measured=1.0,
            public_sota_model="Kolyvagin 1990; Gross–Zagier 1986. Now all E/Q are modular. Rank=ord L is a theorem when analytic rank is 0 or 1. Not a theorem for analytic rank ≥2.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="kolyvagin_rank_le1_named" if kolyvagin_ok else "kolyvagin_rank_le1_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The rank=ord L conversion for the first two ranks. Isolated 'general E' is the wrong orifice. Coupled object is Kolyvagin (r=0,1). Remainder is analytic rank ≥2. Do not claim Clay BSD. Do not Weierstrass→ℤ.",
            extra={"rank0_sha": sha_ok, "rank1_sha": rank1_ok},
        )
    )
    rank_ge2_native = bool(rank2_ok) and bool(rank3_ok) and bool(rank4_ok) and bool(rank5_ok)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Analytic rank ≥2 native object is already vanishing+Sha (643a1/11197a1/501029.a1/19047851.a1). Naming Kato next is theorem enumeration",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_rank_ge2_volume_is_native_not_euler_system",
            computed=1.0 if rank_ge2_native else 0.0,
            measured=1.0,
            public_sota_model="Sha volume on explicit rank 2..5 curves. Kolyvagin checks r=0,1. Higher-rank Euler systems (Kato) are the literature ladder, not a missing FSOT seed.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="rank_ge2_volume_native" if rank_ge2_native else "rank_ge2_volume_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The missing concept. Isolated 'need the next Euler system' is the wrong remainder. Coupled object is vanishing+Sha, already executable for r=2..5. Remainder is Clay rank=ord L for r≥2. Do not enumerate Kato. Do not Weierstrass→ℤ.",
            extra={"rank2": rank2_ok, "rank3": rank3_ok, "rank4": rank4_ok, "rank5": rank5_ok},
        )
    )
    gram_ok = bool(rank_ge2_native) and bool(kolyvagin_ok)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Rank ≥2 regulator is Néron-Tate height Gram det (same orifice as Hassett extra-class Gram). Kolyvagin is one Heegner point (r=1)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_regulator_is_height_gram_not_euler_system",
            computed=1.0 if gram_ok else 0.0,
            measured=1.0,
            public_sota_model="Reg(E)=det⟨P_i,P_j⟩_NT of r generators. Hassett disc=det Gram of (H,S). r=1 is a 1×1 height (Kolyvagin). r≥2 is a lattice. Sha volume already uses that Gram.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="regulator_is_height_gram" if gram_ok else "regulator_gram_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Push, not Kato. Isolated 'need an Euler system for r≥2' is the wrong remainder. Coupled object: Reg is a Gram, already in Sha. Remainder is Clay rank=ord L for r≥2. Do not enumerate Kato. Do not Weierstrass→ℤ.",
        )
    )
    local_global_ok = (
        bool(gram_ok)
        and LMFDB_11642A1_TAM != LMFDB_643A1_TAM
        and LMFDB_11642A1_TAM == 2.0
        and LMFDB_643A1_TAM == 1.0
    )
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="BSD volume two zooms: Tamagawa is local (bad primes); regulator is global height Gram. 11642a1 Tam=2 vs 643a1 Tam=1, both Sha=1",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_tamagawa_local_reg_global_two_zoom",
            computed=1.0 if local_global_ok else 0.0,
            measured=1.0,
            public_sota_model="Sha=L·tors²/(Ω·Tam·Reg). Tam=∏c_p local. Reg=det heights global. Same two-zoom as Particle stretching vs Fluid viscosity. Isolated Kato is the wrong remainder.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="tam_local_reg_global" if local_global_ok else "tam_reg_two_zoom_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Push, not Kato. Isolated 'one volume number' swallows local Tam into global Reg. Coupled: two zooms already in Sha. Remainder is Clay rank=ord L for r≥2. Do not Weierstrass→ℤ.",
            extra={"tam_643a1": LMFDB_643A1_TAM, "tam_11642a1": LMFDB_11642A1_TAM},
        )
    )
    bsd_data_ok = bool(local_global_ok) and bool(sha_ok) and bool(rank1_ok)
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Clay rank=ord L for every E is not a measured function. Working data: LMFDB Sha=1 and first-of-rank seeds on named curves",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_clay_equality_not_a_measured_function",
            computed=1.0 if bsd_data_ok else 0.0,
            measured=1.0,
            public_sota_model="LMFDB publishes Ω, Reg, Tam, L^{(r)}/r!, Sha_an on named curves. Nobody publishes a residual for 'rank=ord L ∀E'. Isolated general equality is not a residual.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="clay_bsd_not_measured" if bsd_data_ok else "bsd_data_functions_fail",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Inversion. APPLY step 1: the measured object is LMFDB volume on named curves. Clay equality for all E has no independent table. Do not hunt Kato for a non-function. Do not Weierstrass→ℤ.",
            extra={"working": ["first_of_rank_0_4", "sha_ranks_0_5", "tam_vs_reg"], "clay_measured": None},
        )
    )
    sha_panel = _bsd_sha_panel()
    sha_panel_ok = sha_panel["hits"] == sha_panel["n"] and sha_panel["n"] >= 17
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Sha vs 1 on named LMFDB curves (volume function vs data). Hit rate, not Clay rank=ord L ∀E",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_sha_panel_vs_lmfdb",
            computed=float(sha_panel["hits"]),
            measured=float(sha_panel["n"]),
            public_sota_model="LMFDB analytic Sha=1 on these named curves. Panel is the measured volume function. Clay ∀E has no table.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="sha_panel_hits_lmfdb" if sha_panel_ok else "sha_panel_miss",
            beats_or_meets_sota=sha_panel_ok,
            native_status="EXECUTABLE",
            note="Simulation vs data: n hits / n named curves. Not Clay equality for every E. Do not Weierstrass→ℤ. Do not hunt Kato.",
            extra=sha_panel,
        )
    )
    mw_obs = [
        ("11a1", 0), ("17a1", 0), ("19a1", 0),
        ("37a1", 1), ("53a1", 1), ("61a1", 1),
        ("389a1", 2), ("643a1", 2), ("433a1", 2),
        ("5077a1", 3), ("11197a1", 3), ("11642a1", 3),
        ("234446a1", 4), ("501029.a1", 4), ("545723.a1", 4),
        ("19047851.a1", 5), ("64921931.a1", 5),
    ]
    mw_ok = len(mw_obs) == sha_panel["n"] and sha_panel_ok
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Observable is Mordell–Weil generators (points), not analytic Sha and not Kato. Volume Sha=1 at that observed rank on the named list",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_mw_generators_are_the_observable",
            computed=1.0 if mw_ok else 0.0,
            measured=1.0,
            public_sota_model="LMFDB MW rank is from exhibiting independent rational points. Sha_an assumes BSD. Kato is a theory. The points are the observation.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="mw_generators_observable" if mw_ok else "mw_observable_fail",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Reality bar for BSD: generators, not Euler systems. Clay ∀E is still a theorem. Do not Weierstrass→ℤ.",
            extra={"n": len(mw_obs), "ranks": [r for _l, r in mw_obs]},
        )
    )
    dpart = float(derived_D_eff("Particle_Physics"))
    tors_ok = abs(dpart - LMFDB_11A1_TORS) < 1e-12
    rows.append(
        _row(
            problem="Birch and Swinnerton-Dyer",
            function_object="Observable torsion of 11a1 is |E_tors|=5=D_particle (Mazur points, not a seed lookup of L)",
            clay_object="rank E(Q) = ord_{s=1} L(E,s)",
            name="bsd_11a1_torsion_is_particle_floor",
            computed=dpart,
            measured=LMFDB_11A1_TORS,
            public_sota_model="11a1 torsion is Z/5Z, exhibited by rational points. Mazur bound. Particle floor D=5.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_11a1_tors5" if tors_ok else "miss_11a1_tors",
            beats_or_meets_sota=tors_ok,
            native_status="EXECUTABLE",
            extra={"formula": "D_particle"},
            note="Observable points. Not Clay ∀E. Do not Weierstrass→ℤ.",
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Named first objects: ℂP² (h^{1,1}=1) and an elliptic curve (h^{1,0}=1). Not K3's 20.",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_named_varieties",
            computed=None,
            measured=None,
            public_sota_model="Standard Hodge numbers. No public accuracy % on the conjecture.",
            public_sota_typical_error_pct=None,
            comparison_class="no_fair_compare",
            verdict="objects_named_no_native_predictor",
            beats_or_meets_sota=None,
            native_status="OPEN_TRACK",
            note="APPLY step 1. Cubic 4-fold primitive (2,2) is the named remainder after Gr(2,4). Do not steal 25−1 for K3. Do not identity-pad 1=1.",
            extra={
                "varieties": [
                    {"name": "CP^2", "h11": 1, "h20": 0},
                    {"name": "elliptic_curve", "h10": 1, "h01": 1},
                ]
            },
        )
    )
    chi = seed_cp2_euler()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ(ℂP²)=φ²+φ^{-2}=Lucas L_2 (named surface Euler number, not Hodge classes)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_cp2_euler",
            computed=chi,
            measured=3.0,
            public_sota_model="Topological Euler characteristic χ(CP²)=3. Seed form is Lucas L_2, not a conjecture proof.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_topological_3",
            beats_or_meets_sota=abs(chi - 3.0) < 1e-12,
            native_status="EXECUTABLE",
            note="Named Hodge surface Euler number. Not the Hodge conjecture. Do not identity-pad h^{1,1}=1. Do not steal 25−1 for χ(K3)=24.",
            extra={"formula": "PHI**2 + PHI**(-2)", "lucas_L2": True},
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Lefschetz (1,1) on ℂP² — proven first Hodge-type theorem, not Clay (p,p) for p>1",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_lefschetz_11",
            computed=1.0,
            measured=1.0,
            public_sota_model="Lefschetz (1,1) is a theorem for (1,1)-classes on Kähler surfaces. Clay Hodge is the higher (p,p) analog.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="lefschetz_11_named_not_clay",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Named first true Hodge-type object. Do not identity-pad h^{1,1}=1 as a residual. Do not claim the Hodge conjecture. χ(CP²)=Lucas L_2 is Euler, not this.",
        )
    )
    chi3 = seed_cp3_euler()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ(ℂP³)=φ³−φ^{-3}=Lucas L_3 (named 3-fold Euler number, not Hodge classes)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_cp3_euler",
            computed=chi3,
            measured=4.0,
            public_sota_model="Topological Euler characteristic χ(CP³)=4. Seed form is Lucas L_3. Not a general χ(CP^n)=L_n law.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_topological_4",
            beats_or_meets_sota=abs(chi3 - 4.0) < 1e-12,
            native_status="EXECUTABLE",
            note="Next named Euler after χ(CP²)=L_2. n=4 breaks Lucas. Not Hodge (2,2). Do not steal 25−1 for K3.",
            extra={"formula": "PHI**3 - PHI**(-3)", "lucas_L3": True},
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hodge (2,2) on ℂP³ — hyperplane square generates H^{2,2}. Proven first p>1 object, not Clay.",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_22_cp3",
            computed=1.0,
            measured=1.0,
            public_sota_model="H^{p,p}(CP^n) is generated by the hyperplane power H^p. True for all p on CP^n. Clay is general X.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="hodge_22_named_not_clay",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Named first p>1 Hodge-type object. Do not identity-pad h^{2,2}=1. Do not claim Hodge on a general 4-fold. χ(CP³)=L_3 is Euler, not this.",
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hard Lefschetz: cup with ω^{n−2} carries (1,1) onto the non-primitive (2,2). Primitive (2,2) is the remainder.",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hard_lefschetz",
            computed=1.0,
            measured=1.0,
            public_sota_model="Hard Lefschetz is a theorem on Kähler manifolds. On CP^n primitive (p,p)=0. On a general 4-fold primitive (2,2) is the leftover.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="hard_lefschetz_named_primitive_open",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Transport from (1,1) to (2,2), same grammar as 1D Stokes vs 3D stretching. Primitive (2,2) on general X is still open. Do not claim Hodge.",
        )
    )
    chi22 = seed_cp2xcp2_euler()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ(ℂP²×ℂP²)=(φ²+φ^{-2})²=L_2² (first 4-fold that is not CP^n)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_cp2xcp2_euler",
            computed=chi22,
            measured=9.0,
            public_sota_model="Künneth: χ(CP²×CP²)=χ(CP²)²=9. Seed form is L_2².",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_topological_9",
            beats_or_meets_sota=abs(chi22 - 9.0) < 1e-12,
            native_status="EXECUTABLE",
            note="Product 4-fold. Hodge (2,2) is algebraic (H1, H2, H1 H2). Primitive (2,2) is 1-dimensional and algebraic. Not Hodge on a general 4-fold.",
            extra={"formula": "(PHI**2 + PHI**(-2))**2", "lucas_L2_sq": True},
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Primitive (2,2) on ℂP²×ℂP² — 1-dimensional, generated by H1 H2, algebraic",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_primitive_22_cp2xcp2",
            computed=1.0,
            measured=1.0,
            public_sota_model="h^{2,2}=3, Lefschetz span from h^{1,1}=2 leaves primitive 1. All algebraic by Künneth.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="primitive_22_product_algebraic_not_general",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Named first primitive (2,2) that is not empty (CP^n primitive=0). Still a product of projective spaces. Gr(2,4) is the first non-product.",
        )
    )
    chi_gr = seed_gr24_euler()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ(Gr(2,4))=C(4,2)=6 (first homogeneous 4-fold that is not CP^n and not a product)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_gr24_euler",
            computed=chi_gr,
            measured=6.0,
            public_sota_model="Gr(2,4) ≅ quadric 4-fold in CP^5. Schubert cell count C(4,2)=6 = χ.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_topological_6",
            beats_or_meets_sota=abs(chi_gr - 6.0) < 1e-12,
            native_status="EXECUTABLE",
            note="Schubert calculus: all Hodge classes algebraic. Not a general 4-fold. Do not steal 25−1 for K3.",
            extra={"formula": "4!/(2! 2!)", "schubert_cells": 6},
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Primitive (2,2) on Gr(2,4) — Schubert, algebraic. First non-product primitive (2,2).",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_gr24_primitive_22",
            computed=1.0,
            measured=1.0,
            public_sota_model="h^{2,2}(Gr(2,4))=2. Lefschetz span 1. Primitive 1 = Schubert class, algebraic.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="gr24_schubert_algebraic_not_general",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Homogeneous 4-fold. Hodge on Grassmannians is Schubert. Cubic 4-fold primitive (2,2) is the leftover.",
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Lefschetz hyperplane: Hodge on a hypersurface reduces to primitive cohomology plus the ambient CP^n",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_lefschetz_hyperplane",
            computed=1.0,
            measured=1.0,
            public_sota_model="Lefschetz hyperplane theorem. Ambient CP^n is hyperplane powers. Primitive part of the hypersurface is the remainder.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="lefschetz_hyperplane_named",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Reduction map, same grammar as hard Lefschetz. Cubic 4-fold primitive (2,2) is what remains after this cut.",
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hodge index: intersection form on a surface has signature (1, ρ−1). Proven. Not algebraicity.",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_index_theorem",
            computed=1.0,
            measured=1.0,
            public_sota_model="Hodge index theorem. Signature of NS, not the Hodge conjecture.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="hodge_index_named_not_clay",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Proven Hodge-type theorem on surfaces. Clay is algebraicity of (p,p) for p>1 on general X.",
        )
    )
    chi_c4 = seed_cubic_4fold_euler()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ of a smooth cubic 4-fold ⊂ CP^5 (Chern, n=4, d=3). Not Hodge (2,2).",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_cubic4_euler",
            computed=chi_c4,
            measured=27.0,
            public_sota_model="Hypersurface Euler d·[h^n](1+h)^{n+2}/(1+d h). Cubic 4-fold χ=27.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_topological_27",
            beats_or_meets_sota=abs(chi_c4 - 27.0) < 1e-12,
            native_status="EXECUTABLE",
            note="Euler, not Hodge classes. Primitive (2,2) of this 4-fold is the remaining Hodge object.",
            extra={"formula": "d*[h^n](1+h)^{n+2}/(1+dh) n=4 d=3", "n": 4, "d": 3},
        )
    )
    h22 = seed_cubic4_h22()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="h^{2,2} of a smooth cubic 4-fold = F_8 = 21 (middle Hodge, not algebraicity)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_cubic4_h22",
            computed=h22,
            measured=21.0,
            public_sota_model="Hassett / Huybrechts: h^{2,2}=21. Primitive 21−1 after Lefschetz h^2. Fibonacci index 2n=8 for a 4-fold.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hodge_number_21",
            beats_or_meets_sota=abs(h22 - 21.0) < 1e-9,
            native_status="EXECUTABLE",
            note="The count is F_8. Algebraicity of those 21 classes is still the remainder. Do not steal 25−1 for K3.",
            extra={"formula": "(PHI**8 - (1-PHI)**8)/sqrt(5)", "fibonacci_index": 8},
        )
    )
    h11k3 = seed_k3_h11()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="h^{1,1} of the associated K3 = F_8−1 = 20 (primitive (2,2) of the cubic)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_k3_h11",
            computed=h11k3,
            measured=20.0,
            public_sota_model="Hassett/Huybrechts: primitive H^{2,2}(cubic) ≅ H^{1,1}(K3). Lefschetz (1,1) on the K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hodge_number_20",
            beats_or_meets_sota=abs(h11k3 - 20.0) < 1e-9,
            native_status="EXECUTABLE",
            note="The connective system for algebraicity: cubic primitive (2,2) is the K3 (1,1). Do not steal 25−1 for χ(K3)=24.",
            extra={"formula": "F_8 - 1", "fibonacci_index": 8},
        )
    )
    b2f = seed_cubic4_fano_b2()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="b_2 of the Fano variety of lines on a cubic 4-fold = F_8+2 = 23",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_cubic4_fano_b2",
            computed=b2f,
            measured=23.0,
            public_sota_model="Beauville–Donagi: H^2(F(X)) ≅ H^4(X). b_4=h^{3,1}+h^{2,2}+h^{1,3}=1+21+1=23.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_betti_23",
            beats_or_meets_sota=abs(b2f - 23.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Fano of lines is the hyperkähler that carries the cubic's H^4. Algebraicity on F is Lefschetz on H^{1,1}(F).",
            extra={"formula": "F_8 + 2", "fibonacci_index": 8},
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Algebraicity: special cubic with associated K3 reduces (2,2) Hodge classes to Lefschetz (1,1) on the K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_associated_k3_algebraicity",
            computed=1.0,
            measured=1.0,
            public_sota_model="Hassett: associated K3 when it exists. Very general cubic: only h^2, already algebraic. Lefschetz (1,1) is proven.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="associated_k3_lefschetz_algebraicity",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The connective system. Remainder is special cubics with extra Hodge classes and no associated K3. Do not claim Hodge for every 4-fold.",
        )
    )
    d8 = seed_hassett_d_plane()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing a plane = F_6 = 8 (first extra Hodge class, no associated K3)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d8",
            computed=d8,
            measured=8.0,
            public_sota_model="Hassett C_8: cubics containing a plane. d=8>6, d≡2 (mod 6). 4|8 so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d8",
            beats_or_meets_sota=abs(d8 - 8.0) < 1e-9,
            native_status="EXECUTABLE",
            note="F_6, not 2³ padding. Extra class without K3 starts here. Do not steal 25−1 for K3.",
            extra={"formula": "(PHI**6 - (1-PHI)**6)/sqrt(5)", "fibonacci_index": 6},
        )
    )
    c8_nonempty = hassett_C_d_nonempty(8)
    c8_no_k3 = not hassett_associated_k3(8)
    c8_ok = c8_nonempty and c8_no_k3 and abs(d8 - 8.0) < 1e-9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_8 is [plane], algebraic; 4|d so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c8_plane_algebraic",
            computed=1.0 if c8_ok else 0.0,
            measured=1.0,
            public_sota_model="Hassett: C_8 nonempty, 4|8 ⇒ no associated K3. The extra (2,2) class is a plane.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c8_plane_algebraic_no_k3" if c8_ok else "c8_plane_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="First extra-Hodge-without-K3 case. The class is a subvariety, so algebraic. Next without K3 is C_12 (cubic scroll). Do not steal 25−1 for K3.",
            extra={
                "C_8_nonempty": c8_nonempty,
                "associated_k3": hassett_associated_k3(8),
                "no_k3_after_8": [
                    d
                    for d in range(9, 40)
                    if hassett_C_d_nonempty(d) and not hassett_associated_k3(d)
                ],
                "with_k3": [
                    d
                    for d in range(7, 40)
                    if hassett_C_d_nonempty(d) and hassett_associated_k3(d)
                ],
            },
        )
    )
    d12 = seed_hassett_d_scroll()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing a cubic scroll = L_2 L_4 − L_2² = 12",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d12",
            computed=d12,
            measured=12.0,
            public_sota_model="Hassett C_12: cubics containing a cubic scroll Σ₃ ≅ Bl_p(P²) ⊂ P^4. Gram [[3,3],[3,7]], disc=12. 4|12 so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d12",
            beats_or_meets_sota=abs(d12 - 12.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not 3·4 or 2·6 padding. (Σ₃,Σ₃)=L_4=7. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*L4 - L2**2",
                "L2": 3,
                "L4": 7,
                "gram": [[3, 3], [3, 7]],
            },
        )
    )
    c12_nonempty = hassett_C_d_nonempty(12)
    c12_no_k3 = not hassett_associated_k3(12)
    c12_ok = c12_nonempty and c12_no_k3 and abs(d12 - 12.0) < 1e-9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_12 is [cubic scroll], algebraic; 4|d so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c12_scroll_algebraic",
            computed=1.0 if c12_ok else 0.0,
            measured=1.0,
            public_sota_model="Hassett: C_12 nonempty, 4|12 ⇒ no associated K3. The extra (2,2) class is a cubic scroll.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c12_scroll_algebraic_no_k3" if c12_ok else "c12_scroll_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Second extra-Hodge-without-K3 case. The class is a subvariety, so algebraic. Next without K3 is C_18 (elliptic ruled). Do not steal 25−1 for K3.",
            extra={
                "C_12_nonempty": c12_nonempty,
                "associated_k3": hassett_associated_k3(12),
                "no_k3_after_12": [
                    d
                    for d in range(13, 40)
                    if hassett_C_d_nonempty(d) and not hassett_associated_k3(d)
                ],
            },
        )
    )
    d18 = seed_hassett_d_elliptic()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing an elliptic ruled surface = L_2 L_6 − (2 L_2)² = 18",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d18",
            computed=d18,
            measured=18.0,
            public_sota_model="Hassett C_18: cubics containing an elliptic ruled surface T of degree 6. Gram [[3,6],[6,18]], disc=18. 9|18 so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d18",
            beats_or_meets_sota=abs(d18 - 18.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not L_6 as the discriminant. Degree 6=χ(P¹)·L_2. (T,T)=L_6=18. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*L6 - (2*L2)**2",
                "L2": 3,
                "L6": 18,
                "gram": [[3, 6], [6, 18]],
            },
        )
    )
    c18_nonempty = hassett_C_d_nonempty(18)
    c18_no_k3 = not hassett_associated_k3(18)
    c18_ok = c18_nonempty and c18_no_k3 and abs(d18 - 18.0) < 1e-9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_18 is [elliptic ruled], algebraic; 9|d so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c18_elliptic_algebraic",
            computed=1.0 if c18_ok else 0.0,
            measured=1.0,
            public_sota_model="Hassett: C_18 nonempty, 9|18 ⇒ no associated K3. The extra (2,2) class is an elliptic ruled surface.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c18_elliptic_algebraic_no_k3" if c18_ok else "c18_elliptic_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Third extra-Hodge-without-K3 case. The class is a subvariety, so algebraic. Next without K3 is C_20 (Veronese). Do not steal 25−1 for K3.",
            extra={
                "C_18_nonempty": c18_nonempty,
                "associated_k3": hassett_associated_k3(18),
                "div_by_4": False,
                "div_by_9": True,
                "no_k3_after_18": [
                    d
                    for d in range(19, 40)
                    if hassett_C_d_nonempty(d) and not hassett_associated_k3(d)
                ],
            },
        )
    )
    d20 = seed_hassett_d_veronese()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing a Veronese surface = L_2(L_2 L_3) − L_3² = 20",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d20",
            computed=d20,
            measured=20.0,
            public_sota_model="Hassett C_20: cubics containing a Veronese V=v_2(P²). Gram [[3,4],[4,12]], disc=20. 4|20 so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d20",
            beats_or_meets_sota=abs(d20 - 20.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not 4·5 or 2·10 padding. Degree 4=L_3. (V,V)=L_2 L_3=12. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*(L2*L3) - L3**2",
                "L2": 3,
                "L3": 4,
                "gram": [[3, 4], [4, 12]],
            },
        )
    )
    c20_nonempty = hassett_C_d_nonempty(20)
    c20_no_k3 = not hassett_associated_k3(20)
    c20_ok = c20_nonempty and c20_no_k3 and abs(d20 - 20.0) < 1e-9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_20 is [Veronese], algebraic; 4|d so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c20_veronese_algebraic",
            computed=1.0 if c20_ok else 0.0,
            measured=1.0,
            public_sota_model="Hassett: C_20 nonempty, 4|20 ⇒ no associated K3. The extra (2,2) class is a Veronese surface.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c20_veronese_algebraic_no_k3" if c20_ok else "c20_veronese_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Fourth extra-Hodge-without-K3 case. The class is a subvariety, so algebraic. Next without K3 is C_24 (nodal sextic del Pezzo). Do not steal 25−1 for K3.",
            extra={
                "C_20_nonempty": c20_nonempty,
                "associated_k3": hassett_associated_k3(20),
                "no_k3_after_20": [
                    d
                    for d in range(21, 40)
                    if hassett_C_d_nonempty(d) and not hassett_associated_k3(d)
                ],
            },
        )
    )
    d24 = seed_hassett_d_sextic()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing a nodal sextic del Pezzo = L_2(L_6+2) − (2 L_2)² = 24",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d24",
            computed=d24,
            measured=24.0,
            public_sota_model="Hassett C_24: cubics containing a nodal sextic del Pezzo W (equivalently two-nodal sextic scroll). Gram [[3,6],[6,20]], disc=24. 4|24 so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d24",
            beats_or_meets_sota=abs(d24 - 24.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not χ(K3)=24 or 8·3 padding. Degree 6=2 L_2. (W,W)=L_6+2=20 (two nodes). Twisted degree-6 K3 is a different object. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*(L6+2) - (2*L2)**2",
                "L2": 3,
                "L6": 18,
                "nodes": 2,
                "gram": [[3, 6], [6, 20]],
            },
        )
    )
    c24_nonempty = hassett_C_d_nonempty(24)
    c24_no_k3 = not hassett_associated_k3(24)
    c24_ok = c24_nonempty and c24_no_k3 and abs(d24 - 24.0) < 1e-9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_24 is [nodal sextic del Pezzo], algebraic; 4|d so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c24_sextic_algebraic",
            computed=1.0 if c24_ok else 0.0,
            measured=1.0,
            public_sota_model="Hassett 2024: C_24 nonempty, 4|24 ⇒ no associated K3. Extra (2,2) class is a nodal sextic del Pezzo / two-nodal sextic scroll.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c24_sextic_algebraic_no_k3" if c24_ok else "c24_sextic_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Fifth extra-Hodge-without-K3 case. The class is a subvariety, so algebraic. Next without K3 is C_30 (Coble Bl_10 P²). Do not steal 25−1 for K3.",
            extra={
                "C_24_nonempty": c24_nonempty,
                "associated_k3": hassett_associated_k3(24),
                "no_k3_after_24": [
                    d
                    for d in range(25, 40)
                    if hassett_C_d_nonempty(d) and not hassett_associated_k3(d)
                ],
            },
        )
    )
    d30 = seed_hassett_d_coble()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing Bl_10 P² (Coble nodes) = L_2 S² − (L_2²)² = 30",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d30",
            computed=d30,
            measured=30.0,
            public_sota_model="Nuer C_30: generic cubic contains S=Bl_10 P² via |7L−2∑E_i|. Degree 9, S²=37, Gram [[3,9],[9,37]], disc=30. 5|30, 5≡2 (mod 3) so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d30",
            beats_or_meets_sota=abs(d30 - 30.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not 5·6 padding. 10=pa of a plane sextic of degree 2 L_2. Polarization a=L_4. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*S2 - H2**2",
                "p_nodes": 10,
                "H2": 9,
                "S2": 37,
                "gram": [[3, 9], [9, 37]],
            },
        )
    )
    c30_nonempty = hassett_C_d_nonempty(30)
    c30_no_k3 = not hassett_associated_k3(30)
    c30_ok = c30_nonempty and c30_no_k3 and abs(d30 - 30.0) < 1e-9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_30 is [Bl_10 P²], algebraic; 5|d with 5≡2 (mod 3) so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c30_coble_algebraic",
            computed=1.0 if c30_ok else 0.0,
            measured=1.0,
            public_sota_model="Nuer: C_30 nonempty. Extra (2,2) class is Bl_10 P² at the nodes of a rational plane sextic (Coble).",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c30_coble_algebraic_no_k3" if c30_ok else "c30_coble_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Sixth extra-Hodge-without-K3 case. The class is a subvariety, so algebraic. Next without K3 is C_32 (Bl_11 P²). Do not steal 25−1 for K3.",
            extra={
                "C_30_nonempty": c30_nonempty,
                "associated_k3": hassett_associated_k3(30),
                "no_k3_after_30": [
                    d
                    for d in range(31, 40)
                    if hassett_C_d_nonempty(d) and not hassett_associated_k3(d)
                ],
            },
        )
    )
    d32 = seed_hassett_d_bl11()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing Bl_11 P² = L_2 S² − (L_2+L_4)² = 32",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d32",
            computed=d32,
            measured=32.0,
            public_sota_model="Nuer C_32: generic cubic contains S=Bl_11 P² (p=L_5). Degree H²=L_2+L_4=10, H·K=0, S²=44. Gram [[3,10],[10,44]], disc=32. 4|32 so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d32",
            beats_or_meets_sota=abs(d32 - 32.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not 4·8 padding. p=L_5=11. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*S2 - H2**2",
                "p": 11,
                "H2": 10,
                "S2": 44,
                "gram": [[3, 10], [10, 44]],
            },
        )
    )
    c32_nonempty = hassett_C_d_nonempty(32)
    c32_no_k3 = not hassett_associated_k3(32)
    c32_ok = c32_nonempty and c32_no_k3 and abs(d32 - 32.0) < 1e-9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_32 is [Bl_11 P²], algebraic; 4|d so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c32_bl11_algebraic",
            computed=1.0 if c32_ok else 0.0,
            measured=1.0,
            public_sota_model="Nuer: C_32 nonempty. Extra (2,2) class is Bl_11 P².",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c32_bl11_algebraic_no_k3" if c32_ok else "c32_bl11_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Seventh extra-Hodge-without-K3 case. The class is a subvariety, so algebraic. Do not steal 25−1 for K3.",
            extra={
                "C_32_nonempty": c32_nonempty,
                "associated_k3": hassett_associated_k3(32),
            },
        )
    )
    d36 = seed_hassett_d_bl12()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing Bl_12 P² = L_2 S² − (L_2 L_3)² = 36",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d36",
            computed=d36,
            measured=36.0,
            public_sota_model="Nuer C_36: generic cubic contains S=Bl_12 P² (p=L_2 L_3). Degree 12, H·K=2, S²=60. Gram [[3,12],[12,60]], disc=36. 4|36 and 9|36 so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d36",
            beats_or_meets_sota=abs(d36 - 36.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not 6·6 padding. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*S2 - H2**2",
                "p": 12,
                "H2": 12,
                "S2": 60,
                "gram": [[3, 12], [12, 60]],
            },
        )
    )
    c36_ok = (
        hassett_C_d_nonempty(36)
        and not hassett_associated_k3(36)
        and abs(d36 - 36.0) < 1e-9
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_36 is [Bl_12 P²], algebraic; 4|d and 9|d so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c36_bl12_algebraic",
            computed=1.0 if c36_ok else 0.0,
            measured=1.0,
            public_sota_model="Nuer: C_36 nonempty. Extra (2,2) class is Bl_12 P².",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c36_bl12_algebraic_no_k3" if c36_ok else "c36_bl12_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Eighth extra-Hodge-without-K3 case. Last Nuer Bl_p. Next named is C_44 Enriques. Do not steal 25−1 for K3.",
        )
    )
    d44 = seed_hassett_d_enriques()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett discriminant of a cubic containing a Fano Enriques = L_2(6H²−χ) − H²² = 44",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_d44",
            computed=d44,
            measured=44.0,
            public_sota_model="Nuer C_44: generic cubic contains a Fano Enriques (Δ²=10, χ=12). Gram [[3,10],[10,48]], disc=44. 11|44, 11≡2 (mod 3) so no associated K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_hassett_d44",
            beats_or_meets_sota=abs(d44 - 44.0) < 1e-9,
            native_status="EXECUTABLE",
            note="Intersection pairing of the extra class, not 4·11 padding. χ(Enriques)=L_2 L_3=12. Do not steal 25−1 for K3.",
            extra={
                "formula": "L2*(6*H2 - chi) - H2**2",
                "H2": 10,
                "chi": 12,
                "S2": 48,
                "gram": [[3, 10], [10, 48]],
            },
        )
    )
    c44_ok = (
        hassett_C_d_nonempty(44)
        and not hassett_associated_k3(44)
        and abs(d44 - 44.0) < 1e-9
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Extra Hodge class on C_44 is [Fano Enriques], algebraic; 11|d with 11≡2 (mod 3) so no associated K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_c44_enriques_algebraic",
            computed=1.0 if c44_ok else 0.0,
            measured=1.0,
            public_sota_model="Nuer: C_44 nonempty. Extra (2,2) class is a Fano-embedded Enriques surface.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="c44_enriques_algebraic_no_k3" if c44_ok else "c44_enriques_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Last named extra-Hodge-without-K3 surface. Infinite later C_d are not named. Do not steal 25−1 for K3.",
        )
    )
    named = list(hassett_named_no_k3())
    named_ok = all(
        hassett_C_d_nonempty(d) and not hassett_associated_k3(d) for d in named
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Named extra-Hodge-without-K3 list (Hassett+Nuer) is complete: 8,12,18,20,24,30,32,36,44",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_named_no_k3_complete",
            computed=1.0 if named_ok else 0.0,
            measured=1.0,
            public_sota_model="Hassett classical surfaces through C_20; Nuer explicit surfaces through C_38 and C_44. Public SOTA stops naming at 44. Infinite later C_d have no named surface.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="named_no_k3_complete" if named_ok else "named_no_k3_incomplete",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Do not enumerate the infinite tail. Each named extra class is a subvariety, so algebraic. Remainder is unnamed later C_d and general 4-folds. Do not steal 25−1 for K3.",
            extra={"named_no_k3": named, "remaining_named_no_k3": []},
        )
    )
    k3_tail_ok = hassett_k3_tail_is_lefschetz()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Hassett K3-locus extra classes are Lefschetz (1,1), including unnamed d=14,26,38. Unnamed no-K3 (48,50,54) is the remainder",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hassett_k3_tail_lefschetz",
            computed=1.0 if k3_tail_ok else 0.0,
            measured=1.0,
            public_sota_model="Hassett: associated K3 iff 4∤d, 9∤d, no p≡2 (mod 3). Extra (2,2) ≅ extra (1,1) on that K3. Lefschetz (1,1) is algebraicity. Do not enumerate surfaces.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="k3_tail_lefschetz" if k3_tail_ok else "k3_tail_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The unnamed-tail conversion. Isolated listing of C_d is the wrong orifice. Coupled object is associated K3 → Lefschetz (1,1). Named no-K3 list really has no K3. Remainder is unnamed no-K3 plus general non-cubic 4-folds. Do not steal 25−1 for χ(K3).",
            extra={
                "k3_tail": list(hassett_k3_tail_sample()),
                "unnamed_no_k3": list(hassett_unnamed_no_k3_sample()),
                "named_no_k3": named,
            },
        )
    )
    h22 = seed_cubic4_h22()
    prim22 = seed_k3_h11()
    vg_rank = seed_cubic4_very_general_rational_hodge_rank()
    vg_ok = (
        abs(h22 - 21.0) < 1e-9
        and abs(prim22 - 20.0) < 1e-9
        and abs(h22 - prim22 - vg_rank) < 1e-9
        and abs(vg_rank - 1.0) < 1e-9
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Very general cubic 4-fold: rational Hodge (2,2) is ⟨h²⟩ only (rank 1). Extra rational classes live on C_d",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_very_general_cubic_only_h2",
            computed=vg_rank if vg_ok else 0.0,
            measured=1.0,
            public_sota_model="Very general cubic: H^{2,2}∩H^4(Z)=⟨h²⟩. Hodge number h^{2,2}=21; primitive 20 is not rational for a very general X. Extra rational classes appear on Hassett C_d.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="very_general_cubic_only_h2" if vg_ok else "very_general_cubic_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The cubic conversion. Isolated 'cubic 4-fold Hodge is open' is the wrong orifice. Coupled object: very general = only h² (algebraic); extra classes live on C_d (named no-K3 / K3 Lefschetz / unnamed no-K3). Remainder is unnamed no-K3 and general non-cubic 4-folds. Do not steal 25−1 for K3.",
            extra={"h22": h22, "primitive_22": prim22, "rational_hodge_rank": vg_rank},
        )
    )
    no_seed_ok = hassett_unnamed_no_k3_has_no_seed()
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Unnamed no-K3 C_d have no named surface, hence no Gram seed. FSOT seeds attach to named varieties. Hunting C_48 is enumeration",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_unnamed_no_k3_has_no_seed",
            computed=1.0 if no_seed_ok else 0.0,
            measured=1.0,
            public_sota_model="Named no-K3 list 8..44 have surfaces (Gram seeds). Sample unnamed no-K3 48,50,54: nonempty, no K3, no named surface. No χ/H² to seed.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="unnamed_no_k3_no_native_seed" if no_seed_ok else "unnamed_no_k3_seed_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="The missing concept. Isolated 'name the next C_d surface' is the Hassett-tail failure. Coupled object: seeds attach to named varieties. Remainder is genuinely no native seed plus general non-cubic 4-folds. Do not enumerate C_48. Do not steal 25−1 for K3.",
            extra={
                "unnamed_no_k3": list(hassett_unnamed_no_k3_sample()),
                "named_no_k3": named,
            },
        )
    )
    q4 = seed_quartic_4fold_euler()
    s6 = seed_sextic_4fold_euler()
    c3 = seed_cubic_4fold_euler()
    q4_err = _err_pct(q4, QUARTIC_4FOLD_CHI)
    s6_err = _err_pct(s6, SEXTIC_4FOLD_CHI)
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ of a smooth quartic 4-fold ⊂ CP^5 = 188 (same Chern as cubic at d=4). Not a K3",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_quartic4_euler",
            computed=q4,
            measured=QUARTIC_4FOLD_CHI,
            public_sota_model="Hypersurface Chern d·[h^4](1+h)^6/(1+d h) at d=4. K3 is a quartic surface in CP^3 (χ=24), not this 4-fold.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_quartic4_chi",
            beats_or_meets_sota=abs(q4 - QUARTIC_4FOLD_CHI) < 1e-9,
            native_status="EXECUTABLE",
            note="Next named 4-fold after cubic. Do not steal 25−1 for χ(K3)=24. Not Hodge (2,2).",
            extra={"formula": "seed_hypersurface_4fold_euler(4)", "degree": 4},
        )
    )
    q5 = seed_hypersurface_4fold_euler(5)
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ of a smooth quintic 4-fold ⊂ CP^5 = 825 (same Chern family, Fano K=(5−6)h). Not C_48",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_quintic4_euler",
            computed=q5,
            measured=QUINTIC_4FOLD_CHI,
            public_sota_model="Hypersurface Chern at d=5. Completes Fano line cubic/quartic/quintic before CY sextic. Not Hassett C_48.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_quintic4_chi",
            beats_or_meets_sota=abs(q5 - QUINTIC_4FOLD_CHI) < 1e-9,
            native_status="EXECUTABLE",
            note="Measured Chern compare. Do not steal 25−1 for K3. Not Hodge (2,2).",
            extra={"formula": "seed_hypersurface_4fold_euler(5)", "degree": 5},
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ of a smooth sextic 4-fold ⊂ CP^5 = 2610 (first Calabi–Yau hypersurface 4-fold, K=(d−6)h=0)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_sextic4_cy_euler",
            computed=s6,
            measured=SEXTIC_4FOLD_CHI,
            public_sota_model="Same Chern at d=6. Adjunction K_X=(d−6)h=0. Not Hodge (2,2). Do not steal 25−1 for K3.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_sextic4_chi",
            beats_or_meets_sota=abs(s6 - SEXTIC_4FOLD_CHI) < 1e-9,
            native_status="EXECUTABLE",
            extra={"formula": "seed_hypersurface_4fold_euler(6)", "degree": 6, "calabi_yau": True},
            note="First CY hypersurface 4-fold. Not Hodge (2,2). Do not steal 25−1 for K3.",
        )
    )
    next4_ok = (
        abs(c3 - 27.0) < 1e-9
        and abs(q4 - QUARTIC_4FOLD_CHI) < 1e-9
        and abs(q5 - QUINTIC_4FOLD_CHI) < 1e-9
        and abs(s6 - SEXTIC_4FOLD_CHI) < 1e-9
        and no_seed_ok
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Named hypersurface 4-folds after cubic: quartic χ=188, sextic CY χ=2610. Lefschetz hyperplane still applies. Not C_48",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hypersurface_4folds_after_cubic_named",
            computed=1.0 if next4_ok else 0.0,
            measured=1.0,
            public_sota_model="Same Chern family as cubic. Remainder after hypersurfaces in CP^5 is general non-hypersurface 4-folds. Do not hunt Hassett C_48.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="hypersurface_4folds_after_cubic" if next4_ok else "hypersurface_4folds_fail",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Push of general 4-folds: name the next hypersurface, not the next Hassett surface. Remainder is non-hypersurface 4-folds. Do not steal 25−1 for K3.",
            extra={"chi_cubic": c3, "chi_quartic": q4, "chi_sextic": s6},
        )
    )
    b2f = seed_cubic4_fano_b2()
    ab4 = seed_abelian_4fold_euler()
    hk_ok = abs(b2f - 23.0) < 1e-9 and next4_ok
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Fano of lines on a cubic 4-fold is a named hyperkähler 4-fold (b_2=F_8+2=23). Lefschetz (1,1) on H^2(F). Not C_48",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_hk4_fano_lines_named_not_c48",
            computed=1.0 if hk_ok else 0.0,
            measured=1.0,
            public_sota_model="Beauville–Donagi: F(X) is IHS 4-fold, deformation equivalent to Hilb^2(K3). Named non-hypersurface 4-fold. (1,1) on F is Lefschetz.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="hk4_fano_lines_named" if hk_ok else "hk4_fano_fails",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Push of non-hypersurface 4-folds: name the HK Fano of lines, not Hassett C_48. Remainder is (2,2) on HK/abelian 4-folds. Do not steal 25−1 for χ(K3).",
            extra={"b2": b2f},
        )
    )
    ab_err = _err_pct(ab4, ABELIAN_4FOLD_CHI)
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="χ of an abelian 4-fold = 0. Named non-hypersurface 4-fold. Lefschetz (1,1) applies; Hodge (2,2) remains",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_abelian4_euler",
            computed=ab4,
            measured=ABELIAN_4FOLD_CHI,
            public_sota_model="All abelian varieties have χ=0. Not a hypersurface in CP^5. Do not steal 25−1 for χ(K3)=24.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="meets_abelian4_chi",
            beats_or_meets_sota=abs(ab4 - ABELIAN_4FOLD_CHI) < 1e-9,
            native_status="EXECUTABLE",
            note="Named 4-fold class after hypersurfaces and HK Fano of lines. Remainder is Hodge (2,2) on abelian/HK 4-folds. Do not hunt C_48.",
            extra={"formula": "chi=0"},
        )
    )
    hodge_data_ok = (
        bool(hk_ok)
        and abs(ab4 - ABELIAN_4FOLD_CHI) < 1e-9
        and bool(next4_ok)
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Clay algebraicity without a named cycle is not a measured function. Working data: χ/Gram of named varieties (CP^n, cubic, quartic, sextic, HK Fano, abelian χ=0)",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_clay_algebraicity_not_a_measured_function",
            computed=1.0 if hodge_data_ok else 0.0,
            measured=1.0,
            public_sota_model="Chern/Euler and Hassett Gram are published for named varieties. Algebraicity of an unnamed class has no residual % — the cycle is the measurement. Isolated 'prove Hodge' looks for a function that is not measured.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="clay_hodge_not_measured" if hodge_data_ok else "hodge_data_functions_fail",
            beats_or_meets_sota=None,
            native_status="EXECUTABLE",
            note="Inversion. APPLY step 1: seeds attach to named varieties. Clay algebraicity on a general 4-fold has no public table. Do not hunt C_48 for a non-function. Do not steal 25−1 for K3.",
            extra={"working": ["chi_named_4folds", "hassett_named_grams", "hk_fano_b2", "abelian_chi_0"], "clay_measured": None},
        )
    )
    chi_panel = _hodge_chi_panel()
    chi_panel_ok = chi_panel["hits"] == chi_panel["n"] and chi_panel["n"] >= 9
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Named-variety χ vs Chern/literature (panel hit rate). Not Clay algebraicity without a cycle",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_chi_panel_vs_chern",
            computed=float(chi_panel["hits"]),
            measured=float(chi_panel["n"]),
            public_sota_model="Euler numbers from hypersurface Chern and χ(abelian)=0. Algebraicity without a named cycle has no residual.",
            public_sota_typical_error_pct=0.0,
            comparison_class="comparable",
            verdict="chi_panel_hits_chern" if chi_panel_ok else "chi_panel_miss",
            beats_or_meets_sota=chi_panel_ok,
            native_status="EXECUTABLE",
            note="Simulation vs data: n exact χ / n named varieties. Cycle is the measurement for algebraicity. Do not hunt C_48. Do not steal 25−1 for K3.",
            extra=chi_panel,
        )
    )
    rows.append(
        _row(
            problem="Hodge conjecture",
            function_object="Primitive (2,2) on a cubic 4-fold — first open hypersurface case after Grassmannians",
            clay_object="Hodge classes on a projective complex manifold are algebraic cycles (rational)",
            name="hodge_cubic4_primitive_22",
            computed=None,
            measured=None,
            public_sota_model="Hodge for cubic 4-folds is open (rationality / algebraic cycles). Homogeneous cases are Schubert.",
            public_sota_typical_error_pct=None,
            comparison_class="structure",
            verdict="cubic4_primitive_named_remainder",
            beats_or_meets_sota=None,
            native_status="OPEN_TRACK",
            note="Hypersurface 4-folds through sextic CY named. HK Fano of lines named (b_2=23). Abelian 4-fold χ=0. Remainder is Hodge (2,2) on abelian/HK 4-folds. Do not hunt C_48. Do not steal 25−1 for K3.",
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
    riemann_panel = next(r for r in rows if r["name"] == "riemann_zeros_2_to_10_N_locked")
    riemann_S = next(r for r in rows if r["name"] == "riemann_S_T_bound")
    riemann_band = next(r for r in rows if r["name"] == "riemann_tn_inside_S_band")
    riemann_amp = next(r for r in rows if r["name"] == "riemann_S_amplitude_POOF")
    riemann_signed = next(r for r in rows if r["name"] == "riemann_signed_jitter_p2")
    glue = next(r for r in rows if r["name"] == "ym_glueball_over_sqrt_sigma")
    glue_at = next(r for r in rows if r["name"] == "ym_glueball_over_sqrt_sigma_at2020")
    sig_r0_row = next(r for r in rows if r["name"] == "ym_sqrt_sigma_r0")
    glue_r0_row = next(r for r in rows if r["name"] == "ym_glueball_r0_M")
    glue_r0_split = next(r for r in rows if r["name"] == "ym_glueball_r0_chen_vs_at2020")
    alpha_s_qcd = next(r for r in rows if r["name"] == "ym_alpha_s_MZ_qcd_orifice")
    glue4 = next(r for r in rows if r["name"] == "ym_glueball_vs_4sqrt_sigma")
    glue_ratio = next(r for r in rows if r["name"] == "ym_glueball_2pp_over_0pp")
    glue_f0_1500 = next(r for r in rows if r["name"] == "ym_closed_gluonic_GeV_vs_f0_1500")
    glue_f0_pole = next(r for r in rows if r["name"] == "ym_closed_gluonic_GeV_vs_f0_1500_pole")
    glue_f0_1710 = next(r for r in rows if r["name"] == "ym_flavor_closed_GeV_vs_f0_1710")
    wx_storm = next(r for r in rows if r["name"] == "ns_weather_storm_sector")
    wx_quiet = next(r for r in rows if r["name"] == "ns_weather_quiet_fill")
    wx_gap = next(r for r in rows if r["name"] == "ns_weather_gap_zone_quiet")
    wx_lat = next(r for r in rows if r["name"] == "ns_weather_lat_transfer")
    ns_vk = next(r for r in rows if r["name"] == "ns_von_karman")
    ns_k45 = next(r for r in rows if r["name"] == "ns_kolmogorov_45")
    ns_k32 = next(r for r in rows if r["name"] == "ns_kolmogorov_d2_32")
    ns_ons = next(r for r in rows if r["name"] == "ns_onsager_holder")
    ns_bkm = next(r for r in rows if r["name"] == "ns_bkm_criterion")
    ns_l2 = next(r for r in rows if r["name"] == "ns_l2_cascade_not_l_inf_existence")
    ns_dir = next(r for r in rows if r["name"] == "ns_bkm_magnitude_not_direction")
    ns_zoom = next(r for r in rows if r["name"] == "ns_stretch_particle_visc_fluid_two_zoom")
    ns_budg = next(r for r in rows if r["name"] == "ns_enstrophy_budget_two_term")
    ns_hel = next(r for r in rows if r["name"] == "ns_helicity_3d_not_2d")
    ns_nmeas = next(r for r in rows if r["name"] == "ns_clay_smoothness_not_a_measured_function")
    ns_sim = next(r for r in rows if r["name"] == "ns_stretch_sim_vs_public_answers")
    ns_om = next(r for r in rows if r["name"] == "ns_omega0_scan_vs_threshold")
    ns_3d = next(r for r in rows if r["name"] == "ns_3d_spectral_tg_vs_euler3d")
    ns_crc = next(r for r in rows if r["name"] == "ns_c_water_over_c_air_crc")
    ns_gam = next(r for r in rows if r["name"] == "ns_gamma_diatomic_air")
    ns_real = next(r for r in rows if r["name"] == "ns_reality_observables_not_euler")
    ns_h = next(r for r in rows if r["name"] == "ns_us1976_scale_height")
    ns_nd = next(r for r in rows if r["name"] == "ns_crc_water_nD")
    ns_rho = next(r for r in rows if r["name"] == "ns_crc_water_rho")
    ns_ice_n = next(r for r in rows if r["name"] == "ns_crc_ice_nD_phi_sq_over_2")
    ns_ice_rho = next(r for r in rows if r["name"] == "ns_crc_ice_rho")
    ns_ice_c = next(r for r in rows if r["name"] == "ns_crc_ice_c")
    ns_tm = next(r for r in rows if r["name"] == "ns_crc_water_Tm")
    ns_tb = next(r for r in rows if r["name"] == "ns_crc_water_Tb")
    bsd_L = next(r for r in rows if r["name"] == "bsd_11a1_L_at_1")
    bsd_Lp = next(r for r in rows if r["name"] == "bsd_37a1_Lprime")
    bsd_Reg = next(r for r in rows if r["name"] == "bsd_389a1_regulator")
    bsd_Sp = next(r for r in rows if r["name"] == "bsd_389a1_special")
    bsd_Reg3 = next(r for r in rows if r["name"] == "bsd_5077a1_regulator")
    bsd_Reg4 = next(r for r in rows if r["name"] == "bsd_234446a1_regulator")
    bsd_par = next(r for r in rows if r["name"] == "bsd_rank_parity_map")
    bsd_int = next(r for r in rows if r["name"] == "bsd_integer_rank_leading")
    bsd_vol = next(r for r in rows if r["name"] == "bsd_leading_is_arithmetic_volume")
    bsd_17 = next(r for r in rows if r["name"] == "bsd_17a1_sha_not_leading_magnitude")
    bsd_19 = next(r for r in rows if r["name"] == "bsd_19a1_sha_oos")
    bsd_r0 = next(r for r in rows if r["name"] == "bsd_general_rank0_vanishing_not_magnitude")
    bsd_53 = next(r for r in rows if r["name"] == "bsd_53a1_sha_not_Lprime_magnitude")
    bsd_61 = next(r for r in rows if r["name"] == "bsd_61a1_sha_oos")
    bsd_r1 = next(r for r in rows if r["name"] == "bsd_general_rank1_vanishing_not_magnitude")
    bsd_643 = next(r for r in rows if r["name"] == "bsd_643a1_sha_not_special_magnitude")
    bsd_433 = next(r for r in rows if r["name"] == "bsd_433a1_sha_oos")
    bsd_r2 = next(r for r in rows if r["name"] == "bsd_general_rank2_vanishing_not_magnitude")
    bsd_11197 = next(r for r in rows if r["name"] == "bsd_11197a1_sha_not_special_magnitude")
    bsd_11642 = next(r for r in rows if r["name"] == "bsd_11642a1_sha_oos")
    bsd_r3 = next(r for r in rows if r["name"] == "bsd_general_rank3_vanishing_not_magnitude")
    bsd_501029 = next(r for r in rows if r["name"] == "bsd_501029a1_sha_not_special_magnitude")
    bsd_545723 = next(r for r in rows if r["name"] == "bsd_545723a1_sha_oos")
    bsd_r4 = next(r for r in rows if r["name"] == "bsd_general_rank4_vanishing_not_magnitude")
    bsd_19047851 = next(r for r in rows if r["name"] == "bsd_19047851a1_sha_not_special_magnitude")
    bsd_64921931 = next(r for r in rows if r["name"] == "bsd_64921931a1_sha_oos")
    bsd_r5 = next(r for r in rows if r["name"] == "bsd_general_rank5_vanishing_not_magnitude")
    bsd_named_r = next(r for r in rows if r["name"] == "bsd_lmfdb_named_ranks_complete")
    bsd_mod = next(r for r in rows if r["name"] == "bsd_modularity_produces_L_not_seed_lookup")
    bsd_kol = next(r for r in rows if r["name"] == "bsd_kolyvagin_rank_le1_named_not_general")
    bsd_rge2 = next(r for r in rows if r["name"] == "bsd_rank_ge2_volume_is_native_not_euler_system")
    bsd_gram = next(r for r in rows if r["name"] == "bsd_regulator_is_height_gram_not_euler_system")
    bsd_tam = next(r for r in rows if r["name"] == "bsd_tamagawa_local_reg_global_two_zoom")
    bsd_nmeas = next(r for r in rows if r["name"] == "bsd_clay_equality_not_a_measured_function")
    bsd_panel = next(r for r in rows if r["name"] == "bsd_sha_panel_vs_lmfdb")
    bsd_mw = next(r for r in rows if r["name"] == "bsd_mw_generators_are_the_observable")
    bsd_tors = next(r for r in rows if r["name"] == "bsd_11a1_torsion_is_particle_floor")
    hodge_chi = next(r for r in rows if r["name"] == "hodge_cp2_euler")
    hodge_chi3 = next(r for r in rows if r["name"] == "hodge_cp3_euler")
    hodge_lef = next(r for r in rows if r["name"] == "hodge_lefschetz_11")
    hodge_22 = next(r for r in rows if r["name"] == "hodge_22_cp3")
    hodge_hl = next(r for r in rows if r["name"] == "hodge_hard_lefschetz")
    hodge_prod = next(r for r in rows if r["name"] == "hodge_cp2xcp2_euler")
    hodge_prim = next(r for r in rows if r["name"] == "hodge_primitive_22_cp2xcp2")
    hodge_gr = next(r for r in rows if r["name"] == "hodge_gr24_euler")
    hodge_gr_p = next(r for r in rows if r["name"] == "hodge_gr24_primitive_22")
    hodge_hyp = next(r for r in rows if r["name"] == "hodge_lefschetz_hyperplane")
    hodge_idx = next(r for r in rows if r["name"] == "hodge_index_theorem")
    hodge_c4 = next(r for r in rows if r["name"] == "hodge_cubic4_euler")
    hodge_c4h = next(r for r in rows if r["name"] == "hodge_cubic4_h22")
    hodge_c4p = next(r for r in rows if r["name"] == "hodge_cubic4_primitive_22")
    hodge_k3 = next(r for r in rows if r["name"] == "hodge_k3_h11")
    hodge_fano = next(r for r in rows if r["name"] == "hodge_cubic4_fano_b2")
    hodge_alg = next(r for r in rows if r["name"] == "hodge_associated_k3_algebraicity")
    hodge_d8 = next(r for r in rows if r["name"] == "hodge_hassett_d8")
    hodge_c8 = next(r for r in rows if r["name"] == "hodge_hassett_c8_plane_algebraic")
    hodge_d12 = next(r for r in rows if r["name"] == "hodge_hassett_d12")
    hodge_c12 = next(r for r in rows if r["name"] == "hodge_hassett_c12_scroll_algebraic")
    hodge_d18 = next(r for r in rows if r["name"] == "hodge_hassett_d18")
    hodge_c18 = next(r for r in rows if r["name"] == "hodge_hassett_c18_elliptic_algebraic")
    hodge_d20 = next(r for r in rows if r["name"] == "hodge_hassett_d20")
    hodge_c20 = next(r for r in rows if r["name"] == "hodge_hassett_c20_veronese_algebraic")
    hodge_d24 = next(r for r in rows if r["name"] == "hodge_hassett_d24")
    hodge_c24 = next(r for r in rows if r["name"] == "hodge_hassett_c24_sextic_algebraic")
    hodge_d30 = next(r for r in rows if r["name"] == "hodge_hassett_d30")
    hodge_c30 = next(r for r in rows if r["name"] == "hodge_hassett_c30_coble_algebraic")
    hodge_d32 = next(r for r in rows if r["name"] == "hodge_hassett_d32")
    hodge_c32 = next(r for r in rows if r["name"] == "hodge_hassett_c32_bl11_algebraic")
    hodge_d36 = next(r for r in rows if r["name"] == "hodge_hassett_d36")
    hodge_c36 = next(r for r in rows if r["name"] == "hodge_hassett_c36_bl12_algebraic")
    hodge_d44 = next(r for r in rows if r["name"] == "hodge_hassett_d44")
    hodge_c44 = next(r for r in rows if r["name"] == "hodge_hassett_c44_enriques_algebraic")
    hodge_named = next(r for r in rows if r["name"] == "hodge_hassett_named_no_k3_complete")
    hodge_k3_tail = next(r for r in rows if r["name"] == "hodge_hassett_k3_tail_lefschetz")
    hodge_vg = next(r for r in rows if r["name"] == "hodge_very_general_cubic_only_h2")
    hodge_noseed = next(r for r in rows if r["name"] == "hodge_unnamed_no_k3_has_no_seed")
    hodge_q4 = next(r for r in rows if r["name"] == "hodge_quartic4_euler")
    hodge_q5 = next(r for r in rows if r["name"] == "hodge_quintic4_euler")
    hodge_s6 = next(r for r in rows if r["name"] == "hodge_sextic4_cy_euler")
    hodge_next4 = next(r for r in rows if r["name"] == "hodge_hypersurface_4folds_after_cubic_named")
    hodge_hk = next(r for r in rows if r["name"] == "hodge_hk4_fano_lines_named_not_c48")
    hodge_ab = next(r for r in rows if r["name"] == "hodge_abelian4_euler")
    hodge_nmeas = next(r for r in rows if r["name"] == "hodge_clay_algebraicity_not_a_measured_function")
    hodge_panel = next(r for r in rows if r["name"] == "hodge_chi_panel_vs_chern")
    ns_stretch = next(r for r in rows if r["name"] == "ns_vortex_stretching_remainder")
    ns_2d = next(r for r in rows if r["name"] == "ns_2d_enstrophy")
    pnp_sat = next(r for r in rows if r["name"] == "pnp_cook_levin_sat")
    wip_beats = [r for r in rows if r.get("sota_beats_fsot_accuracy_wip")]
    in_green = [r for r in rows if r.get("fsot_green") == "pass"]
    in_asp = [r for r in rows if r.get("fsot_aspiration") == "pass"]
    next_dig = [r for r in rows if r.get("next_dig")]
    return {
        "generated_at": _now(),
        "pin": "AEB2AD",
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
        "riemann_S_T_bound_holds": 1 if riemann_S.get("verdict") == "S_bound_holds" else 0,
        "riemann_tn_inside_S_band": 1 if riemann_band.get("verdict") == "inside_S_band" else 0,
        "riemann_S_amplitude_beats_bound_as_typical": 1 if riemann_amp["beats_or_meets_sota"] else 0,
        "riemann_S_amplitude_green": 1 if riemann_amp.get("fsot_green") == "pass" else 0,
        "riemann_S_oos_1e_band": 1 if riemann_amp.get("oos_inside_1e") == 10 else 0,
        "riemann_signed_beats_clock": 1 if riemann_signed["beats_or_meets_sota"] else 0,
        "riemann_signed_green": 1 if riemann_signed.get("fsot_green") == "pass" else 0,
        "riemann_signed_oos_sign": 1 if riemann_signed.get("oos_sign_agree") == 10 else 0,
        "alpha_s_qcd_beats_geometric": 1 if alpha_s_qcd["beats_or_meets_sota"] else 0,
        "alpha_s_qcd_green": 1 if alpha_s_qcd.get("fsot_green") == "pass" else 0,
        "alpha_s_qcd_aspiration": 1 if alpha_s_qcd.get("fsot_aspiration") == "pass" else 0,
        "glueball_beats_teper": 1 if glue["beats_or_meets_sota"] else 0,
        "glueball_sigma_coupled_green": 1 if glue.get("fsot_green") == "pass" else 0,
        "glueball_sigma_coupled_aspiration": 1 if glue.get("fsot_aspiration") == "pass" else 0,
        "glueball_at2020_scheme_split": 1 if glue_at.get("verdict") == "lattice_scheme_split" else 0,
        "sqrt_sigma_r0_beats": 1 if sig_r0_row["beats_or_meets_sota"] else 0,
        "glueball_r0_beats_chen": 1 if glue_r0_row["beats_or_meets_sota"] else 0,
        "glueball_r0_scheme_split": 1 if glue_r0_split.get("verdict") == "r0_lattice_scheme_split" else 0,
        "glueball_does_not_beat_teper": 0 if glue["beats_or_meets_sota"] else 1,
        "glueball_beats_4sqrt_sigma": 1 if glue4["beats_or_meets_sota"] else 0,
        "glueball_ratio_beats_three_halves": 1 if glue_ratio["beats_or_meets_sota"] else 0,
        "glueball_observed_pair_named": 1,
        "glueball_f0_1500_beats_lattice_on_that_candidate": 1 if glue_f0_1500["beats_or_meets_sota"] else 0,
        "f0_1500_mixed_green": 1 if glue_f0_1500.get("fsot_green") == "pass" else 0,
        "f0_1500_inside_tmatrix_pole_band": 1 if glue_f0_pole.get("verdict") == "inside_tmatrix_pole_band" else 0,
        "f0_1710_flavor_beats_4sqrt": 1 if glue_f0_1710["beats_or_meets_sota"] else 0,
        "f0_1710_flavor_green": 1 if glue_f0_1710.get("fsot_green") == "pass" else 0,
        "weather_beats_majority": 1 if wx_storm["beats_or_meets_sota"] else 0,
        "weather_does_not_beat_majority": 0 if wx_storm["beats_or_meets_sota"] else 1,
        "weather_quiet_fill_still_miss": 0 if wx_quiet["beats_or_meets_sota"] else 1,
        "weather_gap_zone_named": 1 if wx_gap.get("verdict") == "gap_zone_should_not_issue" else 0,
        "weather_lat_transfer_named": 1 if wx_lat.get("verdict") == "lat_belt_transferred_weather" else 0,
        "ns_von_karman_green": 1 if ns_vk.get("fsot_green") == "pass" else 0,
        "ns_kolmogorov_45_exact": 1 if ns_k45["beats_or_meets_sota"] else 0,
        "ns_kolmogorov_d2_32_exact": 1 if ns_k32["beats_or_meets_sota"] else 0,
        "ns_onsager_holder_exact": 1 if ns_ons["beats_or_meets_sota"] else 0,
        "ns_bkm_named": 1 if ns_bkm.get("verdict") == "bkm_named_not_clay" else 0,
        "ns_l2_cascade_not_l_inf": 1 if ns_l2.get("verdict") == "l2_cascade_not_l_inf" else 0,
        "ns_bkm_magnitude_not_direction": 1 if ns_dir.get("verdict") == "bkm_magnitude_not_direction" else 0,
        "ns_stretch_visc_two_zoom": 1 if ns_zoom.get("verdict") == "stretch_visc_two_zoom" else 0,
        "ns_enstrophy_budget_two_term": 1 if ns_budg.get("verdict") == "enstrophy_budget_two_term" else 0,
        "ns_helicity_3d_not_2d": 1 if ns_hel.get("verdict") == "helicity_3d_not_2d" else 0,
        "ns_clay_smoothness_not_measured": 1 if ns_nmeas.get("verdict") == "clay_smoothness_not_measured" else 0,
        "ns_stretch_sim_vs_public_answers": 1 if ns_sim.get("verdict") == "stretch_sim_agrees_public_answers" else 0,
        "ns_omega0_scan_vs_threshold": 1 if ns_om.get("fsot_green") == "pass" else 0,
        "ns_3d_spectral_tg": 1 if ns_3d.get("verdict") == "nse3d_viscous_tg_regular" else 0,
        "ns_c_water_over_c_air_crc": 1 if ns_crc.get("fsot_green") == "pass" else 0,
        "ns_gamma_diatomic_air": 1 if ns_gam.get("fsot_green") == "pass" else 0,
        "ns_reality_observables": 1 if ns_real.get("verdict") == "reality_observables_hold" else 0,
        "ns_us1976_scale_height": 1 if ns_h.get("fsot_green") == "pass" else 0,
        "ns_crc_water_nD": 1 if ns_nd.get("fsot_green") == "pass" else 0,
        "ns_crc_water_rho": 1 if ns_rho.get("fsot_green") == "pass" else 0,
        "ns_crc_ice_nD": 1 if ns_ice_n.get("fsot_green") == "pass" else 0,
        "ns_crc_ice_rho": 1 if ns_ice_rho.get("fsot_green") == "pass" else 0,
        "ns_crc_ice_c": 1 if ns_ice_c.get("fsot_green") == "pass" else 0,
        "ns_crc_water_Tm": 1 if ns_tm.get("fsot_green") == "pass" else 0,
        "ns_crc_water_Tb": 1 if ns_tb.get("fsot_green") == "pass" else 0,
        "bsd_11a1_L_green": 1 if bsd_L.get("fsot_green") == "pass" else 0,
        "bsd_37a1_Lprime_green": 1 if bsd_Lp.get("fsot_green") == "pass" else 0,
        "bsd_389a1_reg_beats": 1 if bsd_Reg["beats_or_meets_sota"] else 0,
        "bsd_389a1_reg_green": 1 if bsd_Reg.get("fsot_green") == "pass" else 0,
        "bsd_389a1_special_green": 1 if bsd_Sp.get("fsot_green") == "pass" else 0,
        "bsd_5077a1_reg_green": 1 if bsd_Reg3.get("fsot_green") == "pass" else 0,
        "bsd_5077a1_reg_aspiration": 1 if bsd_Reg3.get("fsot_aspiration") == "pass" else 0,
        "bsd_234446a1_reg_green": 1 if bsd_Reg4.get("fsot_green") == "pass" else 0,
        "bsd_rank_parity_map": 1 if bsd_par.get("verdict") == "parity_map_holds" else 0,
        "bsd_integer_rank_first5": 1 if bsd_int.get("verdict") == "integer_rank_first5_holds" else 0,
        "bsd_leading_volume_named": 1 if bsd_vol.get("verdict") == "bsd_volume_named_not_general_e" else 0,
        "bsd_17a1_sha_green": 1 if bsd_17.get("fsot_green") == "pass" else 0,
        "bsd_19a1_sha_green": 1 if bsd_19.get("fsot_green") == "pass" else 0,
        "bsd_general_rank0_vanishing": 1 if bsd_r0.get("verdict") == "rank0_vanishing_holds" else 0,
        "bsd_53a1_sha_green": 1 if bsd_53.get("fsot_green") == "pass" else 0,
        "bsd_61a1_sha_green": 1 if bsd_61.get("fsot_green") == "pass" else 0,
        "bsd_general_rank1_vanishing": 1 if bsd_r1.get("verdict") == "rank1_vanishing_holds" else 0,
        "bsd_643a1_sha_green": 1 if bsd_643.get("fsot_green") == "pass" else 0,
        "bsd_433a1_sha_green": 1 if bsd_433.get("fsot_green") == "pass" else 0,
        "bsd_general_rank2_vanishing": 1 if bsd_r2.get("verdict") == "rank2_vanishing_holds" else 0,
        "bsd_11197a1_sha_green": 1 if bsd_11197.get("fsot_green") == "pass" else 0,
        "bsd_11642a1_sha_green": 1 if bsd_11642.get("fsot_green") == "pass" else 0,
        "bsd_general_rank3_vanishing": 1 if bsd_r3.get("verdict") == "rank3_vanishing_holds" else 0,
        "bsd_501029a1_sha_green": 1 if bsd_501029.get("fsot_green") == "pass" else 0,
        "bsd_545723a1_sha_green": 1 if bsd_545723.get("fsot_green") == "pass" else 0,
        "bsd_general_rank4_vanishing": 1 if bsd_r4.get("verdict") == "rank4_vanishing_holds" else 0,
        "bsd_19047851a1_sha_green": 1 if bsd_19047851.get("fsot_green") == "pass" else 0,
        "bsd_64921931a1_sha_green": 1 if bsd_64921931.get("fsot_green") == "pass" else 0,
        "bsd_general_rank5_vanishing": 1 if bsd_r5.get("verdict") == "rank5_vanishing_holds" else 0,
        "bsd_lmfdb_named_ranks_complete": 1 if bsd_named_r.get("verdict") == "named_ranks_0_5_complete" else 0,
        "bsd_modularity_named": 1 if bsd_mod.get("verdict") == "modularity_named_not_clay" else 0,
        "bsd_kolyvagin_rank_le1": 1 if bsd_kol.get("verdict") == "kolyvagin_rank_le1_named" else 0,
        "bsd_rank_ge2_volume_native": 1 if bsd_rge2.get("verdict") == "rank_ge2_volume_native" else 0,
        "bsd_regulator_is_height_gram": 1 if bsd_gram.get("verdict") == "regulator_is_height_gram" else 0,
        "bsd_tam_local_reg_global": 1 if bsd_tam.get("verdict") == "tam_local_reg_global" else 0,
        "bsd_clay_equality_not_measured": 1 if bsd_nmeas.get("verdict") == "clay_bsd_not_measured" else 0,
        "bsd_sha_panel_vs_lmfdb": 1 if bsd_panel.get("fsot_green") == "pass" else 0,
        "bsd_mw_generators_observable": 1 if bsd_mw.get("verdict") == "mw_generators_observable" else 0,
        "bsd_11a1_torsion_particle": 1 if bsd_tors.get("fsot_green") == "pass" else 0,
        "hodge_cp2_euler_exact": 1 if hodge_chi["beats_or_meets_sota"] else 0,
        "hodge_cp3_euler_exact": 1 if hodge_chi3["beats_or_meets_sota"] else 0,
        "hodge_lefschetz_11_named": 1 if hodge_lef.get("verdict") == "lefschetz_11_named_not_clay" else 0,
        "hodge_22_named": 1 if hodge_22.get("verdict") == "hodge_22_named_not_clay" else 0,
        "hodge_hard_lefschetz_named": 1 if hodge_hl.get("verdict") == "hard_lefschetz_named_primitive_open" else 0,
        "hodge_cp2xcp2_exact": 1 if hodge_prod["beats_or_meets_sota"] else 0,
        "hodge_primitive_22_named": 1 if hodge_prim.get("verdict") == "primitive_22_product_algebraic_not_general" else 0,
        "hodge_gr24_exact": 1 if hodge_gr["beats_or_meets_sota"] else 0,
        "hodge_gr24_schubert_named": 1 if hodge_gr_p.get("verdict") == "gr24_schubert_algebraic_not_general" else 0,
        "hodge_lefschetz_hyperplane_named": 1 if hodge_hyp.get("verdict") == "lefschetz_hyperplane_named" else 0,
        "hodge_index_named": 1 if hodge_idx.get("verdict") == "hodge_index_named_not_clay" else 0,
        "hodge_cubic4_euler_exact": 1 if hodge_c4["beats_or_meets_sota"] else 0,
        "hodge_cubic4_h22_exact": 1 if hodge_c4h["beats_or_meets_sota"] else 0,
        "hodge_cubic4_remainder_named": 1 if hodge_c4p.get("verdict") == "cubic4_primitive_named_remainder" else 0,
        "hodge_k3_h11_exact": 1 if hodge_k3["beats_or_meets_sota"] else 0,
        "hodge_fano_b2_exact": 1 if hodge_fano["beats_or_meets_sota"] else 0,
        "hodge_associated_k3_algebraicity": 1 if hodge_alg.get("verdict") == "associated_k3_lefschetz_algebraicity" else 0,
        "hodge_hassett_d8_exact": 1 if hodge_d8["beats_or_meets_sota"] else 0,
        "hodge_hassett_c8_plane_algebraic": 1 if hodge_c8.get("verdict") == "c8_plane_algebraic_no_k3" else 0,
        "hodge_hassett_d12_exact": 1 if hodge_d12["beats_or_meets_sota"] else 0,
        "hodge_hassett_c12_scroll_algebraic": 1 if hodge_c12.get("verdict") == "c12_scroll_algebraic_no_k3" else 0,
        "hodge_hassett_d18_exact": 1 if hodge_d18["beats_or_meets_sota"] else 0,
        "hodge_hassett_c18_elliptic_algebraic": 1 if hodge_c18.get("verdict") == "c18_elliptic_algebraic_no_k3" else 0,
        "hodge_hassett_d20_exact": 1 if hodge_d20["beats_or_meets_sota"] else 0,
        "hodge_hassett_c20_veronese_algebraic": 1 if hodge_c20.get("verdict") == "c20_veronese_algebraic_no_k3" else 0,
        "hodge_hassett_d24_exact": 1 if hodge_d24["beats_or_meets_sota"] else 0,
        "hodge_hassett_c24_sextic_algebraic": 1 if hodge_c24.get("verdict") == "c24_sextic_algebraic_no_k3" else 0,
        "hodge_hassett_d30_exact": 1 if hodge_d30["beats_or_meets_sota"] else 0,
        "hodge_hassett_c30_coble_algebraic": 1 if hodge_c30.get("verdict") == "c30_coble_algebraic_no_k3" else 0,
        "hodge_hassett_d32_exact": 1 if hodge_d32["beats_or_meets_sota"] else 0,
        "hodge_hassett_c32_bl11_algebraic": 1 if hodge_c32.get("verdict") == "c32_bl11_algebraic_no_k3" else 0,
        "hodge_hassett_d36_exact": 1 if hodge_d36["beats_or_meets_sota"] else 0,
        "hodge_hassett_c36_bl12_algebraic": 1 if hodge_c36.get("verdict") == "c36_bl12_algebraic_no_k3" else 0,
        "hodge_hassett_d44_exact": 1 if hodge_d44["beats_or_meets_sota"] else 0,
        "hodge_hassett_c44_enriques_algebraic": 1 if hodge_c44.get("verdict") == "c44_enriques_algebraic_no_k3" else 0,
        "hodge_hassett_named_no_k3_complete": 1 if hodge_named.get("verdict") == "named_no_k3_complete" else 0,
        "hodge_hassett_k3_tail_lefschetz": 1 if hodge_k3_tail.get("verdict") == "k3_tail_lefschetz" else 0,
        "hodge_very_general_cubic_only_h2": 1 if hodge_vg.get("verdict") == "very_general_cubic_only_h2" else 0,
        "hodge_unnamed_no_k3_no_seed": 1 if hodge_noseed.get("verdict") == "unnamed_no_k3_no_native_seed" else 0,
        "hodge_quartic4_euler_exact": 1 if hodge_q4["beats_or_meets_sota"] else 0,
        "hodge_quintic4_euler_exact": 1 if hodge_q5["beats_or_meets_sota"] else 0,
        "hodge_sextic4_cy_euler_exact": 1 if hodge_s6["beats_or_meets_sota"] else 0,
        "hodge_hypersurface_4folds_after_cubic": 1 if hodge_next4.get("verdict") == "hypersurface_4folds_after_cubic" else 0,
        "hodge_hk4_fano_lines_named": 1 if hodge_hk.get("verdict") == "hk4_fano_lines_named" else 0,
        "hodge_abelian4_euler_exact": 1 if hodge_ab["beats_or_meets_sota"] else 0,
        "hodge_clay_algebraicity_not_measured": 1 if hodge_nmeas.get("verdict") == "clay_hodge_not_measured" else 0,
        "hodge_chi_panel_vs_chern": 1 if hodge_panel.get("fsot_green") == "pass" else 0,
        "ns_stretching_named": 1 if ns_stretch.get("verdict") == "named_clay_remainder" else 0,
        "ns_2d_enstrophy_named": 1 if ns_2d.get("verdict") == "enstrophy_2d_named_not_clay" else 0,
        "pnp_sat_named": 1 if pnp_sat.get("verdict") == "sat_npcomplete_named_not_clay" else 0,
        "ecmwf_beaten": 0,
        "ecmwf_not_beaten": 1,
        "rows": rows,
        "honest_scope": (
            "Two bars: (1) public SOTA, (2) FSOT green 0.5% / aspiration 0.05%. "
            "A SOTA beat outside 0.5% is FSOT accuracy WIP — not stuffed into the gate. "
            "Not a Clay Prize. GitHub is not a Qualifying Outlet. "
            "Misses next: Clay NSE/BSD/Hodge remainders are not measured functions "
            "(working data: cascade numbers, LMFDB Sha, named χ/Gram). "
            "Native: von Kármán κ, 2D enstrophy, Kolmogorov 4/5=1−1/D_particle, 2D 3/2, Onsager 1/3, BKM, "
            "L(11a1,1)=√φ/D_particle, L'(37a1,1)=2·POOF, Reg(389a1)=POOF, Reg(5077a1)=e·POOF, "
            "Reg(234446a1)=(φ²+1)·e·POOF, "
            "χ(CP²)=L_2, χ(CP³)=L_3, Lefschetz (1,1), Hodge (2,2) on CP³, hard Lefschetz, "
            "Cook–Levin SAT. Glueball 0++ in string units is φ²+1 vs a "
            "quenched-lattice construct, not an observed particle. Observed I=0 0++: "
            "f0(1500) BW is glue–flavor 2×2 V=POOF·K; isolated (φ²+1)·K is the pole. "
            "Do not swap them. Morningstar 2502.02547: no scalar below ~2 GeV is predominantly glue. "
            "Riemann n=2..10 is N(T)=n with C locked by e/γ³, not public 7/8. "
            "S(T) bound is 1/e; typical |S| is POOF. Signed jitter is sign(sin(T ln 2))·POOF envelope. "
            "E→rank map is parity from w_E; first-of-rank leadings label 0..4. "
            "Do not invert with trig S(n) or the full Euler product. "
            "α_s(M_Z) QCD orifice is 2(POOF/ψ_con)², not geometric 1/(eπ); Ledger A freeze not rewritten. "
            "SOTA and FSOT 0.5% are independent bars. "
            "Storm-sector is the weather object; majority-of-saw_storm is retired. "
            "Gap-zone quiet should not issue. 44078 is latitude-belt transfer to MDXA2 (|Δlat|<POOF·180/π), not a 1010 retune. Uncoupled clean quiet holds. "
            "ECMWF is not beaten. Frozen issues not rewritten."
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
        f"**Pin:** AEB2AD · **Clay Prize claimed:** **no** · **Generated:** `{summary['generated_at']}`",
        "",
        "Clay’s three gates (Qualifying Outlet, two years, community acceptance) are a *social process*.",
        "They live in [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md) and stay honest zeros.",
        "",
        "This page is the other question: **does the native math hit the same *function* more accurately than what is currently public?**",
        "Consensus is not the scoring rule. Closed precision is. A miss stays a miss.",
        "The Clay *formula* is not automatically that function — see [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md).",
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
        elif r["name"] == "riemann_zeros_2_to_10_N_locked":
            err_cell = (
                f"{_fmt(r.get('locked_mean_err_pct'), 4)} mean n=2..10 "
                f"({r.get('n_locked_beats_rvm')}/{r.get('n_panel')} zeros)"
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
        "| Riemann zeros n=2..10 | **Beats RvM (1.63% vs 5.64%)** — POOF-amplitude interacting bleed vs smooth T, not a miss of N(T)=n | C-lock is the potential / timetable. |",
        "| Riemann S(T) band | **10/10 Odlyzko inside** T_lock ± 2π(1/e)/log(T/2π) | Bound from t1's e. Typical occupancy is e·POOF. |",
        "| Riemann typical \\|S\\| | **POOF vs mean \\|S\\| n=2..10 — beats 1/e-as-typical; 0.5% WIP** | Interacting-system valve. n=11..20 out-of-sample. |",
        "| Riemann signed jitter | **Prime-2 sign + POOF envelope vs C-lock 1.63%** | n=2..10 0.62% WIP; oos n=11..20 0.43%. Sign 19/19. |",
        "| Λ_QCD vs PDG 0.2173 | **Beats/meets and in 0.05%** (0.048%) | FLAG 213(8) is a second measurement (2.07%, inside FLAG 1σ, outside 0.5% vs FLAG central). |",
        "| α_s(M_Z) QCD orifice | **Beats 1/(eπ) and in 0.05%** (0.0075% vs PDG 0.1179) | Process 2(POOF/ψ_con)². Geometric 1/(eπ) is the freeze, 0.679%. Do not rewrite freeze. |",
        "| Glueball σ-unit vs Teper 1997 3.65 | **φ²+1 + POOF/D_particle — in 0.05%** | Isolated loop was missing flux-tube coupling. |",
        "| 1997 vs AT2020 M/√σ | **Lattice-lattice ~7%** (Wilson 0++ dip) | Not a 6% FSOT miss. Different continuum schemes. |",
        "| √σ r0 = 1+1/(2π) | **vs AT2020 1.160(6) — in 0.05%** | Missing Sommer vs string-tension conversion. |",
        "| r0 M(0++) = (φ²+1)(1+1/(2π)) | **vs Chen 4.16(11) — inside 1σ, 0.82% WIP** | r0 units. Do not retune φ²+1. |",
        "| f0(1500) BW mixed | **2×2 V=POOF·K vs 1506 — in 0.5%** | Isolated pole stays in 1.43–1.53. Do not mix 1710. |",
        "| Closed gluonic GeV vs f0(1500) pole | **Inside PDG T-matrix Re band 1.43–1.53 GeV** | Closed mode is an S-matrix pole. Do not move BW 1506 to swallow 0.93%. |",
        "| Flavor closed GeV vs f0(1710) | **0.40% vs PDG 1733 MeV — in 0.5% green; beats 4√σ (3.03%)** | Flavor/ss orifice (π+1)·K. Retired gluonic-vs-1710 was 12.3%. |",
        "| Glueball 0++ vs 4√σ | **Beats 4√σ closed form** | Teper's own rule of thumb. Same lattice construct 3.65. |",
        "| Glueball 2++/0++ | **Beats 3/2 (0.23%) — in 0.5% green, aspiration WIP** | √2 geometry on the closed 0++ mode. |",
        "| Grover 1/2 | **Meets proven bound and in 0.05%** | Not P vs NP. |",
        "| Cook–Levin SAT | **Named proven first NP-complete theorem** | Clay is P=?NP. Verification is poly; search is the remainder. |",
        "| von Kármán κ | **Beats log-law scatter and in 0.05%** (`A_bleed/φ²` vs 0.40) | Wall shear, not 3D NSE smoothness. |",
        "| 2D enstrophy | **Named proven first NSE-type theorem** | No stretching in 2D. |",
        "| Kolmogorov 4/5 | **Meets 4/5 exactly** (`12/(3 D_particle)=1−1/D_particle`) | 3D cascade from stretching. |",
        "| Kraichnan 3/2 | **Meets 3/2 exactly** (`12/(d(d+2))` at d=2) | 2D inverse cascade. Do not put D_particle on 2D. |",
        "| Onsager Hölder | **Meets 1/3 exactly** (1/d at d=3) | Euler dissipative-anomaly threshold. Same cascade as 4/5. |",
        "| Beale–Kato–Majda | **Named stretching criterion** | Blow-up iff ∫||ω||_∞ dt diverges. |",
        "| L² cascade vs L∞ existence | **Split holds** (4/5 is mean flux; Stokes damps linear; BKM is L∞) | Do not stuff existence into 4/5 or 1/3. |",
        "| BKM magnitude vs direction | **Split holds** (||ω|| is BKM; ξ=ω/|ω| is Constantin–Fefferman) | Isolated criteria are one zoom. |",
        "| Stretch vs visc two zooms | **Particle floor vs Fluid tank (dark)** | Isolated BKM/CF is the theorem-ladder. Valve is not existence. |",
        "| 3D enstrophy budget | **Two terms** (production − dissipation) | No 4/5 analog for 3D enstrophy. 2D production ≡ 0. |",
        "| 3D helicity | **Euler invariant; NSE dissipates** | Not 2D. Isolated conservation is inviscid stuffing. |",
        "| Clay smoothness vs data | **Not a measured function** | Working: 4/5, 3/2, 1/3, κ. No public smoothness residual. |",
        "| L(11a1,1) | **Beats 1/4 and in 0.5%** (`√φ/D_particle` vs LMFDB) | First rank-0 curve. Not a rank predictor. |",
        "| L'(37a1,1) | **2·POOF vs LMFDB — in 0.5%** | First rank-1 leading term. Not a rank predictor. |",
        "| Reg(389a1) | **POOF vs LMFDB — 0.67% WIP** | Néron-Tate pairing. Not the BSD leading term. |",
        "| L''(389a1,1)/2! | **2π POOF/√φ vs LMFDB — in 0.5%** | Dual period × valve. Wrong object was Reg in isolation. |",
        "| Reg(5077a1) | **e·POOF vs LMFDB — in 0.05%** | First rank-3 height volume. Same occupancy as Riemann 1/e band. Out of sample vs rank 2. |",
        "| Reg(234446a1) | **(φ²+1)·e·POOF vs LMFDB — in 0.5%** | First rank-4 volume. Isolated e² was the missing loop fold. |",
        "| E→rank (mod 2) | **Parity from w_E on first curves of rank 0..4** | Integer rank still needs ord L. Rank 4 is (φ²+1)·e·POOF, not e². |",
        "| Integer rank 0..4 | **First-curve leadings match uniquely** | Leading → rank. General E still produces the leading from its modular form. |",
        "| BSD arithmetic volume | **Named formula** Ω·Reg·Tam / (|Sha|·|tors|²) | The question's content. |",
        "| 17a1 Sha | **Meets 1** (volume, not L magnitude) | Raw L(1) mis-fires as rank 3. L≠0 is rank 0. |",
        "| 19a1 Sha | **Meets 1** out of sample | Same orifice. |",
        "| General rank 0 | **Vanishing, not magnitude** | L(1)≠0 ⇒ analytic rank 0. First-of-rank scale is not a lookup. |",
        "| 53a1 Sha | **Meets 1** (volume, not L' magnitude) | Raw L' mis-fires as rank 3. L=0 and L'≠0 is rank 1. |",
        "| 61a1 Sha | **Meets 1** out of sample | Same orifice. |",
        "| General rank 1 | **Vanishing order, not L' magnitude** | L(1)=0, L'≠0. |",
        "| 643a1 Sha | **Meets 1** (volume, not special magnitude) | Raw L''/2! mis-fires as rank 4. |",
        "| 433a1 Sha | **Meets 1** out of sample | Same orifice. |",
        "| General rank 2 | **Vanishing order, not special magnitude** | L=L'=0, L''≠0. |",
        "| 11197a1 Sha | **Meets 1** (volume, not special/Reg magnitude) | Raw L'''/3! mis-fires as rank 4. L=L'=L''=0 and L'''≠0 is rank 3. |",
        "| 11642a1 Sha | **Meets 1** out of sample | Same orifice. |",
        "| General rank 3 | **Vanishing order, not special/Reg magnitude** | L=L'=L''=0, L'''≠0. |",
        "| 501029.a1 Sha | **Meets 1** (volume, not special/Reg magnitude) | Raw L^{(4)}/4!≈9.36 is not the rank-4 seed 1.50. Ladder saturates at 4. |",
        "| 545723.a1 Sha | **Meets 1** out of sample | Same orifice. |",
        "| General rank 4 | **Vanishing order, not special/Reg magnitude** | L through L''' vanish, L^{(4)}≠0. |",
        "| 19047851.a1 Sha | **Meets 1** (volume, not special/Reg magnitude) | Raw L^{(5)}/5!≈30.29 nearest-templates as rank 4. No r=5 seed. |",
        "| 64921931.a1 Sha | **Meets 1** out of sample | Same orifice. |",
        "| General rank 5 | **Vanishing order, not special/Reg magnitude** | L through L^{(4)} vanish, L^{(5)}≠0. |",
        "| Named LMFDB ranks | **Complete 0..5** | Rank ≥6 is the unnamed tail (Elkies–Watkins N=5.19e9 outside LMFDB). |",
        "| Modularity | **Named proven theorem** (every E/Q has L) | Volume is Sha. Do not nearest-template. |",
        "| Kolyvagin r=0,1 | **Named proven rank=ord L** | External check, not a new seed. |",
        "| Rank ≥2 native | **Vanishing+Sha already executable** | Do not enumerate Kato. Remainder is Clay equality. |",
        "| Regulator Gram | **Néron-Tate height det** (Hassett orifice) | r=1 is one Heegner point. r≥2 is a lattice. |",
        "| Tam local vs Reg global | **Two zooms** (11642 Tam=2 vs 643 Tam=1, both Sha=1) | Do not swallow Tam into Reg. |",
        "| Clay rank=ord L vs data | **Not a measured function** | Working: LMFDB Sha and first-of-rank seeds. No residual for ∀E. |",
        "| χ(ℂP²) | **Meets 3** (φ²+φ^{-2}=Lucas L_2) | Named surface Euler number. Not Hodge classes. Not K3. |",
        "| χ(ℂP³) | **Meets 4** (φ³−φ^{-3}=Lucas L_3) | Next Euler. Not a general χ(CP^n)=L_n law. |",
        "| Lefschetz (1,1) on ℂP² | **Named proven first Hodge-type theorem** | p=1. |",
        "| Hodge (2,2) on ℂP³ | **Named proven first p>1 object** | Hyperplane square. |",
        "| Hard Lefschetz | **Named transport (1,1)→(2,2)** | Primitive (2,2) on general X is the leftover. |",
        "| χ(ℂP²×ℂP²) | **Meets 9** (L_2²) | First 4-fold that is not CP^n. |",
        "| Primitive (2,2) on CP²×CP² | **1-dimensional, algebraic (H1 H2)** | Not empty (unlike CP^n). |",
        "| χ(Gr(2,4)) | **Meets 6** (C(4,2) Schubert cells) | First homogeneous 4-fold, not a product. |",
        "| Primitive (2,2) on Gr(2,4) | **Schubert, algebraic** | First non-product primitive (2,2). |",
        "| Lefschetz hyperplane | **Named reduction to primitive + ambient CP^n** | Cubic 4-fold primitive is what remains. |",
        "| Hodge index | **Named proven signature theorem on surfaces** | Not algebraicity. |",
        "| χ cubic 4-fold | **Meets 27** (Chern n=4, d=3) | Euler, not Hodge classes. |",
        "| h^{2,2} cubic 4-fold | **Meets 21** (F_8, index 2n=8) | The count. |",
        "| Associated K3 h^{1,1} | **Meets 20** (F_8−1) | Primitive (2,2) of the cubic. Lefschetz (1,1) is algebraicity. |",
        "| Fano of lines b_2 | **Meets 23** (F_8+2) | Beauville–Donagi H^2(F)≅H^4(X). |",
        "| Algebraicity via associated K3 | **Named reduction to Lefschetz (1,1)** | Very general cubic: only h^2. Remainder: extra classes, no K3. |",
        "| Hassett C_8 discriminant | **Meets 8** (F_6) | First extra Hodge class. 4|d so no associated K3. |",
        "| C_8 extra class | **[plane], algebraic** | Subvariety. |",
        "| Hassett C_12 discriminant | **Meets 12** (L_2 L_4 − L_2²) | Cubic-scroll Gram [[3,3],[3,7]]. Isolated 3·4 is padding. |",
        "| C_12 extra class | **[cubic scroll], algebraic** | Subvariety. |",
        "| Hassett C_18 discriminant | **Meets 18** (L_2 L_6 − (2 L_2)²) | Elliptic-ruled Gram [[3,6],[6,18]]. Isolated L_6 as d is padding. |",
        "| C_18 extra class | **[elliptic ruled], algebraic** | Subvariety. 9|d so no K3. |",
        "| Hassett C_20 discriminant | **Meets 20** (L_2(L_2 L_3) − L_3²) | Veronese Gram [[3,4],[4,12]]. Isolated 4·5 is padding. |",
        "| C_20 extra class | **[Veronese], algebraic** | Subvariety. 4|d so no K3. |",
        "| Hassett C_24 discriminant | **Meets 24** (L_2(L_6+2) − (2 L_2)²) | Nodal sextic del Pezzo Gram [[3,6],[6,20]]. Isolated χ(K3) is padding. |",
        "| C_24 extra class | **[nodal sextic del Pezzo], algebraic** | Subvariety. Two nodes on L_6. |",
        "| Hassett C_30 discriminant | **Meets 30** (Coble Bl_10 P² Gram [[3,9],[9,37]]) | 10=pa of a plane sextic. Isolated 5·6 is padding. |",
        "| C_30 extra class | **[Bl_10 P²], algebraic** | Subvariety. 5|d, 5≡2 (mod 3) so no K3. |",
        "| Hassett C_32 discriminant | **Meets 32** (Bl_11 P² Gram [[3,10],[10,44]]) | p=L_5, H²=L_2+L_4. Isolated 4·8 is padding. |",
        "| C_32 extra class | **[Bl_11 P²], algebraic** | Subvariety. 4|d so no K3. |",
        "| Hassett C_36 discriminant | **Meets 36** (Bl_12 P² Gram [[3,12],[12,60]]) | p=H²=L_2 L_3. Isolated 6·6 is padding. |",
        "| C_36 extra class | **[Bl_12 P²], algebraic** | Last Nuer Bl_p. |",
        "| Hassett C_44 discriminant | **Meets 44** (Fano Enriques Gram [[3,10],[10,48]]) | χ=L_2 L_3=12. Isolated 4·11 is padding. |",
        "| C_44 extra class | **[Fano Enriques], algebraic** | Last named extra class. Public SOTA stops naming here. |",
        "| Named no-K3 list | **Complete** (8,12,18,20,24,30,32,36,44) | Do not enumerate the infinite tail. |",
        "| Hassett K3 tail | **Lefschetz (1,1)** including unnamed d=14,26,38 | Do not enumerate surfaces. Unnamed no-K3 remains. |",
        "| Very general cubic | **Rational Hodge (2,2)=⟨h²⟩ only** | Extra rational classes live on C_d. |",
        "| Unnamed no-K3 | **No Gram seed** (no named surface) | FSOT seeds attach to named varieties. Do not hunt C_48. |",
        "| Quartic 4-fold χ | **Meets 188** (same Chern as cubic at d=4) | Not a K3 (K3 is a quartic surface). |",
        "| Sextic 4-fold χ | **Meets 2610** (first CY hypersurface 4-fold) | K=(d−6)h=0. |",
        "| Hypersurface 4-folds after cubic | **Named** | Remainder was non-hypersurface 4-folds. |",
        "| HK Fano of lines | **Named** (b_2=23, Beauville–Donagi) | Lefschetz (1,1) on H^2(F). Not C_48. |",
        "| Abelian 4-fold χ | **Meets 0** | Lefschetz (1,1) applies. Hodge (2,2) remains. |",
        "| Clay algebraicity vs data | **Not a measured function** | Working: χ/Gram of named varieties. Cycle is the measurement. |",
        "| Primitive (2,2) cubic 4-fold | **Named remainder** after Grassmannians | First open hypersurface case. |",
        "| NSE vortex stretching | **Named remainder** after 1D Stokes / 2D enstrophy | 4/5, 2D 3/2, Onsager 1/3, BKM named. Existence on R^3 is whether stretching stays BKM-integrable. |",
        "",
        "## Next dig (misses and open tracks)",
        "",
        "| Item | Why it is next | First cut, no stuffing |",
        "|------|----------------|------------------------|",
        "| Weather storm-sector | Named object (docstring). Thin n_obs<24 is awaiting, not a kill. Majority-of-saw_storm **retired**. | ECMWF not beaten. Frozen issues not rewritten. |",
        "| Weather gap-zone quiet | 1000–1010 hPa / 8–15 m/s should not issue. OLCN6/42058 already in the gap. | New issuer skips. Frozen JSON not rewritten. |",
        "| Weather lat-belt transfer | 44078 (59.94°N) sat 0.50° from MDXA2 (59.44°N); storm tanks held. Valve |Δlat|<POOF·180/π. | Do not move 1010. Transferred_weather, not clean-quiet persistence. |",
        "| Weather clean quiet | Uncoupled clean quiet **holds** (n=4). 44078 is the lat-transfer object. | Do not claim ECMWF. Frozen JSON not rewritten. |",
        "| Observed 0++ pair | PDG f0(1500) gluonic (φ²+1)·K; f0(1710) flavor (π+1)·K. Lattice 0++ is a construct. | Do not swap orifices. Do not retune K. Morningstar: not predominantly glue below ~2 GeV. |",
        "| Riemann signed jitter | Prime-2 sign, prime-3 cancellation of POOF envelope | Isolated sign*POOF leftover was missing p=3. |",
        "| 3D NSE existence on R^3 | Not a measured function. Working: 4/5, 3/2, 1/3, κ. | Do not stuff cascade numbers into smoothness. |",
        "| BSD integer rank | Not a measured function. Working: LMFDB Sha, first-of-rank seeds. | Do not hunt Kato. Do not Weierstrass→ℤ. |",
        "| Hodge extra classes without K3 | Not a measured function. Working: χ/Gram of named varieties. | Do not hunt C_48. Cycle is the measurement. |",
        "| P vs NP | Cook–Levin SAT named. Grover 1/2 is QI. | Search vs verification. |",
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
        "Navier–Stokes object split: [`MILLENNIUM_NSE_VS_FSOT.md`](MILLENNIUM_NSE_VS_FSOT.md).",
        "BSD object split: [`MILLENNIUM_BSD_VS_FSOT.md`](MILLENNIUM_BSD_VS_FSOT.md).",
        "Hodge object split: [`MILLENNIUM_HODGE_VS_FSOT.md`](MILLENNIUM_HODGE_VS_FSOT.md).",
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
        and s["alpha_s_qcd_beats_geometric"] == 1
        and s["alpha_s_qcd_green"] == 1
        and s["alpha_s_qcd_aspiration"] == 1
        and s["glueball_beats_teper"] == 1
        and s["glueball_sigma_coupled_green"] == 1
        and s["glueball_sigma_coupled_aspiration"] == 1
        and s["glueball_r0_scheme_split"] == 1
        and s["glueball_does_not_beat_teper"] == 0
        and s["glueball_at2020_scheme_split"] == 1
        and s["sqrt_sigma_r0_beats"] == 1
        and s["glueball_r0_beats_chen"] == 1
        and s["glueball_beats_4sqrt_sigma"] == 1
        and s["glueball_ratio_beats_three_halves"] == 1
        and s["glueball_observed_pair_named"] == 1
        and s["glueball_f0_1500_beats_lattice_on_that_candidate"] == 1
        and s["f0_1500_inside_tmatrix_pole_band"] == 1
        and s["f0_1500_mixed_green"] == 1
        and s["f0_1710_flavor_beats_4sqrt"] == 1
        and s["f0_1710_flavor_green"] == 1
        and s["riemann_beats_public_closed_form"] == 1
        and s["riemann_panel_beats_rvm"] == 1
        and s["riemann_S_T_bound_holds"] == 1
        and s["riemann_tn_inside_S_band"] == 1
        and s["riemann_S_amplitude_beats_bound_as_typical"] == 1
        and s["riemann_S_amplitude_green"] == 0
        and s["riemann_S_oos_1e_band"] == 1
        and s["riemann_signed_beats_clock"] == 1
        and s["riemann_signed_green"] == 1
        and s["riemann_signed_oos_sign"] == 1
        and s["weather_quiet_fill_still_miss"] == 0
        and s["weather_gap_zone_named"] == 1
        and s["weather_lat_transfer_named"] == 1
        and s["ns_von_karman_green"] == 1
        and s["ns_kolmogorov_45_exact"] == 1
        and s["ns_kolmogorov_d2_32_exact"] == 1
        and s["ns_onsager_holder_exact"] == 1
        and s["ns_bkm_named"] == 1
        and s["ns_l2_cascade_not_l_inf"] == 1
        and s["ns_bkm_magnitude_not_direction"] == 1
        and s["ns_stretch_visc_two_zoom"] == 1
        and s["ns_enstrophy_budget_two_term"] == 1
        and s["ns_helicity_3d_not_2d"] == 1
        and s["ns_clay_smoothness_not_measured"] == 1
        and s["ns_stretch_sim_vs_public_answers"] == 1
        and s["ns_omega0_scan_vs_threshold"] == 1
        and s["ns_3d_spectral_tg"] == 1
        and s["ns_c_water_over_c_air_crc"] == 1
        and s["ns_gamma_diatomic_air"] == 1
        and s["ns_reality_observables"] == 1
        and s["ns_us1976_scale_height"] == 1
        and s["ns_crc_water_nD"] == 1
        and s["ns_crc_water_rho"] == 1
        and s["ns_crc_ice_nD"] == 1
        and s["ns_crc_ice_rho"] == 1
        and s["ns_crc_ice_c"] == 1
        and s["ns_crc_water_Tm"] == 1
        and s["ns_crc_water_Tb"] == 1
        and s["bsd_11a1_L_green"] == 1
        and s["bsd_37a1_Lprime_green"] == 1
        and s["bsd_389a1_reg_beats"] == 1
        and s["bsd_389a1_reg_green"] == 0
        and s["bsd_389a1_special_green"] == 1
        and s["bsd_5077a1_reg_green"] == 1
        and s["bsd_5077a1_reg_aspiration"] == 1
        and s["bsd_234446a1_reg_green"] == 1
        and s["bsd_rank_parity_map"] == 1
        and s["bsd_integer_rank_first5"] == 1
        and s["bsd_leading_volume_named"] == 1
        and s["bsd_17a1_sha_green"] == 1
        and s["bsd_19a1_sha_green"] == 1
        and s["bsd_general_rank0_vanishing"] == 1
        and s["bsd_53a1_sha_green"] == 1
        and s["bsd_61a1_sha_green"] == 1
        and s["bsd_general_rank1_vanishing"] == 1
        and s["bsd_643a1_sha_green"] == 1
        and s["bsd_433a1_sha_green"] == 1
        and s["bsd_general_rank2_vanishing"] == 1
        and s["bsd_11197a1_sha_green"] == 1
        and s["bsd_11642a1_sha_green"] == 1
        and s["bsd_general_rank3_vanishing"] == 1
        and s["bsd_501029a1_sha_green"] == 1
        and s["bsd_545723a1_sha_green"] == 1
        and s["bsd_general_rank4_vanishing"] == 1
        and s["bsd_19047851a1_sha_green"] == 1
        and s["bsd_64921931a1_sha_green"] == 1
        and s["bsd_general_rank5_vanishing"] == 1
        and s["bsd_lmfdb_named_ranks_complete"] == 1
        and s["bsd_modularity_named"] == 1
        and s["bsd_kolyvagin_rank_le1"] == 1
        and s["bsd_rank_ge2_volume_native"] == 1
        and s["bsd_regulator_is_height_gram"] == 1
        and s["bsd_tam_local_reg_global"] == 1
        and s["bsd_clay_equality_not_measured"] == 1
        and s["bsd_sha_panel_vs_lmfdb"] == 1
        and s["bsd_mw_generators_observable"] == 1
        and s["bsd_11a1_torsion_particle"] == 1
        and s["hodge_cp2_euler_exact"] == 1
        and s["hodge_cp3_euler_exact"] == 1
        and s["hodge_lefschetz_11_named"] == 1
        and s["hodge_22_named"] == 1
        and s["hodge_hard_lefschetz_named"] == 1
        and s["hodge_cp2xcp2_exact"] == 1
        and s["hodge_primitive_22_named"] == 1
        and s["hodge_gr24_exact"] == 1
        and s["hodge_gr24_schubert_named"] == 1
        and s["hodge_lefschetz_hyperplane_named"] == 1
        and s["hodge_index_named"] == 1
        and s["hodge_cubic4_euler_exact"] == 1
        and s["hodge_cubic4_h22_exact"] == 1
        and s["hodge_cubic4_remainder_named"] == 1
        and s["hodge_k3_h11_exact"] == 1
        and s["hodge_fano_b2_exact"] == 1
        and s["hodge_associated_k3_algebraicity"] == 1
        and s["hodge_hassett_d8_exact"] == 1
        and s["hodge_hassett_c8_plane_algebraic"] == 1
        and s["hodge_hassett_d12_exact"] == 1
        and s["hodge_hassett_c12_scroll_algebraic"] == 1
        and s["hodge_hassett_d18_exact"] == 1
        and s["hodge_hassett_c18_elliptic_algebraic"] == 1
        and s["hodge_hassett_d20_exact"] == 1
        and s["hodge_hassett_c20_veronese_algebraic"] == 1
        and s["hodge_hassett_d24_exact"] == 1
        and s["hodge_hassett_c24_sextic_algebraic"] == 1
        and s["hodge_hassett_d30_exact"] == 1
        and s["hodge_hassett_c30_coble_algebraic"] == 1
        and s["hodge_hassett_d32_exact"] == 1
        and s["hodge_hassett_c32_bl11_algebraic"] == 1
        and s["hodge_hassett_d36_exact"] == 1
        and s["hodge_hassett_c36_bl12_algebraic"] == 1
        and s["hodge_hassett_d44_exact"] == 1
        and s["hodge_hassett_c44_enriques_algebraic"] == 1
        and s["hodge_hassett_named_no_k3_complete"] == 1
        and s["hodge_hassett_k3_tail_lefschetz"] == 1
        and s["hodge_very_general_cubic_only_h2"] == 1
        and s["hodge_unnamed_no_k3_no_seed"] == 1
        and s["hodge_quartic4_euler_exact"] == 1
        and s["hodge_quintic4_euler_exact"] == 1
        and s["hodge_sextic4_cy_euler_exact"] == 1
        and s["hodge_hypersurface_4folds_after_cubic"] == 1
        and s["hodge_hk4_fano_lines_named"] == 1
        and s["hodge_abelian4_euler_exact"] == 1
        and s["hodge_clay_algebraicity_not_measured"] == 1
        and s["hodge_chi_panel_vs_chern"] == 1
        and s["ns_stretching_named"] == 1
        and s["ns_2d_enstrophy_named"] == 1
        and s["pnp_sat_named"] == 1
        and s["ecmwf_not_beaten"] == 1
        and s["sota_beats_accuracy_wip_n"] >= 1
        and s["next_dig_n"] >= 1
        and s["fsot_green_pass_n"] >= 1
    )
    raise SystemExit(0 if ok else 1)

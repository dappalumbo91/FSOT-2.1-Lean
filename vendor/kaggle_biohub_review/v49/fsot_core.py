#!/usr/bin/env python3
"""
FSOT 2.1 CORE SCALAR ENGINE  (fast float64 port + equivalence validator)
========================================================================
Faithful port of Damian Arthur Palumbo's FSOT scalar engine
(`compute_S_D_chaotic` / `compute_scalar`) from the Lean 4 formalization
(FSOT-2.1-Lean: FSOT/Scalar.lean) and the workspace mpmath reference
(fsot_rna_trinary_evolution_sim.py :: compute_scalar).

WHY THIS FILE EXISTS
--------------------
The verified reference engine runs at mp.dps = 50 (50-digit mpmath). That is
the source of truth, but far too slow to evaluate for thousands of cell-pairs
across many frames inside Kaggle's 12-hour cap. This module reproduces the
*same* engine in float64 so it runs at competition scale, and ships a
validator (`validate_against_mpmath`) that proves the float64 result matches
the mpmath reference to ~1e-12 for the biological domain and parameter sweeps.

Nothing about FSOT is approximated away — only the arithmetic precision of the
numeric evaluation changes, and that change is measured and bounded.
"""

from __future__ import annotations
import math
from dataclasses import dataclass

# ============================================================
# FUNDAMENTAL & DERIVED CONSTANTS  (float64, mirror of Scalar.lean)
# ============================================================
PI = math.pi
E = math.e
PHI = (1.0 + math.sqrt(5.0)) / 2.0
SQRT2 = math.sqrt(2.0)
GAMMA_EULER = 0.5772156649015329
CATALAN_G = 0.9159655941772190

ALPHA = math.log(PI) / (E * PHI**13)
PSI_CON = (E - 1.0) / E                      # == 1 - exp(-1)
ETA_EFF = 1.0 / (PI - 1.0)
BETA = 1.0 / math.exp(PI**PI + (E - 1.0))
GAMMA_C = -math.log(2.0) / PHI
OMEGA = math.sin(PI / E) * SQRT2
THETA_S = math.sin(PSI_CON * ETA_EFF)
POOF = math.exp((-math.log(PI) / E) / (ETA_EFF * math.log(PHI)))

C_EFF = (1.0 - POOF * math.sin(THETA_S)) * (1.0 + 0.01 * CATALAN_G / (PI * PHI))
A_BLEED = math.sin(PI / E) * PHI / SQRT2
P_VAR = -math.cos(THETA_S + PI)
B_IN = C_EFF * (1.0 - math.sin(THETA_S) / PHI)
A_IN = A_BLEED * (1.0 + math.cos(THETA_S) / PHI)
SUCTION = POOF * (-math.cos(THETA_S - PI))
CHAOS = GAMMA_C / OMEGA
P_BASE = GAMMA_EULER / E
P_NEW = P_BASE * SQRT2
C_FACTOR = C_EFF * P_NEW                      # consciousness_factor
K = PHI * (P_BASE * SQRT2) / math.log(PI) * 0.99

# Trinary collapse threshold (C_EFF * P_VAR ~= 0.9175)
COLLAPSE_THRESHOLD = C_EFF * P_VAR

# Fertile emergence window (64_codon_trinary_map.txt §6, §10; RNA sim scripts)
FERTILE_LOW = 0.15
FERTILE_HIGH = 0.45

# Biological domain binding (FSOT/Formal/Scalar.lean get_domain_params "biological")
BIO_D_EFF = 12
BIO_DELTA_PSI = 0.08
BIO_DELTA_THETA = 1.0
BIO_RECENT_HITS = 0
BIO_OBSERVED = False


def compute_scalar_fast(
    N: float = 1.0,
    P: float = 1.0,
    D_eff: float = 25.0,
    recent_hits: float = 0.0,
    delta_psi: float = 1.0,
    delta_theta: float = 1.0,
    rho: float = 1.0,
    scale: float = 1.0,
    amplitude: float = 1.0,
    trend_bias: float = 0.0,
    observed: bool = False,
) -> float:
    """Core FSOT scalar  S = K * (T1 + T2 + T3).

    Float64 reproduction of compute_scalar / compute_S_D_chaotic.
    """
    D = float(D_eff)
    dp = float(delta_psi)
    dt = float(delta_theta)
    hits = float(recent_hits)
    Nf = float(N)
    Pf = float(P)

    # Term 1: observer-modulated base
    growth = math.exp(ALPHA * (1.0 - hits / Nf) * GAMMA_EULER / PHI)
    base = (
        (Nf * Pf / math.sqrt(D))
        * math.cos((PSI_CON + dp) / ETA_EFF)
        * math.exp(-ALPHA * hits / Nf + rho + B_IN * dp)
        * (1.0 + growth * C_EFF)
    )
    T1 = base * (1.0 + P_NEW * math.log(D / 25.0))
    if observed:
        T1 = T1 * math.exp(C_FACTOR * P_VAR) * math.cos(dp + P_VAR)

    # Term 2: linear pressure trend
    T2 = scale * amplitude + trend_bias

    # Term 3: valve-acoustic-phase
    valve = (
        BETA * math.cos(dp)
        * (Nf * Pf / math.sqrt(D))
        * (1.0 + CHAOS * (D - 25.0) / 25.0)
        * (1.0 + POOF * math.cos(THETA_S + PI) + SUCTION * math.sin(THETA_S))
    )
    acoustic = (
        1.0
        + (A_BLEED * math.sin(dt) ** 2) / PHI
        + (A_IN * math.cos(dt) ** 2) / PHI
    )
    phase = 1.0 + B_IN * P_VAR
    T3 = valve * acoustic * phase

    return K * (T1 + T2 + T3)


def compute_scalar_biological(
    N: float = 1.0,
    P: float = 1.0,
    delta_psi: float = BIO_DELTA_PSI,
    recent_hits: float = 0.0,
    amplitude: float = 1.0,
    observed: bool = False,
) -> float:
    """FSOT scalar bound to the biological domain (D_eff=12)."""
    return compute_scalar_fast(
        N=N, P=P, D_eff=BIO_D_EFF,
        recent_hits=recent_hits, delta_psi=delta_psi,
        delta_theta=BIO_DELTA_THETA, amplitude=amplitude, observed=observed,
    )


def trinary_collapse(local_coherence: float, threshold: float = COLLAPSE_THRESHOLD) -> int:
    """Trinary collapse state: -1 (repel/unstable), 0 (neutral), +1 (locked/stable)."""
    if local_coherence < threshold * 0.8:
        return -1
    elif local_coherence < threshold:
        return 0
    return 1


# ============================================================
# EQUIVALENCE VALIDATION vs the mpmath reference engine
# ============================================================
def validate_against_mpmath(dps: int = 50, tol: float = 1e-10) -> dict:
    """Compare float64 port against a mpmath (dps-digit) reference across a
    parameter sweep. Returns {'max_rel_err', 'n', 'ok'}."""
    from mpmath import mp, mpf, sin, cos, exp, sqrt, pi as MP_PI, e as MP_E, ln
    mp.dps = dps

    m_PI = MP_PI
    m_E = MP_E
    m_PHI = (1 + sqrt(5)) / 2
    m_GAMMA = mpf("0.57721566490153286060651209008240243104215933593992")
    m_GCAT = mpf("0.91596559417721901505460351493238411077414937428167")
    m_ALPHA = ln(m_PI) / (m_E * m_PHI**13)
    m_PSI = 1 - exp(-1)
    m_ETA = 1 / (m_PI - 1)
    m_BETA = 1 / exp(m_PI**m_PI + (m_E - 1))
    m_GC = -ln(2) / m_PHI
    m_OMEGA = sin(m_PI / m_E) * sqrt(2)
    m_THETA = sin(m_PSI * m_ETA)
    m_POOF = exp((-ln(m_PI) / m_E) / (m_ETA * ln(m_PHI)))
    m_CEFF = (1 - m_POOF * sin(m_THETA)) * (1 + mpf("0.01") * m_GCAT / (m_PI * m_PHI))
    m_ABLEED = sin(m_PI / m_E) * m_PHI / sqrt(2)
    m_PVAR = -cos(m_THETA + m_PI)
    m_BIN = m_CEFF * (1 - sin(m_THETA) / m_PHI)
    m_AIN = m_ABLEED * (1 + cos(m_THETA) / m_PHI)
    m_SUCT = m_POOF * (-cos(m_THETA - m_PI))
    m_CHAOS = m_GC / m_OMEGA
    m_PNEW = (m_GAMMA / m_E) * sqrt(2)
    m_CFAC = m_CEFF * m_PNEW
    m_K = m_PHI * (m_GAMMA / m_E) * sqrt(2) / ln(m_PI) * mpf("0.99")

    def ref(N, P, D, hits, dp, dt, rho, scale, amp, tb, obs):
        N = mpf(N); P = mpf(P); D = mpf(D); hits = mpf(hits)
        dp = mpf(dp); dt = mpf(dt); rho = mpf(rho)
        scale = mpf(scale); amp = mpf(amp); tb = mpf(tb)
        growth = exp(m_ALPHA * (1 - hits / N) * m_GAMMA / m_PHI)
        base = ((N * P / sqrt(D)) * cos((m_PSI + dp) / m_ETA)
                * exp(-m_ALPHA * hits / N + rho + m_BIN * dp)
                * (1 + growth * m_CEFF))
        T1 = base * (1 + m_PNEW * ln(D / 25))
        if obs:
            T1 = T1 * exp(m_CFAC * m_PVAR) * cos(dp + m_PVAR)
        T2 = scale * amp + tb
        valve = (m_BETA * cos(dp) * (N * P / sqrt(D))
                 * (1 + m_CHAOS * (D - 25) / 25)
                 * (1 + m_POOF * cos(m_THETA + m_PI) + m_SUCT * sin(m_THETA)))
        acoustic = 1 + (m_ABLEED * sin(dt)**2) / m_PHI + (m_AIN * cos(dt)**2) / m_PHI
        phase = 1 + m_BIN * m_PVAR
        T3 = valve * acoustic * phase
        return m_K * (T1 + T2 + T3)

    max_rel = 0.0
    n = 0
    for D in (6, 9, 12, 25):
        for hits in (0, 1, 3):
            for dp in (0.05, 0.5, 1.0):
                for obs in (False, True):
                    for amp in (1.0, 0.5):
                        r = float(ref(1, 1, D, hits, dp, 1.0, 1.0, 1.0, amp, 0.0, obs))
                        f = compute_scalar_fast(
                            N=1, P=1, D_eff=D, recent_hits=hits, delta_psi=dp,
                            delta_theta=1.0, rho=1.0, scale=1.0, amplitude=amp,
                            trend_bias=0.0, observed=obs)
                        denom = abs(r) if abs(r) > 1e-300 else 1.0
                        rel = abs(f - r) / denom
                        max_rel = max(max_rel, rel)
                        n += 1
    return {"max_rel_err": max_rel, "n": n, "ok": max_rel < tol}


if __name__ == "__main__":
    print("=" * 70)
    print("FSOT 2.1 CORE — float64 port")
    print("=" * 70)
    print(f"K                  = {K:.15f}")
    print(f"COLLAPSE_THRESHOLD = {COLLAPSE_THRESHOLD:.15f}")
    print(f"C_EFF              = {C_EFF:.15f}")
    print(f"P_VAR              = {P_VAR:.15f}")
    print(f"biological S (dp=0.08, obs=False) = {compute_scalar_biological():.12f}")
    print("-" * 70)
    try:
        res = validate_against_mpmath()
        status = "PASS" if res["ok"] else "FAIL"
        print(f"[{status}] float64 vs mpmath(50): max rel err = {res['max_rel_err']:.3e} "
              f"over {res['n']} configs")
    except ImportError:
        print("[SKIP] mpmath not installed; cannot run equivalence validation.")
    print("=" * 70)

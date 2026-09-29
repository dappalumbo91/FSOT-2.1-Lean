#!/usr/bin/env python3
"""Reduce the GR weak field and the SM tree mass relation to the scalar engine.

Nothing here is a new coefficient. g_00 is the factor already multiplying
term 1. The Schwarzschild relation uses the rest unit K and the acoustic
cone already in the law. The W/Z relation is the on-shell identity on those
same constants.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from mpmath import log, mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))
import fsot_compute as F  # noqa: E402
from fsot_correspondence_limit import terms  # noqa: E402
from fsot_seed_flavor import (  # noqa: E402
    seed_m_W_GeV,
    seed_m_Z_GeV,
    seed_sin2_theta_W_onshell,
    seed_unitarity_triangle,
)


def g_00(dimension: mpf) -> mpf:
    """Time-time metric factor inside T1. Minkowski when D = 25."""
    return -(1 + F.P_NEW * log(dimension / 25))


def newton_potential(dimension: mpf) -> mpf:
    """g_00 = -(1 + 2 Φ). Φ vanishes at the home dimension."""
    return -(g_00(dimension) + 1) / 2


def acoustic_c2() -> mpf:
    return F.C_EFF / F.PHI


def schwarzschild_radius(rest_mass: mpf) -> mpf:
    """r_s = 2 M / c_ac² with c_ac² = C_eff/φ and M the rest unit."""
    return 2 * rest_mass / acoustic_c2()


def main() -> int:
    home = mpf(25)
    if g_00(home) != -1:
        raise SystemExit(f"Minkowski limit failed: g_00(25)={g_00(home)}")
    if newton_potential(home) != 0:
        raise SystemExit("Newtonian potential is not zero at D=25")

    # First-order slope: d g_00 / d ln(D/25) = -P_new, read off the factor.
    near = mpf(25) * mpf("1.0000001")
    strain = log(near / 25)
    slope = (g_00(near) - g_00(home)) / strain
    if abs(slope + F.P_NEW) > mpf("1e-20"):
        raise SystemExit(f"weak-field slope {slope} is not -P_new")

    # T1 really is the bare amplitude times -g_00.
    chem = F.DOMAINS["Chemistry"]
    for dimension, observed, hits, look in (
        (mpf(chem.D_eff), bool(chem.observed), mpf(chem.hits), chem.delta_psi),
        (mpf(25), False, mpf(0), mpf(1)),
        (mpf(26), False, mpf(0), mpf(1)),
    ):
        sample = F.ScalarInput(
            D_eff=dimension,
            delta_psi=look,
            recent_hits=hits,
            observed=observed,
        )
        t1, t2, t3, scalar = terms(sample)
        bare = t1 / (-g_00(dimension))
        rebuilt = bare * (1 + F.P_NEW * log(dimension / 25))
        if abs(rebuilt - t1) > mpf("1e-18"):
            raise SystemExit(f"T1 is not bare*(-g_00) at D={dimension}")
        gamma = (t1 + t2 + t3) / t2
        if abs(scalar - F.K * t2 * gamma) > mpf("1e-18"):
            raise SystemExit("S is not (K T2) gamma")

    rest = F.K  # T2 = 1
    radius = schwarzschild_radius(rest)
    if abs(radius * acoustic_c2() / (2 * rest) - 1) > mpf("1e-18"):
        raise SystemExit("Schwarzschild identity failed")

    mw = seed_m_W_GeV()
    mz = seed_m_Z_GeV()
    s2 = seed_sin2_theta_W_onshell()
    if abs(mw**2 / mz**2 - (1.0 - s2)) > 1e-12:
        raise SystemExit("on-shell W/Z relation failed")

    angles = seed_unitarity_triangle()
    angle_sum = angles["alpha_rad"] + angles["beta_rad"] + angles["gamma_rad"]
    if abs(angle_sum - math.pi) > 1e-12:
        raise SystemExit(f"CKM angle sum {angle_sum} is not pi")

    print(f"g_00(D=25) = {g_00(home)}")
    print(f"weak-field slope = {-F.P_NEW}")
    print(f"acoustic c^2 = {acoustic_c2()}")
    print(f"r_s(M=K) = {radius}")
    print(f"m_W^2/m_Z^2 = {mw**2 / mz**2}")
    print(f"1-sin^2 theta_W = {1.0 - s2}")
    print(f"alpha+beta+gamma = {angle_sum}")
    print("scalar_reduction_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

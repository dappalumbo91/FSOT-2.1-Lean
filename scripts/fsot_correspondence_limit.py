#!/usr/bin/env python3
"""FSOT rest split. The same role E = gamma m c^2 plays for special relativity.

S = K (T1 + T2 + T3) is the live scalar engine. At the engine defaults
T2 = 1, and the valve T3 is O(beta) with beta = exp(-(pi^pi + e - 1)).
The working law on every catalog domain is therefore

    S = K (T1 + 1)

K * T2 is the rest unit. T1 is the fluid dressing. Their ratio is

    gamma_FSOT = (T1 + T2 + T3) / T2
    S = (K T2) * gamma_FSOT

At the home dimension D = 25 the compactification strain ln(D/25) and the
valve strain (D-25)/25 are identically zero. That is the unstrained fluid,
the same kind of limit as v/c -> 0. No new coefficient. vendor/fsot_compute.py
is not rewritten.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import cos, exp, log, mpf, sin, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402


def terms(s: F.ScalarInput) -> tuple[mpf, mpf, mpf, mpf]:
    growth = exp(s.alpha * (1 - s.recent_hits / s.N) * F.GAMMA / F.PHI)
    base = (
        (s.N * s.P / sqrt(s.D_eff))
        * cos((s.psi_con + s.delta_psi) / F.ETA_EFF)
        * exp(-s.alpha * s.recent_hits / s.N + s.rho + s.B_in * s.delta_psi)
        * (1 + growth * s.C_eff)
    )
    t1 = base * (1 + s.P_new * log(s.D_eff / 25))
    if s.observed:
        t1 = t1 * exp(F.C_FACTOR * s.P_var) * cos(s.delta_psi + s.P_var)
    t2 = s.scale * s.amplitude + s.trend_bias
    valve = (
        s.beta
        * cos(s.delta_psi)
        * (s.N * s.P / sqrt(s.D_eff))
        * (1 + s.chaos * (s.D_eff - 25) / 25)
        * (1 + s.poof * cos(s.theta_s + F.PI) + s.suction * sin(s.theta_s))
    )
    acoustic = (
        1
        + (s.A_bleed * sin(s.delta_theta) ** 2) / F.PHI
        + (s.A_in * cos(s.delta_theta) ** 2) / F.PHI
    )
    phase = 1 + s.B_in * s.P_var
    t3 = valve * acoustic * phase
    return t1, t2, t3, F.K * (t1 + t2 + t3)


def main() -> int:
    home = F.ScalarInput(D_eff=mpf(25), recent_hits=mpf(0), observed=False)
    t1, t2, t3, scalar = terms(home)
    direct = F.compute_scalar(home)
    if abs(scalar - direct) > mpf("1e-30"):
        raise SystemExit(f"term split disagrees with compute_scalar: {scalar} vs {direct}")
    if t2 != 1:
        raise SystemExit(f"rest unit T2 is {t2}, expected 1")
    if abs(t3) > mpf("1e-15"):
        raise SystemExit(f"valve is not silent: T3={t3}")
    if abs(log(home.D_eff / 25)) != 0 or (home.D_eff - 25) != 0:
        raise SystemExit("home dimension still carries compactification strain")
    if abs(scalar - F.S_COSM) > mpf("1e-12"):
        raise SystemExit(f"home scalar {scalar} is not S_COSM {F.S_COSM}")

    chem = F.DOMAINS["Chemistry"]
    chem_in = F.ScalarInput(
        D_eff=mpf(chem.D_eff),
        delta_psi=chem.delta_psi,
        recent_hits=mpf(chem.hits),
        observed=bool(chem.observed),
    )
    c1, c2, c3, chem_s = terms(chem_in)
    if abs(chem_s - F.S_CHEM) > mpf("1e-12"):
        raise SystemExit(f"chemistry scalar {chem_s} is not S_CHEM {F.S_CHEM}")
    gamma = (c1 + c2 + c3) / c2
    rest = F.K * c2
    print(f"rest_unit K*T2 = {rest}")
    print(f"chemistry gamma_FSOT = {gamma}")
    print(f"chemistry S = {chem_s}")
    print(f"home S = S_COSM = {scalar}")
    print(f"valve |T3| home = {abs(t3)}")
    print("correspondence_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

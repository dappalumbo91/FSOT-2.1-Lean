#!/usr/bin/env python3
"""Check m_pi/m_p as the charged-pion leaf divided by the proton-mass leaf.

Both masses are in MeV. The pion is the PDG mass 139.57039 ± 0.00018 MeV.
The proton is the CODATA kilogram 1.67262192595(52)e-27 converted with c and e.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, power, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

C = mpf("299792458")
H = mpf("6.62607015e-34")
NU = mpf("9192631770")
CHARGE = mpf("1.602176634e-19")
PI_MEV = mpf("139.57039")
PI_BAR = mpf("0.00018")
M_P = mpf("1.67262192595e-27")
M_P_BAR = mpf("5.2e-37")


def mev(mass_kg):
    return mass_kg * C**2 / CHARGE / mpf("1e6")


def main() -> int:
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    exponent = (
        power(F.E, F.PI)
        + (F.C_FACTOR * F.K * log(2)) ** 2
        + F.G_CAT * F.P_NEW * F.PSI_CON
        - alpha**5 * F.PHI**2 / log(2) ** 2
    )
    mass_e = H * NU / C**2 * exp(exponent)
    proton_ratio = 6 * F.PI**5 + log(2) / F.E**3 + alpha**2 * (1 + F.PSI_CON / F.E**3)
    proton_mev = mev(proton_ratio * mass_e)
    pion_mev = power(F.THETA_S, -4) - F.THETA_S**2 + alpha / (F.PI - 1)
    ratio = pion_mev / proton_mev
    proton_meas = mev(M_P)
    proton_bar = mev(M_P_BAR)
    measured = PI_MEV / proton_meas
    bar = sqrt((PI_BAR / proton_meas) ** 2 + (PI_MEV * proton_bar / proton_meas**2) ** 2)
    gap = ratio - measured
    print(f"pion_MeV={pion_mev}")
    print(f"proton_MeV={proton_mev}")
    print(f"ratio={ratio}")
    print(f"pdg={measured}")
    print(f"bar={bar}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / bar} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

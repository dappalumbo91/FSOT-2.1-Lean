#!/usr/bin/env python3
"""Check the neutron as the proton mass times one plus a small excess.

The excess is e*(POOF*SUCTION)^2 minus B_in/(P_new*e^13). This script
only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

RATIO = mpf("1.00137841946")
RATIO_BAR = mpf("4.0e-10")
M_N = mpf("1.67492750056e-27")
M_N_BAR = mpf("8.5e-37")
C = mpf("299792458")
H = mpf("6.62607015e-34")
NU = mpf("9192631770")


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
    proton_ratio = (
        6 * F.PI**5 + log(2) / F.E**3 + alpha**2 * (1 + F.PSI_CON / F.E**3)
    )
    delta = F.E * (F.POOF * F.SUCTION) ** 2 - F.B_IN / (F.P_NEW * F.E**13)
    ratio = 1 + delta
    mass = proton_ratio * mass_e * ratio
    print(f"delta={delta}")
    rd = ratio - RATIO
    print(f"ratio_sigmas={abs(rd) / RATIO_BAR} side={'high' if rd > 0 else 'low'}")
    md = mass - M_N
    print(f"mass={mass}")
    print(f"mass_sigmas={abs(md) / M_N_BAR} side={'high' if md > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

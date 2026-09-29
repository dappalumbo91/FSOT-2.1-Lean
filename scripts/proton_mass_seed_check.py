#!/usr/bin/env python3
"""Check the proton mass as the electron mass times a seed ratio.

ratio/pi^5 is 6.000113, so the leading piece is 6*pi^5. The corrections
are ln2/e^3 and alpha^2*(1 + psi_con/e^3). This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

RATIO = mpf("1836.152673426")
RATIO_BAR = mpf("3.2e-8")
M_P = mpf("1.67262192595e-27")
M_P_BAR = mpf("5.2e-37")
MU_N = mpf("5.0507837393e-27")
MU_BAR = mpf("1.6e-36")
C = mpf("299792458")
H = mpf("6.62607015e-34")
NU = mpf("9192631770")
CHARGE = mpf("1.602176634e-19")


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
    ratio = 6 * F.PI**5 + log(2) / F.E**3 + alpha**2 * (1 + F.PSI_CON / F.E**3)
    mass_p = ratio * mass_e
    magneton = CHARGE * H / (4 * F.PI * mass_p)
    print(f"6*pi^5={6 * F.PI**5}")
    print(f"ratio={ratio}")
    rd = ratio - RATIO
    print(f"ratio_sigmas={abs(rd) / RATIO_BAR} side={'high' if rd > 0 else 'low'}")
    md = mass_p - M_P
    print(f"mass={mass_p}")
    print(f"mass_sigmas={abs(md) / M_P_BAR} side={'high' if md > 0 else 'low'}")
    nd = magneton - MU_N
    print(f"nuclear_magneton={magneton}")
    print(f"magneton_sigmas={abs(nd) / MU_BAR} side={'high' if nd > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

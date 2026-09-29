#!/usr/bin/env python3
"""Check the atomic mass constant and the carbon-12 molar mass.

u/m_e = 6*pi^5 - pi*phi^3 + gamma/e^2 + alpha*ln2/e^3 + K*pi/e^12.
gamma is Euler's constant. The molar mass is 12*N_A*u.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

RATIO = 1 / mpf("5.485799090441e-4")
RATIO_BAR = RATIO * mpf("1.8e-11")
U = mpf("1.66053906892e-27")
U_BAR = mpf("5.2e-37")
M12 = mpf("0.0120000000126")
M12_BAR = mpf("3.7e-12")
NA = mpf("6.02214076e23")
C = mpf("299792458")
H = mpf("6.62607015e-34")
NU = mpf("9192631770")


def main() -> int:
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    mass_e = H * NU / C**2 * exp(
        power(F.E, F.PI)
        + (F.C_FACTOR * F.K * log(2)) ** 2
        + F.G_CAT * F.P_NEW * F.PSI_CON
        - alpha**5 * F.PHI**2 / log(2) ** 2
    )
    ratio = (
        6 * F.PI**5
        - F.PI * F.PHI**3
        + F.GAMMA / F.E**2
        + alpha * log(2) / F.E**3
        + F.K * F.PI / F.E**12
    )
    unit = ratio * mass_e
    molar = 12 * NA * unit
    print(f"ratio={ratio}")
    rd = ratio - RATIO
    print(f"ratio_sigmas={abs(rd) / RATIO_BAR} side={'high' if rd > 0 else 'low'}")
    ud = unit - U
    print(f"u={unit}")
    print(f"u_sigmas={abs(ud) / U_BAR} side={'high' if ud > 0 else 'low'}")
    md = molar - M12
    print(f"molar={molar}")
    print(f"molar_sigmas={abs(md) / M12_BAR} side={'high' if md > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

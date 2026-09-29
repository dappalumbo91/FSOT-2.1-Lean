#!/usr/bin/env python3
"""Check the muon mass as the electron mass times a seed ratio.

The ratio is the wave piece (pi^3 - G_Catalan^2)*phi^4 minus
e*(POOF*SUCTION)^2*ln2*P_new/P_base. P_new/P_base is sqrt(2).
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

RATIO = mpf("206.7682827")
RATIO_BAR = mpf("4.6e-6")
MASS = mpf("1.883531627e-28")
MASS_BAR = mpf("4.2e-36")
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
    wave = (F.PI**3 - F.G_CAT**2) * F.PHI**4
    corr = F.E * (F.POOF * F.SUCTION) ** 2 * log(2) * F.P_NEW / F.P_BASE
    ratio = wave - corr
    mass = ratio * mass_e
    print(f"wave={wave}")
    print(f"correction={corr}")
    print(f"ratio={ratio}")
    rd = ratio - RATIO
    print(f"ratio_sigmas={abs(rd) / RATIO_BAR} side={'high' if rd > 0 else 'low'}")
    md = mass - MASS
    print(f"mass={mass}")
    print(f"mass_sigmas={abs(md) / MASS_BAR} side={'high' if md > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

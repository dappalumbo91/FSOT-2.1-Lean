#!/usr/bin/env python3
"""Check the tau mass as the electron mass times the wave ratio.

The ratio is pi^7*ln(pi) + e^3, the m_tau/m_e formula already in the engine.
The electron mass is the adopted kilogram leaf. The MeV value is m*c^2/e.
PDG 2024 gives 1776.93 ± 0.09 MeV.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

C = mpf("299792458")
H = mpf("6.62607015e-34")
E_SI = mpf("1.602176634e-19")
NU = mpf("9192631770")
PDG_2024 = mpf("1776.93")
BAR_2024 = mpf("0.09")


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
    mev = mass_e * C**2 / E_SI / mpf("1e6")
    ratio = F.PI**7 * log(F.PI) + F.E**3
    mass = ratio * mev
    gap = mass - PDG_2024
    print(f"m_e_MeV={mev}")
    print(f"ratio={ratio}")
    print(f"tau_MeV={mass}")
    print(f"gap_MeV={gap}")
    print(f"sigmas={abs(gap) / BAR_2024} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

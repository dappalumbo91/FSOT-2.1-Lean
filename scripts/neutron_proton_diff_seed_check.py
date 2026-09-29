#!/usr/bin/env python3
"""Check the neutron-proton mass difference as the two mass leaves subtracted.

Both masses are in MeV. CODATA 2022 gives 1.29333251(38) MeV. The (38)
is an absolute uncertainty of 0.00000038 MeV. The mass leaves are unchanged.
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
NU = mpf("9192631770")
CHARGE = mpf("1.602176634e-19")
MEASURED = mpf("1.29333251")
BAR = mpf("0.00000038")


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
    proton_kg = proton_ratio * mass_e
    delta = F.E * (F.POOF * F.SUCTION) ** 2 - F.B_IN / (F.P_NEW * F.E**13)
    neutron_kg = proton_kg * (1 + delta)
    proton_mev = mev(proton_kg)
    neutron_mev = mev(neutron_kg)
    difference = neutron_mev - proton_mev
    gap = difference - MEASURED
    print(f"proton_MeV={proton_mev}")
    print(f"neutron_MeV={neutron_mev}")
    print(f"difference={difference}")
    print(f"codata={MEASURED}")
    print(f"bar={BAR}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / BAR} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

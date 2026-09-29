#!/usr/bin/env python3
"""Check m_tau/m_e as pi^7*ln(pi) + e^3.

PDG 2024 gives 1776.93 ± 0.09 MeV. The electron is the CODATA kilogram
9.1093837139(28)e-31, converted with c and e. The 2025 listing still
averages the same tau mass. CODATA's own ratio 3477.23 ± 0.23 is the
older tau and is printed beside the adopted ratio. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import log, mpf, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

C = mpf("299792458")
CHARGE = mpf("1.602176634e-19")
M_E = mpf("9.1093837139e-31")
M_E_BAR = mpf("2.8e-40")
TAU = mpf("1776.93")
TAU_BAR = mpf("0.09")
CODATA_RATIO = mpf("3477.23")
CODATA_BAR = mpf("0.23")


def mev(mass_kg):
    return mass_kg * C**2 / CHARGE / mpf("1e6")


def main() -> int:
    ratio = F.PI**7 * log(F.PI) + F.E**3
    electron = mev(M_E)
    electron_bar = mev(M_E_BAR)
    pdg = TAU / electron
    bar = pdg * sqrt((TAU_BAR / TAU) ** 2 + (electron_bar / electron) ** 2)
    gap = ratio - pdg
    codata_gap = ratio - CODATA_RATIO
    print(f"ratio={ratio}")
    print(f"electron_MeV={electron}")
    print(f"pdg={pdg}")
    print(f"bar={bar}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / bar} side={'high' if gap > 0 else 'low'}")
    print(f"codata_ratio={CODATA_RATIO}")
    print(
        f"codata_sigmas={abs(codata_gap) / CODATA_BAR} "
        f"side={'high' if codata_gap > 0 else 'low'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

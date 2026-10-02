#!/usr/bin/env python3
"""Check the atmospheric splitting (G_Catalan*SUCTION)^3 * (1+(POOF*SUCTION)^2).

The seed file calls this reading dm2_31. OD-1 (2026-10-02) compares it with
Delta m^2_31 = 2.5303e-3 (NO, rpp2024-sum-leptons), not the old 0.002453 anchor.
PDG 2026 review Table 14.7 quotes it as Delta m^2_32. The adopted bar is
the NuFIT global fit that includes Super-Kamiokande and IceCube atmospheric
data, normal ordering, which is that fit's best ordering:
2.438 +0.021 -0.019, in units of 10^-3 eV^2. Delta m^2_31 is this splitting
plus the solar splitting, and it is printed beside the adopted bar.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

# Table 14.7, normal ordering, units eV^2.
ADOPTED = mpf("2.438e-3")
ADOPTED_HI = mpf("0.021e-3")
ADOPTED_LO = mpf("0.019e-3")
OTHER_GLOBAL = mpf("2.458e-3")
OTHER_BAR = mpf("0.020e-3")
PARTIAL = mpf("2.420e-3")
PARTIAL_BAR = mpf("0.020e-3")
LISTING = mpf("2.451e-3")
LISTING_BAR = mpf("0.026e-3")
# NuFIT 6.0 with atmospheric data, Delta m^2_3l for normal ordering.
DM31 = mpf("2.513e-3")
DM31_HI = mpf("0.021e-3")
DM31_LO = mpf("0.019e-3")
SOLAR_FIT = mpf("7.49e-5")


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred, meas, bar) -> None:
    gap = pred - meas
    print(f"{label}={meas}")
    print(f"{label}_bar={bar}")
    print(f"{label}_gap={gap}")
    print(f"{label}_sigmas={abs(gap) / bar} side={side(gap)}")


def main() -> int:
    base = (F.G_CAT * F.SUCTION) ** 3
    polish = (F.POOF * F.SUCTION) ** 2
    atm = base * (1 + polish)
    solar = (F.POOF * F.G_CAT * F.P_NEW) ** 3
    bar = ADOPTED_HI if atm > ADOPTED else ADOPTED_LO
    dm31_bar = DM31_LO if atm < DM31 else DM31_HI
    sum_bar = DM31_HI if (atm + solar) > DM31 else DM31_LO
    print(f"base={base}")
    print(f"polish={polish}")
    print(f"atm={atm}")
    print(f"solar={solar}")
    report("adopted_dm32", atm, ADOPTED, bar)
    report("other_global_dm32", atm, OTHER_GLOBAL, OTHER_BAR)
    report("partial_dm32", atm, PARTIAL, PARTIAL_BAR)
    report("listing_dm32", atm, LISTING, LISTING_BAR)
    report("dm31", atm, DM31, dm31_bar)
    report("atm_plus_solar_vs_dm31", atm + solar, DM31, sum_bar)
    print(f"dm32_from_dm31_minus_solar={DM31 - SOLAR_FIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

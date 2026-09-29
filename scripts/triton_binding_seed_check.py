#!/usr/bin/env python3
"""Check the triton binding.

The wave formula is e^2 + 1/G_Catalan. It sits about 1 keV low of the
AME2020 total. The fractional gap divided by (POOF*SUCTION)^2 is
gamma*(1 - 1/e)^2, and 1 - 1/e is psi_con. The leaf multiplies the
wave formula by 1 + (POOF*SUCTION)^2*gamma*psi_con^2. Dividing the
same gap by alpha^2 returns 2.205505, which is not a short ratio of
e and Catalan's G, and several unrelated products sit in that wider
window. G^3*P_new also fits the suction window and is not the leaf.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, pi, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

# AME2020 mass_1.mas20. Binding energy per nucleon, keV, then the total.
BE_A = mpf("2827.2654")
BE_A_UNC = mpf("0.0003")
ROUNDED = 3 * BE_A / 1000
ROUNDED_BAR = 3 * BE_A_UNC / 1000
# Binding rebuilt from the mass excesses in that file: 1H, n, 3H.
EXCESS = (
    mpf("7288.971064") + 2 * mpf("8071.31806") - mpf("14949.81090")
) / 1000
EXCESS_BAR = (
    mpf("0.000013") ** 2
    + (2 * mpf("0.00044")) ** 2
    + mpf("0.00008") ** 2
) ** mpf("0.5") / 1000
STALE = mpf("8.481798")


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred, meas, bar) -> None:
    gap = pred - meas
    print(f"{label}={pred}")
    print(f"{label}_gap_keV={gap * 1000}")
    print(f"{label}_sigmas={abs(gap) / bar} side={side(gap)}")


def main() -> int:
    bare = F.E**2 + 1 / F.G_CAT
    a2 = alpha() ** 2
    yy = (F.POOF * F.SUCTION) ** 2
    piece = F.GAMMA * F.PSI_CON**2
    leaf = bare * (1 + yy * piece)
    # Also inside the suction window, farther from the mass excess.
    g3 = bare * (1 + yy * (F.G_CAT**3 * F.P_NEW))
    # The alpha^2 window is wider. These are not the leaf.
    wider = bare * (1 + a2 * (pi - 1 + F.C_COSM))
    integer_part = bare * (1 + a2 * (2 + F.GAMMA**2 / F.PHI))
    print(f"bare={bare}")
    print(f"yy={yy}")
    print(f"gamma_psi2={piece}")
    print(f"gap_over_yy={(ROUNDED - bare) / bare / yy}")
    print(f"gap_over_yy_excess={(EXCESS - bare) / bare / yy}")
    print(f"gap_over_alpha2={(ROUNDED - bare) / bare / a2}")
    report("leaf_vs_rounded", leaf, ROUNDED, ROUNDED_BAR)
    print(f"rounded={ROUNDED}")
    print(f"rounded_bar_MeV={ROUNDED_BAR}")
    report("leaf_vs_excess", leaf, EXCESS, EXCESS_BAR)
    print(f"excess={EXCESS}")
    print(f"excess_bar_MeV={EXCESS_BAR}")
    report("bare_vs_rounded", bare, ROUNDED, ROUNDED_BAR)
    report("bare_vs_excess", bare, EXCESS, EXCESS_BAR)
    report("G3_Pnew_vs_excess", g3, EXCESS, EXCESS_BAR)
    report("pi_minus_1_plus_C_cosm_vs_excess", wider, EXCESS, EXCESS_BAR)
    report("two_plus_gamma2_over_phi_vs_excess", integer_part, EXCESS, EXCESS_BAR)
    stale_gap = STALE - ROUNDED
    print(
        f"stale_8.481798_sigmas={abs(stale_gap) / ROUNDED_BAR} "
        f"side={side(stale_gap)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

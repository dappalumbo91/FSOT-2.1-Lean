#!/usr/bin/env python3
"""Check the triton binding.

The wave formula is e^2 + 1/G_Catalan. It sits about 1 keV low of the
AME2020 total. The fractional gap divided by the adopted alpha^2 is
2.205505. That number is not a short ratio of e and Catalan's G.
G^-6 + G^2 on the e^2 term would sit inside, and so would several
unrelated products, so none is installed. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power

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
    frac = (ROUNDED - bare) / bare
    inv_g = 1 / F.G_CAT
    print(f"bare={bare}")
    print(f"alpha2={a2}")
    print(f"yy={yy}")
    print(f"gap_over_alpha2={frac / a2}")
    print(f"gap_over_yy={frac / yy}")
    print(f"rounded={ROUNDED}")
    print(f"rounded_bar_MeV={ROUNDED_BAR}")
    report("bare_vs_rounded", bare, ROUNDED, ROUNDED_BAR)
    print(f"excess={EXCESS}")
    print(f"excess_bar_MeV={EXCESS_BAR}")
    report("bare_vs_excess", bare, EXCESS, EXCESS_BAR)
    # Found by comparing the gap to powers of e and G. Just outside.
    g9 = bare * (1 + a2 * power(F.G_CAT, -9))
    report("G_to_minus9_vs_rounded", g9, ROUNDED, ROUNDED_BAR)
    # Same comparison, on the e^2 term only. Inside, and not unique.
    g_pow = power(F.G_CAT, -6) + F.G_CAT**2
    on_e2 = F.E**2 * (1 + a2 * g_pow) + inv_g
    report("Gpow_on_e2_vs_rounded", on_e2, ROUNDED, ROUNDED_BAR)
    same_side = F.P_NEW**3 + power(F.PSI_CON, -2)
    foreign_low = F.E**2 * (1 + a2 * same_side) + inv_g
    report("Pnew3_psi_on_e2_vs_rounded", foreign_low, ROUNDED, ROUNDED_BAR)
    crosses = 3 - F.ETA_EFF
    foreign_high = F.E**2 * (1 + a2 * crosses) + inv_g
    report("three_minus_eta_on_e2_vs_rounded", foreign_high, ROUNDED, ROUNDED_BAR)
    phi_g = F.E**2 * (1 + a2 * (F.PHI + F.G_CAT)) + inv_g
    report("phi_plus_G_on_e2_vs_rounded", phi_g, ROUNDED, ROUNDED_BAR)
    two = bare * (1 + a2 * (2 + F.GAMMA**2 / F.PHI))
    report("two_plus_gamma2_over_phi_vs_rounded", two, ROUNDED, ROUNDED_BAR)
    yy_piece = bare * (1 + yy * (F.GAMMA * F.PSI_CON**2))
    report("gamma_psi2_yy_vs_rounded", yy_piece, ROUNDED, ROUNDED_BAR)
    stale_gap = STALE - ROUNDED
    print(
        f"stale_8.481798_sigmas={abs(stale_gap) / ROUNDED_BAR} "
        f"side={side(stale_gap)}"
    )
    print(
        "note=the formula stays e^2 + 1/G. "
        "G^-6+G^2 is inside, and other short products fit the same windows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

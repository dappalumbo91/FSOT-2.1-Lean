#!/usr/bin/env python3
"""Check the helium-4 binding.

The wave formula is pi/gamma^4, written as pi*gamma/gamma^5. It sits
about 5 keV high of the AME2020 total. The fractional gap divided by
the adopted alpha^2 lands on pi + gamma/e, and gamma/e is P_base.
The leaf multiplies the wave formula by 1 - alpha^2*(pi + P_base).
pi alone in that factor stays high. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

# AME2020 mass_1.mas20. Binding energy per nucleon, keV, then the total.
BE_A = mpf("7073.9156")
BE_A_UNC = mpf("0.0002")
ROUNDED = 4 * BE_A / 1000
ROUNDED_BAR = 4 * BE_A_UNC / 1000
# Binding rebuilt from the mass excesses in that file: 1H, n, 4He.
EXCESS = (
    2 * mpf("7288.971064") + 2 * mpf("8071.31806") - mpf("2424.91587")
) / 1000
EXCESS_BAR = (
    (2 * mpf("0.000013")) ** 2
    + (2 * mpf("0.00044")) ** 2
    + mpf("0.00015") ** 2
) ** mpf("0.5") / 1000
STALE = mpf("28.295674")


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
    bare = F.PI / power(F.GAMMA, 4)
    a2 = alpha() ** 2
    quotient = (bare - ROUNDED) / bare / a2
    piece = F.PI + F.P_BASE
    leaf = bare * (1 - a2 * piece)
    pi_only = bare * (1 - a2 * F.PI)
    print(f"bare={bare}")
    print(f"alpha2={a2}")
    print(f"gap_over_alpha2={quotient}")
    print(f"pi_plus_P_base={piece}")
    print(f"P_base={F.P_BASE}")
    report("leaf_vs_rounded", leaf, ROUNDED, ROUNDED_BAR)
    print(f"rounded={ROUNDED}")
    print(f"rounded_bar_MeV={ROUNDED_BAR}")
    report("leaf_vs_excess", leaf, EXCESS, EXCESS_BAR)
    print(f"excess={EXCESS}")
    print(f"excess_bar_MeV={EXCESS_BAR}")
    report("bare_vs_rounded", bare, ROUNDED, ROUNDED_BAR)
    report("pi_only_vs_rounded", pi_only, ROUNDED, ROUNDED_BAR)
    stale_gap = STALE - ROUNDED
    print(
        f"stale_28.295674_sigmas={abs(stale_gap) / ROUNDED_BAR} "
        f"side={side(stale_gap)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

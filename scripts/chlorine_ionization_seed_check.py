#!/usr/bin/env python3
"""Check chlorine's first ionization energy.

The wave formula is phi^7/sqrt(5). NIST ASD 5.12 gives
12.967633 +/- 0.000016 eV. The bare quotient is about 1060 uncertainties
high. The fractional gap divided by the adopted alpha is 0.1790, and
5/phi^7 is the radicand over the written seventh. That factor alone is
40 uncertainties high. The leftover on that factor is 5.432, and 7 - phi
is the seventh minus its base. One more share is 1.263, and sqrt(phi)
is the square root of that base. The leaf multiplies the wave formula by
1 - alpha*(5/phi^7)*(1 + alpha*(7-phi)*(1 + alpha*sqrt(phi))).
sqrt(5)/phi finishes 0.035 uncertainties low and stays off. This script
only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("12.967633")
BAR = mpf("0.000016")
HANDBOOK = mpf("12.968")


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred) -> None:
    gap = pred - NIST
    print(f"{label}={pred}")
    print(f"{label}_gap={gap}")
    print(f"{label}_sigmas={abs(gap) / BAR} side={side(gap)}")


def main() -> int:
    bare = F.PHI**7 / sqrt(5)
    a = alpha()
    piece = 5 / F.PHI**7
    q2 = 7 - F.PHI
    q3 = sqrt(F.PHI)
    quotient = (bare - NIST) / bare / a
    leaf = bare * (1 - a * piece * (1 + a * q2 * (1 + a * q3)))
    written = bare * (1 - a * piece * (1 + a * q2 * (1 + a * sqrt(5) / F.PHI)))
    two_step = bare * (1 - a * piece * (1 + a * q2))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={quotient}")
    print(f"five_over_phi7={piece}")
    print(f"seven_minus_phi={q2}")
    print(f"sqrt_phi={q3}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("leaf", leaf)
    report("sqrt5_over_phi", written)
    report("two_step", two_step)
    report("bare", bare)
    print(f"handbook_error_pct={abs(leaf - HANDBOOK) / HANDBOOK * 100}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

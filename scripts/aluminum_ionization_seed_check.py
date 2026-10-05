#!/usr/bin/env python3
"""Check aluminum's first ionization energy.

The wave formula is phi^4/ln(pi). NIST ASD 5.12 gives 5.985769 +/- 0.000003 eV.
The bare quotient is about 586 uncertainties high. The fractional gap divided
by the adopted alpha is 0.04025, and 4/pi^4 is the written fourth on the pi
already inside the logarithm. That factor alone is 11.8 uncertainties low.
The leftover on that factor is 2.7086, and e is the base of ln. The leaf
multiplies the wave formula by 1 - alpha*(4/pi^4)*(1 - alpha*e).
phi^2 finishes 0.39 uncertainties low and pi finishes 1.89 high, so they
stay off the leaf. This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import log, mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("5.985769")
BAR = mpf("0.000003")
HANDBOOK = mpf("5.986")


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
    print(f"{label}_gap={gap}")
    print(f"{label}_sigmas={abs(gap) / bar} side={side(gap)}")


def main() -> int:
    bare = F.PHI**4 / log(F.PI)
    a = alpha()
    piece = 4 / F.PI**4
    quotient = (bare - NIST) / bare / a
    on_piece = (NIST - bare * (1 - a * piece)) / (bare * (1 - a * piece)) / (a**2) / piece
    leaf = bare * (1 - a * piece * (1 - a * F.E))
    phi2 = bare * (1 - a * piece * (1 - a * F.PHI**2))
    pi_leaf = bare * (1 - a * piece * (1 - a * F.PI))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={quotient}")
    print(f"four_over_pi4={piece}")
    print(f"on_piece={on_piece}")
    print(f"e={F.E}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("leaf", leaf, NIST, BAR)
    report("phi2", phi2, NIST, BAR)
    report("pi", pi_leaf, NIST, BAR)
    report("bare", bare, NIST, BAR)
    print(f"handbook_error_pct={abs(leaf - HANDBOOK) / HANDBOOK * 100}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

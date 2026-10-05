#!/usr/bin/env python3
"""Check phosphorus's first ionization energy.

The wave formula is pi^2 + 1/phi. NIST ASD 5.12 gives
10.486686 +/- 0.000015 eV. The bare sum is about 63 uncertainties
high. The gap on the inverse, divided by the adopted alpha, is 0.2112,
and 2/pi^2 is the written exponent over the squared pi. That share
alone is 2.56 uncertainties high. The leftover on that factor is 5.768,
and pi + phi^2 is 5.760. phi^2 = phi + 1, so the same number is
pi + phi + 1. That reading is 0.0039 uncertainties high. The leftover
on that sum is 0.208, and 2/pi^2 is that same exponent share again.
The leaf multiplies the inverse by
1 - alpha*(2/pi^2)*(1 + alpha*(pi+phi^2)*(1 + alpha*(2/pi^2))).
1/(phi*pi) finishes 0.00021 uncertainties high and stays off.
This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("10.486686")
BAR = mpf("0.000015")
HANDBOOK = mpf("10.487")


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
    pi2 = F.PI**2
    inv = 1 / F.PHI
    bare = pi2 + inv
    a = alpha()
    piece = 2 / pi2
    q2 = F.PI + F.PHI**2
    q_inv = (bare - NIST) / inv / a
    one = pi2 + inv * (1 - a * piece)
    two = pi2 + inv * (1 - a * piece * (1 + a * q2))
    leaf = pi2 + inv * (1 - a * piece * (1 + a * q2 * (1 + a * piece)))
    other = pi2 + inv * (1 - a * piece * (1 + a * q2 * (1 + a / (F.PHI * F.PI))))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"inv_phi={inv}")
    print(f"gap_on_inv_over_alpha={q_inv}")
    print(f"two_over_pi2={piece}")
    print(f"pi_plus_phi2={q2}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("one_step", one)
    report("two_step", two)
    report("leaf", leaf)
    report("one_over_phi_pi", other)
    report("bare", bare)
    print(f"handbook_error_pct={abs(leaf - HANDBOOK) / HANDBOOK * 100}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

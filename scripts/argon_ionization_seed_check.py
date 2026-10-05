#!/usr/bin/env python3
"""Check argon's first ionization energy.

The wave formula is gamma^(-5) + Poof. NIST ASD 5.12 gives
15.7596119 +/- 0.0000005 eV. The bare sum is about 1024
uncertainties high. The fractional gap divided by the adopted alpha
is 0.004451, and Poof*gamma^5 is Poof over the inverse fifth. That
share alone is 1238 uncertainties low. The leftover is 75.02, and
five times the inverse fifth is 78.03. That reading is 50
uncertainties high. The leftover on that multiple is 5.298, and 5 is
the written exponent. That reading is 2.80 uncertainties high. The
leftover on the exponent is 8.158, and 5/gamma is 8.662. That reading
is 0.17 uncertainties low. The leftover on that quotient is 7.984,
and 5*(1+gamma) is the same exponent times one plus its base. The
leaf multiplies the wave formula by
1 - alpha*(Poof*gamma^5)*(1 - alpha*(5/gamma^5)*(1 - alpha*5*(1 + alpha*(5/gamma)*(1 - alpha*5*(1+gamma))))).
5/gamma on the last share finishes 0.015 uncertainties high and stays off.
This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("15.7596119")
BAR = mpf("0.0000005")
HANDBOOK = mpf("15.76")


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
    a = alpha()
    g5 = F.GAMMA ** (-5)
    bare = g5 + F.POOF
    piece = F.POOF * F.GAMMA**5
    q2 = 5 * g5
    q4 = 5 / F.GAMMA
    q5 = 5 * (1 + F.GAMMA)
    quotient = (bare - NIST) / bare / a
    one = bare * (1 - a * piece)
    two = bare * (1 - a * piece * (1 - a * q2))
    three = bare * (1 - a * piece * (1 - a * q2 * (1 - a * 5)))
    four = bare * (1 - a * piece * (1 - a * q2 * (1 - a * 5 * (1 + a * q4))))
    leaf = bare * (1 - a * piece * (1 - a * q2 * (1 - a * 5 * (1 + a * q4 * (1 - a * q5)))))
    other = bare * (1 - a * piece * (1 - a * q2 * (1 - a * 5 * (1 + a * q4 * (1 - a * q4)))))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={quotient}")
    print(f"poof_times_gamma5={piece}")
    print(f"five_gamma_inv5={q2}")
    print(f"five_over_gamma={q4}")
    print(f"five_times_one_plus_gamma={q5}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("one_step", one)
    report("two_step", two)
    report("three_step", three)
    report("four_step", four)
    report("leaf", leaf)
    report("five_over_gamma_last", other)
    report("bare", bare)
    print(f"handbook_error_pct={abs(leaf - HANDBOOK) / HANDBOOK * 100}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check sulfur's first ionization energy.

The wave formula is phi^6/sqrt(3). NIST ASD 5.12 gives
10.3600167 +/- 0.0000014 eV. The bare quotient is about 81
uncertainties high. The fractional gap divided by the adopted alpha
is 0.001502, and 6/phi^18 is the written sixth over the sixth power
raised to the radicand. That share alone is 25 uncertainties high.
The leftover is 61.11, and six times the wave is 62.16. That reading
is 0.43 uncertainties low. The leftover on that multiple is 2.308, and
2 is the root index. That reading is 0.057 uncertainties low. The
leftover on the root index is 21.10, and phi^6 + 3 is the sixth power
plus the radicand. The leftover on that sum is 1.022, so one more
factor of the adopted alpha finishes the leaf. 12*sqrt(3) on the
fourth share finishes 0.00086 uncertainties low and stays off.
This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("10.3600167")
BAR = mpf("0.0000014")
HANDBOOK = mpf("10.36")


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
    bare = F.PHI**6 / sqrt(3)
    piece = 6 / F.PHI**18
    q2 = 6 * bare
    q4 = F.PHI**6 + 3
    quotient = (bare - NIST) / bare / a
    one = bare * (1 - a * piece)
    two = bare * (1 - a * piece * (1 + a * q2))
    three = bare * (1 - a * piece * (1 + a * q2 * (1 - a * 2)))
    fourth = bare * (1 - a * piece * (1 + a * q2 * (1 - a * 2 * (1 + a * q4))))
    leaf = bare * (1 - a * piece * (1 + a * q2 * (1 - a * 2 * (1 + a * q4 * (1 + a)))))
    other = bare * (1 - a * piece * (1 + a * q2 * (1 - a * 2 * (1 + a * (12 * sqrt(3))))))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={quotient}")
    print(f"six_over_phi18={piece}")
    print(f"six_times_wave={q2}")
    print(f"phi6_plus_3={q4}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("one_step", one)
    report("two_step", two)
    report("three_step", three)
    report("four_step", fourth)
    report("leaf", leaf)
    report("twelve_sqrt3", other)
    report("bare", bare)
    print(f"handbook_error_pct={abs(leaf - HANDBOOK) / HANDBOOK * 100}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

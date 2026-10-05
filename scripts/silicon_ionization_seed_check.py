#!/usr/bin/env python3
"""Check silicon's first ionization energy.

The wave formula is e^2 + sqrt(gamma). NIST ASD 5.12 gives
8.15168 +/- 0.00003 eV. The bare sum is about 96 uncertainties low.
The gap on the square root, divided by the adopted alpha, is 0.5189,
and 1/2 is the root index. That share alone is 3.49 uncertainties low.
The leftover on that half is 5.177, and e^2 - 2 is the squared term
minus its written exponent. That reading is 0.14 uncertainties high.
The leftover on that difference is 5.393, the same difference again.
The leaf adds the square root times
1 + alpha*(1/2)*(1 + alpha*(e^2-2)*(1 - alpha*(e^2-2))).
2*e on that last share finishes 0.0012 uncertainties low and stays off.
This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("8.15168")
BAR = mpf("0.00003")
HANDBOOK = mpf("8.152")


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
    e2 = F.E**2
    root = sqrt(F.GAMMA)
    bare = e2 + root
    a = alpha()
    diff = e2 - 2
    half = mpf(1) / 2
    q_root = (NIST - bare) / root / a
    one = e2 + root * (1 + a * half)
    two = e2 + root * (1 + a * half * (1 + a * diff))
    leaf = e2 + root * (1 + a * half * (1 + a * diff * (1 - a * diff)))
    two_e = e2 + root * (1 + a * half * (1 + a * diff * (1 - a * (2 * F.E))))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"sqrt_gamma={root}")
    print(f"gap_on_root_over_alpha={q_root}")
    print(f"half={half}")
    print(f"e2_minus_2={diff}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("one_step", one)
    report("two_step", two)
    report("leaf", leaf)
    report("two_e", two_e)
    report("bare", bare)
    print(f"handbook_error_pct={abs(leaf - HANDBOOK) / HANDBOOK * 100}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

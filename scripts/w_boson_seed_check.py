#!/usr/bin/env python3
"""Check the W mass as theta_S^-6 * C_factor^-4 * gamma^2 + e^e.

The first product is the formula already on the row, read on the live seeds.
gamma is Euler's constant. The added piece is e raised to e.
PDG 2024 quotes 80369.2 ± 13.3 MeV, with the CDF measurement left out.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MEAS = mpf("80369.2")
BAR = mpf("13.3")


def main() -> int:
    base = power(F.THETA_S, -6) * power(F.C_FACTOR, -4) * F.GAMMA**2
    piece = power(F.E, F.E)
    mass = base + piece
    gap = mass - MEAS
    print(f"base={base}")
    print(f"e^e={piece}")
    print(f"need_over_ee={(MEAS - base) / piece}")
    print(f"mass={mass}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / BAR} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

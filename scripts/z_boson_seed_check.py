#!/usr/bin/env python3
"""Check the Z mass as the live W seed divided by the on-shell cosine.

The W piece is theta_S^-6 * C_factor^-4 * gamma^2. Gamma is Euler's constant.
The angle is the one already in the seeds: sin^2 theta_W = POOF + K/6.
The Z mass is that W piece divided by the cosine.
PDG 2024 gives 91.1880 ± 0.0020 GeV, which is 91188 ± 2.0 MeV.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MEASURED_MEV = mpf("91188.0")
BAR_MEV = mpf("2.0")


def main() -> int:
    w = power(F.THETA_S, -6) * power(F.C_FACTOR, -4) * F.GAMMA**2
    sin2 = F.POOF + F.K / 6
    z = w / sqrt(1 - sin2)
    gap = z - MEASURED_MEV
    print(f"w_MeV={w}")
    print(f"sin2={sin2}")
    print(f"z_MeV={z}")
    print(f"gap_MeV={gap}")
    print(f"sigmas={abs(gap) / BAR_MEV} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

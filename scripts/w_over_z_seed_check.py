#!/usr/bin/env python3
"""Check M_W/M_Z as the W leaf divided by the Z leaf.

The W leaf includes e^e. The Z leaf uses the W product without that piece.
PDG 2024: W 80369.2 ± 13.3 MeV, Z 91188.0 ± 2.0 MeV.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

W_MEAS = mpf("80369.2")
W_BAR = mpf("13.3")
Z_MEAS = mpf("91188.0")
Z_BAR = mpf("2.0")


def main() -> int:
    product = power(F.THETA_S, -6) * power(F.C_FACTOR, -4) * F.GAMMA**2
    w = product + power(F.E, F.E)
    z = product / sqrt(1 - (F.POOF + F.K / 6))
    ratio = w / z
    pdg = W_MEAS / Z_MEAS
    bar = pdg * sqrt((W_BAR / W_MEAS) ** 2 + (Z_BAR / Z_MEAS) ** 2)
    gap = ratio - pdg
    print(f"W={w}")
    print(f"Z={z}")
    print(f"ratio={ratio}")
    print(f"pdg={pdg}")
    print(f"bar={bar}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / bar} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

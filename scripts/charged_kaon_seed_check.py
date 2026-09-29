#!/usr/bin/env python3
"""Check the charged kaon mass as G_Catalan^-7 + P_base^-4 - pi^-4.

The first two terms are the formula already on the row.
pi^-4 uses the same fourth power. The bare sum is just over the
tighter PDG average. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MEAS = mpf("493.677")
AVG_BAR = mpf("0.013")
FIT_BAR = mpf("0.015")


def main() -> int:
    base = power(F.G_CAT, -7) + power(F.P_BASE, -4)
    piece = power(F.PI, -4)
    mass = base - piece
    gap = mass - MEAS
    side = "high" if gap > 0 else "low"
    print(f"base={base}")
    print(f"pi^-4={piece}")
    print(f"mass={mass}")
    print(f"gap={gap}")
    print(f"average_sigmas={abs(gap) / AVG_BAR} side={side}")
    print(f"fit_sigmas={abs(gap) / FIT_BAR} side={side}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

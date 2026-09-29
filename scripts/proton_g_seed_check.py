#!/usr/bin/env python3
"""Check the proton g-factor.

P_new/P_base is sqrt(2), so the leading piece is (A_in*sqrt(2))^2.
The rest is alpha/psi_con^3 times one plus (POOF*SUCTION)^4.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

G = mpf("5.5856946893")
BAR = mpf("1.6e-9")


def main() -> int:
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    value = (F.A_IN * F.P_NEW / F.P_BASE) ** 2 + (alpha / F.PSI_CON**3) * (
        1 + (F.POOF * F.SUCTION) ** 4
    )
    diff = value - G
    print(f"leading={(F.A_IN * F.P_NEW / F.P_BASE) ** 2}")
    print(f"g={value}")
    print(f"sigmas={abs(diff) / BAR} side={'high' if diff > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

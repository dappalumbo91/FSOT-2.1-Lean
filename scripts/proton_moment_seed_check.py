#!/usr/bin/env python3
"""Check the proton magnetic moment as the proton g-factor leaf divided by 2.

CODATA 2022 proton mag. mom. to nuclear magneton ratio is 2.79284734463(82).
The (82) is an absolute uncertainty of 8.2e-10. The g-factor leaf is unchanged.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MEASURED = mpf("2.79284734463")
BAR = mpf("8.2e-10")


def main() -> int:
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    g_factor = (F.A_IN * F.P_NEW / F.P_BASE) ** 2 + (alpha / F.PSI_CON**3) * (
        1 + (F.POOF * F.SUCTION) ** 4
    )
    moment = g_factor / 2
    gap = moment - MEASURED
    print(f"g={g_factor}")
    print(f"moment={moment}")
    print(f"codata={MEASURED}")
    print(f"bar={BAR}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / BAR} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

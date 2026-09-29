#!/usr/bin/env python3
"""Check the D+ mass as (P_var/P_base)^5 + pi/4.

(P_var/P_base)^5 is the formula already on the row.
The added piece is one quarter of pi. The gap over pi is 0.24998.
PDG fit is 1869.66 ± 0.05 MeV.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, pi, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

FIT = mpf("1869.66")
FIT_BAR = mpf("0.05")
AVG = mpf("1869.5")
AVG_BAR = mpf("0.4")


def main() -> int:
    base = power(F.P_VAR / F.P_BASE, 5)
    mass = base + pi / 4
    gap = mass - FIT
    print(f"base={base}")
    print(f"gap_over_pi={(FIT - base) / pi}")
    print(f"pi_over_4={pi / 4}")
    print(f"mass={mass}")
    print(f"fit_gap={gap}")
    print(f"fit_sigmas={abs(gap) / FIT_BAR} side={'high' if gap > 0 else 'low'}")
    agap = mass - AVG
    print(f"average_gap={agap}")
    print(f"average_sigmas={abs(agap) / AVG_BAR} side={'high' if agap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

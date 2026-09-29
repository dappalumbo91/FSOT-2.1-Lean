#!/usr/bin/env python3
"""Check the Higgs mass as (THETA_S + e^3) / C_FACTOR^7.

The row is in MeV. PDG 2024, still the 2025 listing average, is
125.20 ± 0.11 GeV. The ±0.11 already includes the scale factor 1.4.
The extra (1+(POOF*SUCTION)^2) on seed_higgs_GeV is printed beside
the base. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MEASURED = mpf("125.20") * 1000
BAR = mpf("0.11") * 1000


def main() -> int:
    base = (F.THETA_S + F.E**3) / F.C_FACTOR**7
    polish = 1 + (F.POOF * F.SUCTION) ** 2
    full = base * polish
    gap = base - MEASURED
    full_gap = full - MEASURED
    print(f"base_MeV={base}")
    print(f"pdg_MeV={MEASURED}")
    print(f"bar_MeV={BAR}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / BAR} side={'high' if gap > 0 else 'low'}")
    print(f"with_polish_MeV={full}")
    print(
        f"polish_sigmas={abs(full_gap) / BAR} "
        f"side={'high' if full_gap > 0 else 'low'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

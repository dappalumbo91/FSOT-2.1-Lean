#!/usr/bin/env python3
"""Check the proton charge radius as G_Catalan^7 + P_new.

That sum is the r_p formula already in the engine.
PDG 2024 gives 0.8409 ± 0.0004 fm.
CODATA 2022 gives 0.84075 ± 0.00064 fm.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

PDG = mpf("0.8409")
PDG_BAR = mpf("0.0004")
CODATA = mpf("0.84075")
CODATA_BAR = mpf("0.00064")


def main() -> int:
    radius = power(F.G_CAT, 7) + F.P_NEW
    gap = radius - PDG
    print(f"G7={power(F.G_CAT, 7)}")
    print(f"P_new={F.P_NEW}")
    print(f"radius_fm={radius}")
    print(f"pdg_gap_fm={gap}")
    print(f"pdg_sigmas={abs(gap) / PDG_BAR} side={'high' if gap > 0 else 'low'}")
    codata_gap = radius - CODATA
    print(f"codata2022_gap_fm={codata_gap}")
    print(
        f"codata2022_sigmas={abs(codata_gap) / CODATA_BAR} "
        f"side={'high' if codata_gap > 0 else 'low'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

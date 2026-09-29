#!/usr/bin/env python3
"""Check the MS-bar weak mixing angle.

The bare piece is (gamma - 1/pi^2)/phi^(3/2). PDG 2024's global fit
gives s-hat^2_Z = 0.23129 ± 0.00004. One adopted alpha^2 is the piece
on the row. alpha^2*sqrt(phi) is printed beside it. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MEASURED = mpf("0.23129")
BAR = mpf("0.00004")


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def main() -> int:
    bare = (F.GAMMA - 1 / F.PI**2) / power(F.PHI, mpf("1.5"))
    a2 = alpha() ** 2
    value = bare + a2
    center_piece = bare + a2 * sqrt(F.PHI)
    gap = value - MEASURED
    bare_gap = bare - MEASURED
    center_gap = center_piece - MEASURED
    print(f"bare={bare}")
    print(f"alpha2={a2}")
    print(f"gap_over_alpha2={(MEASURED - bare) / a2}")
    print(f"value={value}")
    print(f"pdg={MEASURED}")
    print(f"bar={BAR}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / BAR} side={'high' if gap > 0 else 'low'}")
    print(
        f"bare_sigmas={abs(bare_gap) / BAR} "
        f"side={'high' if bare_gap > 0 else 'low'}"
    )
    print(f"alpha2_sqrt_phi={center_piece}")
    print(
        f"alpha2_sqrt_phi_sigmas={abs(center_gap) / BAR} "
        f"side={'high' if center_gap > 0 else 'low'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

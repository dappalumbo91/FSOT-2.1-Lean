#!/usr/bin/env python3
"""Check the charm-to-bottom ratio as C_cosm/P_base + alpha*sqrt(phi).

C_cosm/P_base is the formula already on the row, read on the live seeds.
The added piece is the adopted alpha times the square root of the golden ratio.
The PDG ratio is 1.2730/4.183. The uncertainty is the quadrature of the
ideogram errors 0.0028 GeV and 0.004 GeV. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MC = mpf("1.2730")
MB = mpf("4.183")
DMC = mpf("0.0028")
DMB = mpf("0.004")


def main() -> int:
    ratio = MC / MB
    bar = ratio * ((DMC / MC) ** 2 + (DMB / MB) ** 2) ** mpf("0.5")
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    base = F.C_COSM / F.P_BASE
    mass = base + alpha * sqrt(F.PHI)
    gap = mass - ratio
    print(f"base={base}")
    print(f"alpha_sqrt_phi={alpha * sqrt(F.PHI)}")
    print(f"ratio={mass}")
    print(f"pdg={ratio}")
    print(f"bar={bar}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / bar} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

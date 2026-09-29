#!/usr/bin/env python3
"""Check the charged pion mass as theta_S^-4 - theta_S^2 + alpha/(pi-1).

alpha/(pi-1) is the adopted alpha times eta_eff. eta_eff is 1/(pi-1).
PDG 2024 gives 139.57039 ± 0.00018 MeV.
This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MEAS = mpf("139.57039")
BAR = mpf("0.00018")


def main() -> int:
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    base = power(F.THETA_S, -4) - F.THETA_S**2
    mass = base + alpha / (F.PI - 1)
    gap = mass - MEAS
    print(f"base={base}")
    print(f"alpha_eta={alpha / (F.PI - 1)}")
    print(f"mass={mass}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / BAR} side={'high' if gap > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

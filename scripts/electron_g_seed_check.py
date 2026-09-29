#!/usr/bin/env python3
"""Compare the electron g-factor gap with the third-order piece.

The bare anomaly (e/pi - ln2)/e^5 is high. The gap is 0.621126 of
(alpha/pi)^3, with alpha the adopted fine-structure leaf. One over phi
is the nearby seed and stays outside the CODATA uncertainty. The weight
on the leaf is A_bleed*G_Catalan^2*P_base/P_new. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import fabs, log, mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

G_MEAS = mpf("2.00231930436092")
BAR = mpf("3.6e-13")


def main() -> int:
    look = F.E / F.PI - log(2)
    bare = look / F.E**5
    yy = (F.POOF * F.SUCTION) ** 2
    interface = F.C_FACTOR**2 / F.P_BASE
    alpha = 1 / (F.E**3 * F.PHI**4 - F.PSI_CON - yy * interface)
    third = (alpha / F.PI) ** 3
    gap = bare - (G_MEAS / 2 - 1)
    weight = F.A_BLEED * F.G_CAT**2 * F.P_BASE / F.P_NEW
    candidates = {
        "bare anomaly": bare,
        "(alpha/pi)^3 / phi": bare - third / F.PHI,
        "(alpha/pi)^3 * psi_con": bare - third * F.PSI_CON,
        "phi^-1 + phi^-12": bare - third * (F.PHI ** -1 + F.PHI ** -12),
        "alpha channel * |chaos|^4 / pi^5": bare
        - yy * interface * fabs(F.CHAOS) ** 4 / F.PI**5,
        "A_bleed*G_Catalan^2*P_base/P_new": bare - third * weight,
    }
    print(f"gap_over_third={gap / third}")
    print(f"weight={weight}")
    print(f"one_over_phi={1 / F.PHI}")
    for name, anomaly in candidates.items():
        g = 2 * (1 + anomaly)
        diff = g - G_MEAS
        ppm = diff / G_MEAS * mpf("1e6")
        print(
            f"{name}: g={g} signed_ppm={ppm} "
            f"sigmas={fabs(diff) / BAR} meets={fabs(diff) <= BAR}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

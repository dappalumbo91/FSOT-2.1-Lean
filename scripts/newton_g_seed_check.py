#!/usr/bin/env python3
"""Check Newton's G from the electron mass and one exponent.

G = hbar*c/m_e^2 * exp(-(e^2*phi^3/ln2^3 + phi*omega/(gamma^2*ln2))).
gamma is Euler's constant. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, pi, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

G = mpf("6.67430e-11")
BAR = mpf("1.5e-15")
C = mpf("299792458")
H = mpf("6.62607015e-34")
NU = mpf("9192631770")


def main() -> int:
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    mass = H * NU / C**2 * exp(
        power(F.E, F.PI)
        + (F.C_FACTOR * F.K * log(2)) ** 2
        + F.G_CAT * F.P_NEW * F.PSI_CON
        - alpha**5 * F.PHI**2 / log(2) ** 2
    )
    first = F.E**2 * F.PHI**3 / log(2) ** 3
    second = F.PHI * F.OMEGA / (F.GAMMA**2 * log(2))
    grav = H / (2 * pi) * C / mass**2 * exp(-(first + second))
    diff = grav - G
    print(f"piece_e2_phi3={first}")
    print(f"piece_omega={second}")
    print(f"exponent={first + second}")
    print(f"G={grav}")
    print(f"sigmas={abs(diff) / BAR} side={'high' if diff > 0 else 'low'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

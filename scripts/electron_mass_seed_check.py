#!/usr/bin/env python3
"""Check the electron mass against the caesium-clock pure number.

SI fixes h, c, and the caesium frequency, so the kilogram mass is that
unit times a pure number. The logarithm of the pure number is e^pi plus
(C_factor*K*ln2)^2 plus G_Catalan*P_new*psi_con. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import exp, log, mpf, pi, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

M = mpf("9.1093837139e-31")
BAR = mpf("2.8e-40")
C = mpf("299792458")
H = mpf("6.62607015e-34")
NU = mpf("9192631770")
CHARGE = mpf("1.602176634e-19")


def main() -> int:
    alpha = 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )
    square = (F.C_FACTOR * F.K * log(2)) ** 2
    bulk = F.G_CAT * F.P_NEW * F.PSI_CON
    exponent = power(F.E, F.PI) + square + bulk
    mass = H * NU / C**2 * exp(exponent)
    diff = mass - M
    print(f"e^pi={power(F.E, F.PI)}")
    print(f"square={square}")
    print(f"bulk={bulk}")
    print(f"exponent={exponent}")
    print(f"target_ln={log(M * C**2 / (H * NU))}")
    print(f"mass={mass}")
    print(f"signed_rel={diff / M}")
    print(f"sigmas={abs(diff) / BAR} side={'high' if diff > 0 else 'low'}")
    rydberg = alpha**2 * mass * C / (2 * H)
    bohr = H / (2 * pi * mass * C * alpha)
    compton = H / (mass * C)
    radius = alpha * compton / (2 * pi)
    thomson = 8 * pi * radius**2 / 3
    hartree = alpha**2 * mass * C**2
    magneton = CHARGE * H / (4 * pi * mass)
    rows = (
        ("Rydberg", rydberg, mpf("10973731.568157"), mpf("1.1e-12")),
        ("Bohr radius", bohr, mpf("5.29177210544e-11"), mpf("1.6e-10")),
        ("Compton", compton, mpf("2.42631023538e-12"), mpf("3.1e-10")),
        ("classical radius", radius, mpf("2.8179403205e-15"), mpf("4.7e-10")),
        ("Thomson", thomson, mpf("6.6524587051e-29"), mpf("9.3e-10")),
        ("Hartree", hartree, mpf("4.359744722206e-18"), mpf("1.1e-12")),
        ("Bohr magneton", magneton, mpf("9.2740100657e-24"), mpf("3.1e-10")),
    )
    for name, pred, meas, bar in rows:
        rel = (pred - meas) / meas
        print(f"{name} rel={rel} sigmas={abs(rel) / bar} meets={abs(rel) <= bar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

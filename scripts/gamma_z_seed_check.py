#!/usr/bin/env python3
"""Check the Z width over its mass.

The wave formula is phi^5/e^6. PDG 2024 gives Gamma_Z = 2.4955(23) GeV
and M_Z = 91.1880(20) GeV, so the ratio is 0.02736654 with sigma 0.000025.
The bare seed is about 4.93 uncertainties high. The fractional gap divided
by the adopted alpha lands on 1/phi, and phi is already the tower.
The leaf multiplies the wave formula by 1 - alpha/phi.
alpha*gamma and alpha*psi_con also fall inside two uncertainties and finish
farther, so they stay off the leaf. This script only prints.
The engine row stays on the bare seed.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

WIDTH = mpf("2.4955")
MASS = mpf("91.1880")
SIGMA = mpf("0.000025")
DISPLAY = mpf("0.027366")


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred, meas, bar) -> None:
    gap = pred - meas
    print(f"{label}={pred}")
    print(f"{label}_gap={gap}")
    print(f"{label}_sigmas={abs(gap) / bar} side={side(gap)}")
    print(f"{label}_error_pct={abs(gap) / abs(meas) * 100}")


def main() -> int:
    bare = F.PHI**5 / F.E**6
    a = alpha()
    ratio = WIDTH / MASS
    quotient = (bare - ratio) / bare / a
    leaf = bare * (1 - a / F.PHI)
    gamma_leaf = bare * (1 - a * F.GAMMA)
    psi_leaf = bare * (1 - a * F.PSI_CON)
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={quotient}")
    print(f"one_over_phi={1 / F.PHI}")
    print(f"pdg_ratio={ratio}")
    print(f"display_target={DISPLAY}")
    print(f"bar={SIGMA}")
    report("leaf_vs_ratio", leaf, ratio, SIGMA)
    report("leaf_vs_display", leaf, DISPLAY, SIGMA)
    report("bare_vs_ratio", bare, ratio, SIGMA)
    report("alpha_gamma_vs_ratio", gamma_leaf, ratio, SIGMA)
    report("alpha_psi_vs_ratio", psi_leaf, ratio, SIGMA)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

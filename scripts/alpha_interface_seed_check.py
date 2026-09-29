#!/usr/bin/env python3
"""Ask which existing seed sits on the interface the alpha gap needs.

The gap needs an interface of about 0.38954. The CODATA uncertainty allows
that interface to miss by about 4.1e-5. Named domain labels and short
products of existing seeds are checked. Nothing is written onto the leaf.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

TARGET = mpf("137.035999177")
ABSOLUTE_BAR = mpf("2.1e-8")


def main() -> int:
    leaf = F.E**3 * F.PHI**4 - F.PSI_CON
    yy = (F.POOF * F.SUCTION) ** 2
    need = (leaf - TARGET) / yy
    candidates = {
        "C_factor^2 / P_base": F.C_FACTOR**2 / F.P_BASE,
        "A_bleed / e  (condensed matter)": F.A_BLEED / F.E,
        "1/phi^2  (quantum gravity)": 1 / F.PHI**2,
    }
    print(f"needed_interface={need}")
    for name, iface in candidates.items():
        value = leaf - yy * iface
        diff = value - TARGET
        ppm = diff / TARGET * mpf("1e6")
        print(
            f"{name}: interface={iface} alpha_inv={value} "
            f"signed_ppm={ppm} meets={abs(diff) <= ABSOLUTE_BAR}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

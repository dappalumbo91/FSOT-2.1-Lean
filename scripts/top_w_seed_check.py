#!/usr/bin/env python3
"""Check m_t/m_W as |S_cosm|/|Chaos| + psi_con on the live seeds.

PDG 2024 direct top mass is 172.57 ± 0.29 GeV. The W mass is the same
2024 average used on the W row, 80369.2 ± 13.3 MeV. The ratio bar is
those two uncertainties in quadrature. The Higgs-path top mass over
the W leaf is printed beside the adopted ratio. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import fabs, mpf, sqrt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

MT = mpf("172.57")
MT_BAR = mpf("0.29")
MW = mpf("80369.2") / 1000
MW_BAR = mpf("13.3") / 1000


def main() -> int:
    ratio = fabs(F.S_COSM) / fabs(F.CHAOS) + F.PSI_CON
    pdg = MT / MW
    bar = pdg * sqrt((MT_BAR / MT) ** 2 + (MW_BAR / MW) ** 2)
    gap = ratio - pdg
    higgs = (F.THETA_S + F.E**3) / F.C_FACTOR**7 / 1000 * (
        1 + (F.POOF * F.SUCTION) ** 2
    )
    w_leaf = F.THETA_S ** -6 * F.C_FACTOR ** -4 * F.GAMMA**2 + F.E**F.E
    higgs_path = higgs * F.PI * F.K / F.C_EFF / (w_leaf / 1000)
    path_gap = higgs_path - pdg
    print(f"ratio={ratio}")
    print(f"pdg={pdg}")
    print(f"bar={bar}")
    print(f"gap={gap}")
    print(f"sigmas={abs(gap) / bar} side={'high' if gap > 0 else 'low'}")
    print(f"higgs_path={higgs_path}")
    print(
        f"higgs_path_sigmas={abs(path_gap) / bar} "
        f"side={'high' if path_gap > 0 else 'low'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check ammonia's normal boiling point.

The wave formula is e^5 * phi. NIST Chemistry WebBook fluid data
give 239.832 K (Gao, Wu, Bell, and Lemmon). The vapor-pressure
uncertainty is 0.05% from 200 K to 404 K. Between the saturation
row 239.71 K at 1.0070e5 Pa and 239.832 K at 101325 Pa, that 0.05%
is about 0.01 K. The bare product is 0.306 K high. The fractional
gap divided by the adopted alpha is 0.1744. The reciprocal of the
written fifth is 1/5. That share alone is 0.0449 K low. The leftover
is 17.57, and 5*(1+e) is the same exponent times one plus its base.
The leaf multiplies the wave formula by
1 - alpha*(1/5)*(1 - alpha*(5*(1+e))).
The exponent 5 finishes 0.032 K low and stays off. e on that leftover
finishes 0.038 K low and stays off. This script only prints. The
engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("239.832")
HANDBOOK = mpf("239.82")
P_NIST = mpf("101325")
P_ROW = mpf("1.0070e5")
T_ROW = mpf("239.71")
CENTERS = {
    "BP_H₂O": (mpf("373.1243"), mpf("0.0004")),
    "BP_NH₃": (NIST, None),
    "BP_CH₄": (mpf("111.667"), mpf("0.0005")),
    "BP_C₂H₅OH": (mpf("351.44"), mpf("0.005")),
    "BP_CO₂_sub": (mpf("194.6857"), mpf("0.003")),
}


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def main() -> int:
    a = alpha()
    bare = F.E**5 * F.PHI
    slope = (P_NIST - P_ROW) / (NIST - T_ROW)
    bar = (P_NIST * mpf("0.0005")) / slope
    CENTERS["BP_NH₃"] = (NIST, bar)
    p1 = mpf(1) / 5
    p2 = 5 * (1 + F.E)
    one = bare * (1 - a * p1)
    leaf = bare * (1 - a * p1 * (1 - a * p2))
    exp5 = bare * (1 - a * p1 * (1 - a * 5))
    base_e = bare * (1 - a * p1 * (1 - a * F.E))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={(bare - NIST) / bare / a}")
    print(f"one_fifth={p1}")
    print(f"five_times_one_plus_e={p2}")
    print(f"nist={NIST}")
    print(f"slope_Pa_per_K={slope}")
    print(f"bar={bar}")

    def report(label, pred) -> None:
        gap = pred - NIST
        print(f"{label}={pred}")
        print(f"{label}_gap_K={gap}")
        print(f"{label}_bars={abs(gap) / bar} side={side(gap)}")

    report("one_step", one)
    report("leaf", leaf)
    report("exponent_5", exp5)
    report("base_e", base_e)
    print(f"handbook_error_pct={abs(float(leaf) - float(HANDBOOK)) / float(HANDBOOK) * 100}")
    print(f"leaf_float={float(leaf)!r}")
    factor = leaf / bare
    nearest = None
    for row in F.chemistry_molecular():
        if row.name not in CENTERS or row.name == "BP_NH₃":
            continue
        center, other_bar = CENTERS[row.name]
        gap = row.computed * factor - center
        bars = abs(gap) / other_bar
        print(f"other={row.name} gap_K={gap} bars={bars}")
        if nearest is None or bars < nearest[0]:
            nearest = (bars, row.name)
    print(f"nearest_other={nearest[1]} bars={nearest[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

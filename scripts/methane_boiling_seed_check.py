#!/usr/bin/env python3
"""Check methane's normal boiling point.

The wave formula is pi^7 * gamma^6. NIST Chemistry WebBook fluid
data give 111.667 K (Setzmann and Wagner 1991). The stated
uncertainties on that page are density, sound speed, and heat
capacity, so the bar used here is half of the last quoted
millikelvin, 0.0005 K. The bare product is 0.039 K high. The
fractional gap divided by the adopted alpha is 0.04824. The written
sixth is 0.03699 and leaves 41.70, which names no piece of the
product. 1/(7*pi) is the reciprocal of the seventh times its base.
That share alone is 0.00226 K high. The leftover is 8.343, and
6*(1+gamma) is the sixth's exponent times one plus its base. The
leaf multiplies the wave formula by
1 - alpha*(1/(7*pi))*(1 + alpha*(6*(1+gamma))).
The exponent 7 finishes 0.00036 K high and stays off. 1/(6*pi) then
7/gamma finishes 0.000094 K low and stays off because 6 is gamma's
exponent on pi. This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("111.667")
BAR = mpf("0.0005")
HANDBOOK = mpf("111.66")
CENTERS = {
    "BP_H₂O": (mpf("373.1243"), mpf("0.0004")),
    "BP_NH₃": (mpf("239.832"), mpf("0.0099")),
    "BP_CH₄": (NIST, BAR),
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


def report(label, pred) -> None:
    gap = pred - NIST
    print(f"{label}={pred}")
    print(f"{label}_gap_K={gap}")
    print(f"{label}_bars={abs(gap) / BAR} side={side(gap)}")


def main() -> int:
    a = alpha()
    g = F.GAMMA
    bare = F.PI**7 * g**6
    p1 = 1 / (7 * F.PI)
    p2 = 6 * (1 + g)
    one = bare * (1 - a * p1)
    leaf = bare * (1 - a * p1 * (1 + a * p2))
    exp7 = bare * (1 - a * p1 * (1 + a * 7))
    cross = bare * (1 - a * (1 / (6 * F.PI)) * (1 - a * (7 / g)))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={(bare - NIST) / bare / a}")
    print(f"gamma6={g**6}")
    print(f"one_over_7pi={p1}")
    print(f"six_times_one_plus_gamma={p2}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("one_step", one)
    report("leaf", leaf)
    report("exponent_7", exp7)
    report("cross_wired", cross)
    print(f"handbook_error_pct={abs(float(leaf) - float(HANDBOOK)) / float(HANDBOOK) * 100}")
    print(f"leaf_float={float(leaf)!r}")
    factor = leaf / bare
    nearest = None
    for row in F.chemistry_molecular():
        if row.name not in CENTERS or row.name == "BP_CH₄":
            continue
        center, bar = CENTERS[row.name]
        gap = row.computed * factor - center
        bars = abs(gap) / bar
        print(f"other={row.name} gap_K={gap} bars={bars}")
        if nearest is None or bars < nearest[0]:
            nearest = (bars, row.name)
    print(f"nearest_other={nearest[1]} bars={nearest[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

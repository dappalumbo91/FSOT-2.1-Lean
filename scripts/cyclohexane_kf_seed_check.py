#!/usr/bin/env python3
"""Check cyclohexane's cryoscopic constant.

The wave formula is E^3. The printed CRC / Atkins digit is 20.0
K kg/mol, and half of that integer is 0.5. The bare cube is 0.0855
high. The fractional gap divided by the adopted alpha is 0.5836.
1/e is the reciprocal of the written base. That share is the closest
reading of the cube. The leaf multiplies the wave formula by
1 - alpha*(1/e). 1/3, e/3, and 3-e also finish inside half of 0.1
and stay off because they finish farther. 3/e^2 finishes closer and
stays off because e^2 is not written in the cube. The leftover on
1/e is 80.4. The exponent 3 and 3*(1+e) do not name it, so that step
waits. This script only prints. The engine has no cryoscopic row
for cyclohexane.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

CENTER = mpf("20")
BAR = mpf("0.5")
HANDBOOK = CENTER
OTHERS = (
    ("H2O_Kb", mpf("0.5120150995357865"), mpf("0.512"), mpf("0.0005")),
    ("benzene_Kb", mpf("2.5300140780352622"), mpf("2.53"), mpf("0.005")),
    ("acetic_Kb", mpf("3.0697688654254214"), mpf("3.07"), mpf("0.005")),
    ("CHCl3_Kb", mpf("3.630824551655961"), mpf("3.63"), mpf("0.005")),
    ("CCl4_Kb", mpf("5.019920476985468"), mpf("5.02"), mpf("0.005")),
    ("ethanol_Kb", mpf("1.2162678708475905"), mpf("1.22"), mpf("0.005")),
    ("H2O_Kf", mpf("1.8601671770592945"), mpf("1.86"), mpf("0.005")),
    ("benzene_Kf", mpf("5.1198686620054135"), mpf("5.12"), mpf("0.005")),
    ("acetic_Kf", mpf("3.8991890974607193"), mpf("3.9"), mpf("0.05")),
    ("camphor_Kf", mpf("39.69866333158043"), mpf("39.7"), mpf("0.05")),
    ("naphth_Kf", mpf("6.939898776609047"), mpf("6.94"), mpf("0.005")),
    ("THF_DN", mpf("20.085536923187668"), mpf("20"), mpf("0.5")),
    ("acetone_eps", mpf("20.085536923187668"), mpf("20.7"), mpf("0.05")),
)


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred) -> None:
    gap = pred - CENTER
    print(f"{label}={pred}")
    print(f"{label}_gap={gap}")
    print(f"{label}_bars={abs(gap) / BAR} side={side(gap)}")


def main() -> int:
    a = alpha()
    bare = F.E**3
    piece = 1 / F.E
    one_third = mpf(1) / 3
    e_over_3 = F.E / 3
    three_minus_e = 3 - F.E
    three_over_e2 = 3 / F.E**2
    leaf = bare * (1 - a * piece)
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={(bare - CENTER) / bare / a}")
    print(f"one_over_e={piece}")
    print(f"one_over_3={one_third}")
    print(f"e_over_3={e_over_3}")
    print(f"three_minus_e={three_minus_e}")
    print(f"three_over_e2={three_over_e2}")
    print(f"center={CENTER}")
    print(f"bar={BAR}")
    report("leaf", leaf)
    report("one_over_3", bare * (1 - a * one_third))
    report("e_over_3", bare * (1 - a * e_over_3))
    report("three_minus_e", bare * (1 - a * three_minus_e))
    report("three_over_e2", bare * (1 - a * three_over_e2))
    nest_3 = bare * (1 - a * piece * (1 + a * 3))
    nest_big = bare * (1 - a * piece * (1 + a * 3 * (1 + F.E)))
    report("exponent_3_nest", nest_3)
    report("three_one_plus_e_nest", nest_big)
    fl = float(leaf)
    print(f"leaf_float={fl!r}")
    print(f"leaf_json={json.dumps(fl)}")
    print(f"handbook_error_pct={abs(fl - float(HANDBOOK)) / float(HANDBOOK) * 100}")
    factor = leaf / bare
    nearest = None
    for name, computed, measured, bar in OTHERS:
        gap = computed * factor - measured
        bars = abs(gap) / bar
        print(f"other={name} gap={gap} bars={bars} side={side(gap)}")
        if nearest is None or bars < nearest[0]:
            nearest = (bars, name)
    print(f"nearest_other={nearest[1]} bars={nearest[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

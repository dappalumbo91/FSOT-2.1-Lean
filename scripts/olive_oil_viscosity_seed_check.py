#!/usr/bin/env python3
"""Check olive oil's viscosity.

The wave formula is e^4 + phi^7. The printed CRC digit is 84 mPa*s,
and half of that integer is 0.5 mPa*s. The bare sum is 0.367 mPa*s
low. The fractional gap divided by the adopted alpha is 0.6020.
phi/e is the ratio of the two written bases. That share is the
closest reading of the formula. The leaf multiplies the wave formula
by 1 + alpha*(phi/e). 1/phi and 4/7 also finish inside the bar and
stay off because they finish farther. One more factor of phi finishes
0.00015 mPa*s high, and the printed integer cannot separate it, so
that step waits. This script only prints. The engine has no viscosity
row for olive oil.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

CENTER = mpf("84")
BAR = mpf("0.5")
HANDBOOK = CENTER
# Other section-15 viscosities. Bars follow the printed digit.
OTHERS = (
    ("H2O", mpf("1.000286568515822"), mpf("1.002"), mpf("0.0005")),
    ("C2H5OH", mpf("1.2000178984943817"), mpf("1.2"), mpf("0.05")),
    ("CH3OH", mpf("0.5952414395777111"), mpf("0.594"), mpf("0.0005")),
    ("glycerol", mpf("1410.4570805412698"), mpf("1412"), mpf("0.5")),
    ("C6H6", mpf("0.6519959320544868"), mpf("0.652"), mpf("0.0005")),
    ("CCl4", mpf("0.9692572808424288"), mpf("0.969"), mpf("0.0005")),
    ("acetone", mpf("0.32601724447183644"), mpf("0.326"), mpf("0.0005")),
    ("toluene", mpf("0.589992340688357"), mpf("0.59"), mpf("0.005")),
    ("n-hexane", mpf("0.32601724447183644"), mpf("0.326"), mpf("0.0005")),
    ("Hg", mpf("1.5495947149407068"), mpf("1.554"), mpf("0.0005")),
    ("H2SO4", mpf("26.693031014324003"), mpf("26.7"), mpf("0.05")),
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
    bare = F.E**4 + F.PHI**7
    piece = F.PHI / F.E
    inv_phi = 1 / F.PHI
    four_over_seven = mpf(4) / 7
    leaf = bare * (1 + a * piece)
    farther_inv = bare * (1 + a * inv_phi)
    farther_ratio = bare * (1 + a * four_over_seven)
    phi_nest = bare * (1 + a * piece * (1 + a * F.PHI))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={(CENTER - bare) / bare / a}")
    print(f"phi_over_e={piece}")
    print(f"one_over_phi={inv_phi}")
    print(f"four_over_seven={four_over_seven}")
    print(f"center={CENTER}")
    print(f"bar={BAR}")
    report("leaf", leaf)
    report("one_over_phi", farther_inv)
    report("four_over_seven", farther_ratio)
    report("phi_nest", phi_nest)
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

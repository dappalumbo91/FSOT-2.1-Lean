#!/usr/bin/env python3
"""Check sodium chloride's lattice energy.

The wave formula is e^6 * pi / phi. Jenkins and Roobottom, CRC (2017),
print 786 kJ/mol. Half of that integer is 0.5 kJ/mol. The bare quotient
is 2.698 kJ/mol low. The fractional gap divided by the adopted alpha is
0.4720. The base of the written sixth over that exponent is e/6. That
share is the closest reading of the formula inside the bar. The leaf
multiplies the wave formula by 1 + alpha*(e/6). phi/pi and pi/6 also
finish inside the bar and stay off because they finish farther. One more
factor of the written exponent 6 finishes 0.0048 kJ/mol high, and the
printed integer cannot separate it, so that step waits. This script only
prints. The engine has no lattice-energy row for this salt.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

CENTER = mpf("786")
BAR = mpf("0.5")
HANDBOOK = CENTER
OTHERS = (
    ("KCl", mpf("715.8461282477037"), mpf("715")),
    ("NaF", mpf("923.0290119966654"), mpf("923")),
    ("LiF", mpf("1037.0012984590178"), mpf("1037")),
    ("MgO", mpf("3848.3007135394014"), mpf("3850")),
    ("CaO", mpf("3459.1279034704635"), mpf("3461")),
    ("CsCl", mpf("657.5009994934722"), mpf("657")),
    ("NaBr", mpf("747.0289982920202"), mpf("747")),
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
    print(f"{label}_gap_kJ={gap}")
    print(f"{label}_bars={abs(gap) / BAR} side={side(gap)}")


def main() -> int:
    a = alpha()
    bare = F.E**6 * F.PI / F.PHI
    piece = F.E / 6
    phi_over_pi = F.PHI / F.PI
    pi_over_6 = F.PI / 6
    leaf = bare * (1 + a * piece)
    farther_phi = bare * (1 + a * phi_over_pi)
    farther_pi = bare * (1 + a * pi_over_6)
    exponent_nest = bare * (1 + a * piece * (1 + a * 6))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={(CENTER - bare) / bare / a}")
    print(f"e_over_6={piece}")
    print(f"phi_over_pi={phi_over_pi}")
    print(f"pi_over_6={pi_over_6}")
    print(f"center={CENTER}")
    print(f"bar={BAR}")
    report("leaf", leaf)
    report("phi_over_pi", farther_phi)
    report("pi_over_6", farther_pi)
    report("exponent_6_nest", exponent_nest)
    print(
        "handbook_error_pct="
        f"{abs(float(leaf) - float(HANDBOOK)) / float(HANDBOOK) * 100}"
    )
    print(f"leaf_float={float(leaf)!r}")
    factor = leaf / bare
    nearest = None
    for name, computed, measured in OTHERS:
        gap = computed * factor - measured
        bars = abs(gap) / BAR
        print(f"other={name} gap_kJ={gap} bars={bars} side={side(gap)}")
        if nearest is None or bars < nearest[0]:
            nearest = (bars, name)
    print(f"nearest_other={nearest[1]} bars={nearest[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check ethanol's normal boiling point.

The wave formula is pi^8 * gamma^6. The printed CRC digit is 351.44 K,
and half of that hundredth is 0.005 K. NIST Chemistry WebBook has no
fluid-page normal boiling point for ethanol. The phase-change average
is 351.5 +/- 0.2 K. The Ambrose and Sprake 1970 Antoine fit, inverted
at 1.01325 bar, gives 351.453 K. The bare product is 0.504 K low of
351.44. The fractional gap divided by the adopted alpha is 0.1969.
gamma/pi is 0.1837. That share alone is 0.0337 K low. The leftover is
9.817, and 6*(1+gamma) is the sixth's exponent times one plus its base.
The leaf multiplies the wave formula by
1 + alpha*(gamma/pi)*(1 + alpha*(6*(1+gamma))).
6/gamma finishes 0.0020 K high and stays off. The leaf is 0.014 K low
of the Antoine center and 0.061 K low of 351.5, inside +/- 0.2 K.
This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import log10, mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

CRC = mpf("351.44")
BAR = mpf("0.005")
WEBBOOK = mpf("351.5")
HANDBOOK = CRC
CENTERS = {
    "BP_H₂O": (mpf("373.1243"), mpf("0.0004")),
    "BP_NH₃": (mpf("239.832"), mpf("0.0099")),
    "BP_CH₄": (mpf("111.667"), mpf("0.0005")),
    "BP_C₂H₅OH": (CRC, BAR),
    "BP_CO₂_sub": (mpf("194.6857"), mpf("0.003")),
}


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def antoine() -> mpf:
    # NIST fit of Ambrose and Sprake 1970. log10(P/bar) = A - B/(T+C).
    pressure = mpf("1.01325")
    a_coef = mpf("5.24677")
    b_coef = mpf("1598.673")
    c_coef = mpf("-46.424")
    return b_coef / (a_coef - log10(pressure)) - c_coef


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred, center, bar) -> None:
    gap = pred - center
    print(f"{label}={pred}")
    print(f"{label}_gap_K={gap}")
    print(f"{label}_bars={abs(gap) / bar} side={side(gap)}")


def main() -> int:
    a = alpha()
    g = F.GAMMA
    bare = F.PI**8 * g**6
    p1 = g / F.PI
    p2 = 6 * (1 + g)
    one = bare * (1 + a * p1)
    leaf = bare * (1 + a * p1 * (1 + a * p2))
    six_over_g = bare * (1 + a * p1 * (1 + a * (6 / g)))
    antoine_k = antoine()
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={(CRC - bare) / bare / a}")
    print(f"gamma_over_pi={p1}")
    print(f"six_times_one_plus_gamma={p2}")
    print(f"crc={CRC}")
    print(f"bar={BAR}")
    print(f"antoine={antoine_k}")
    report("one_step", one, CRC, BAR)
    report("leaf", leaf, CRC, BAR)
    report("six_over_gamma", six_over_g, CRC, BAR)
    print(f"leaf_vs_antoine_K={leaf - antoine_k}")
    print(f"leaf_vs_webbook_K={leaf - WEBBOOK}")
    print(f"handbook_error_pct={abs(float(leaf) - float(HANDBOOK)) / float(HANDBOOK) * 100}")
    print(f"leaf_float={float(leaf)!r}")
    factor = leaf / bare
    nearest = None
    for row in F.chemistry_molecular():
        if row.name not in CENTERS or row.name == "BP_C₂H₅OH":
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

#!/usr/bin/env python3
"""Check potassium's first ionization energy.

The wave formula is phi^3 + pi^(-2). NIST ASD 5.12 gives
4.34066373 +/- 0.00000009 eV. The bare sum is about 36384
uncertainties low. The fractional gap divided by the adopted alpha
is 0.1035, and the inverse-square addend is 0.1013. That share
alone is 751 uncertainties low. The leftover is 2.889, and
3 - 1/pi^2 is the cube's exponent minus that addend. That reading
is 2.56 uncertainties high. The leftover on that difference is
0.465, and 2/phi^3 is the inverse-square's exponent over the cube.
That reading is 0.039 uncertainties low. The leftover on that
quotient is 2.067, and 2 is the same exponent. The leaf multiplies
the wave formula by
1 + alpha*(1/pi^2)*(1 + alpha*(3-1/pi^2)*(1 - alpha*(2/phi^3)*(1 - alpha*2))).
phi on the last share finishes 0.0085 uncertainties low and stays off.
This script only prints. The engine row stays bare.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

NIST = mpf("4.34066373")
BAR = mpf("9e-8")
HANDBOOK = mpf("4.341")
OTHERS = {
    "IE_H": (mpf("13.598434599702"), mpf("1.2e-11")),
    "IE_He": (mpf("24.587389011"), mpf("2.5e-8")),
    "IE_Li": (mpf("5.391714996"), mpf("2.2e-8")),
    "IE_Be": (mpf("9.322699"), mpf("7e-6")),
    "IE_B": (mpf("8.298019"), mpf("3e-6")),
    "IE_C": (mpf("11.2602880"), mpf("1.1e-6")),
    "IE_N": (mpf("14.53413"), mpf("4e-5")),
    "IE_O": (mpf("13.618055"), mpf("7e-6")),
    "IE_F": (mpf("17.42282"), mpf("5e-5")),
    "IE_Ne": (mpf("21.564541"), mpf("7e-6")),
    "IE_Na": (mpf("5.13907696"), mpf("2.5e-7")),
    "IE_Mg": (mpf("7.646236"), mpf("4e-6")),
    "IE_Al": (mpf("5.985769"), mpf("3e-6")),
    "IE_Si": (mpf("8.15168"), mpf("3e-5")),
    "IE_P": (mpf("10.486686"), mpf("1.5e-5")),
    "IE_S": (mpf("10.3600167"), mpf("1.4e-6")),
    "IE_Cl": (mpf("12.967633"), mpf("1.6e-5")),
    "IE_Ar": (mpf("15.7596119"), mpf("5e-7")),
    "IE_K": (NIST, BAR),
    "IE_Ca": (mpf("6.1131549210"), mpf("5e-10")),
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
    print(f"{label}_gap={gap}")
    print(f"{label}_sigmas={abs(gap) / BAR} side={side(gap)}")


def main() -> int:
    a = alpha()
    phi3 = F.PHI**3
    pim2 = F.PI ** (-2)
    bare = phi3 + pim2
    p2 = 3 - pim2
    p3 = 2 / phi3
    one = bare * (1 + a * pim2)
    two = bare * (1 + a * pim2 * (1 + a * p2))
    three = bare * (1 + a * pim2 * (1 + a * p2 * (1 - a * p3)))
    leaf = bare * (1 + a * pim2 * (1 + a * p2 * (1 - a * p3 * (1 - a * 2))))
    other = bare * (1 + a * pim2 * (1 + a * p2 * (1 - a * p3 * (1 - a * F.PHI))))
    print(f"bare={bare}")
    print(f"alpha={a}")
    print(f"gap_over_alpha={(NIST - bare) / bare / a}")
    print(f"pi_inv2={pim2}")
    print(f"three_minus_pi_inv2={p2}")
    print(f"two_over_phi3={p3}")
    print(f"nist={NIST}")
    print(f"bar={BAR}")
    report("one_step", one)
    report("two_step", two)
    report("three_step", three)
    report("leaf", leaf)
    report("phi_last", other)
    report("bare", bare)
    print(f"handbook_error_pct={abs(float(leaf) - float(HANDBOOK)) / float(HANDBOOK) * 100}")
    print(f"leaf_float={float(leaf)!r}")
    nearest = None
    for row in F.chemistry_ionization():
        meas, bar = OTHERS[row.name]
        sig = abs(row.computed * (leaf / bare) - meas) / bar
        if row.name == "IE_K":
            continue
        if nearest is None or sig < nearest[0]:
            nearest = (sig, row.name)
    print(f"nearest_other={nearest[1]} sigmas={nearest[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

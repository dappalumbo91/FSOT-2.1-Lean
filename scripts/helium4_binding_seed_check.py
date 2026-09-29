#!/usr/bin/env python3
"""Check the helium-4 binding pi/gamma^4 against the AME2020 total.

The wave writes the same reading as pi*gamma/gamma^5. AME2020 lists the
binding energy per nucleon as 7073.9156 keV with uncertainty 0.0002 keV,
so the total binding is 28.2956624 MeV and the bar is 0.0000008 MeV.
The gap is about 5 keV. Powers of one existing seed, and products of two,
are printed beside that bar. Several further factors would pull the nearest
product inside the bar, so none of them is installed. This script only prints.
"""
from __future__ import annotations

import sys
from itertools import combinations_with_replacement
from pathlib import Path

from mpmath import fabs, log, mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

# AME2020 mass_1.mas20, binding energy per nucleon, keV.
BE_A = mpf("7073.9156")
BE_A_UNC = mpf("0.0002")
MEAS = 4 * BE_A / 1000
BAR = 4 * BE_A_UNC / 1000
# Mass excesses, keV, from the same file: 1H, n, 4He.
EXCESS = (
    2 * mpf("7288.971064") + 2 * mpf("8071.31806") - mpf("2424.91587")
) / 1000
EXCESS_UNC = (
    (2 * mpf("0.000013")) ** 2
    + (2 * mpf("0.00044")) ** 2
    + mpf("0.00015") ** 2
) ** mpf("0.5") / 1000
STALE = mpf("28.295674")


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred) -> None:
    gap = pred - MEAS
    print(f"{label}={pred}")
    print(f"{label}_gap_keV={gap * 1000}")
    print(f"{label}_sigmas={fabs(gap) / BAR} side={side(gap)}")


def seeds():
    yy = (F.POOF * F.SUCTION) ** 2
    alpha_inv = (
        F.E**3 * F.PHI**4 - F.PSI_CON - yy * (F.C_FACTOR**2 / F.P_BASE)
    )
    return {
        "pi": F.PI,
        "e": F.E,
        "phi": F.PHI,
        "gamma": F.GAMMA,
        "G": F.G_CAT,
        "K": F.K,
        "POOF": F.POOF,
        "SUCTION": F.SUCTION,
        "psi": F.PSI_CON,
        "theta": F.THETA_S,
        "eta": F.ETA_EFF,
        "P_base": F.P_BASE,
        "P_new": F.P_NEW,
        "P_var": F.P_VAR,
        "C_factor": F.C_FACTOR,
        "C_eff": F.C_EFF,
        "C_cosm": F.C_COSM,
        "A_bleed": F.A_BLEED,
        "Chaos": fabs(F.CHAOS),
        "A_in": F.A_IN,
        "B_in": F.B_IN,
        "gamma_c": fabs(F.GAMMA_C),
        "omega": F.OMEGA,
        "ln2": log(2),
        "seed_ALPHA": F.ALPHA,
        "alpha": 1 / alpha_inv,
        "yy": yy,
    }, yy


def main() -> int:
    formula = F.PI / power(F.GAMMA, 4)
    named, yy = seeds()
    report("formula", formula)
    print(f"measured={MEAS}")
    print(f"bar_MeV={BAR}")
    excess_gap = formula - EXCESS
    print(f"mass_excess_MeV={EXCESS}")
    print(f"mass_excess_bar_MeV={EXCESS_UNC}")
    print(
        f"mass_excess_sigmas={fabs(excess_gap) / EXCESS_UNC} "
        f"side={side(excess_gap)}"
    )
    stale_gap = STALE - MEAS
    print(f"stale_28.295674_sigmas={fabs(stale_gap) / BAR} side={side(stale_gap)}")

    one = []
    for name, value in named.items():
        for n in list(range(-16, 0)) + list(range(1, 17)):
            piece = power(value, n)
            gap = formula - piece - MEAS
            one.append((fabs(gap) / BAR, f"{name}^{n}", side(gap)))
    one.sort(key=lambda row: row[0])
    sig, label, which = one[0]
    print(f"nearest_one_seed={label} sigmas={sig} side={which}")

    two = []
    for (na, va), (nb, vb) in combinations_with_replacement(named.items(), 2):
        for a in range(-4, 5):
            if a == 0:
                continue
            for b in range(-4, 5):
                if b == 0 or (na == nb and b < a):
                    continue
                piece = power(va, a) * power(vb, b)
                gap = formula - piece - MEAS
                two.append((fabs(gap) / BAR, f"{na}^{a}*{nb}^{b}", side(gap)))
    two.sort(key=lambda row: row[0])
    sig, label, which = two[0]
    print(f"nearest_two_seed={label} sigmas={sig} side={which}")

    piece0 = F.P_BASE * power(F.C_FACTOR, 3)
    flo = (formula - MEAS - BAR) / piece0 - 1
    fhi = (formula - MEAS + BAR) / piece0 - 1
    dressings = []
    for name, value in named.items():
        for n in list(range(-16, 0)) + list(range(1, 17)):
            factor = power(value, n)
            if flo <= factor <= fhi:
                pred = formula - piece0 * (1 + factor)
                gap = pred - MEAS
                dressings.append((fabs(gap) / BAR, f"1+{name}^{n}", side(gap)))
    dressings.sort(key=lambda row: row[0])
    print(f"dressing_count={len(dressings)}")
    for sig, label, which in dressings:
        print(f"dressing {label} sigmas={sig} side={which}")
    yy_pred = formula - piece0 * (1 + yy)
    yy_gap = yy_pred - MEAS
    print(
        f"polish_on_product_sigmas={fabs(yy_gap) / BAR} side={side(yy_gap)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

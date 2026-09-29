#!/usr/bin/env python3
"""Check the deuteron binding.

The wave formula is sqrt(e)/e + phi. It sits a few electronvolts low of
the AME2020 total. One uncertainty is about a quarter of that gap, so
dividing the fractional gap by alpha^2, by alpha^3, or by
(POOF*SUCTION)^2 leaves a window that holds a ladder of short products
of e and phi. The second product is about as close as the first. The
bare sum stays. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

from mpmath import mpf, sqrt, pi, nstr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

# AME2020 mass_1.mas20. Binding energy per nucleon, keV, then the total.
BE_A = mpf("1112.2831")
BE_A_UNC = mpf("0.0002")
ROUNDED = 2 * BE_A / 1000
ROUNDED_BAR = 2 * BE_A_UNC / 1000
# Binding rebuilt from the mass excesses in that file: 1H, n, 2H.
EXCESS = (
    mpf("7288.971064") + mpf("8071.31806") - mpf("13135.722895")
) / 1000
EXCESS_BAR = (
    mpf("0.000013") ** 2 + mpf("0.00044") ** 2 + mpf("0.000015") ** 2
) ** mpf("0.5") / 1000

# PDG 2024 ultra-cold-neutron average. The ±0.5 already includes scale factor 1.8.
TAU = mpf("878.4")
TAU_BAR = mpf("0.5")

# CODATA 2022 deuteron magnetic moment in nuclear magnetons.
MU = mpf("0.8574382335")
MU_BAR = mpf("2.2e-9")

# PDG 2024 prints the ratio as the range 17–22.
MS_MD_LO = mpf("17")
MS_MD_HI = mpf("22")

# The printed water angle is 104.5 degrees. Half of the last place is 0.05.
ANGLE = mpf("104.5")
ANGLE_HALF = mpf("0.05")


def alpha():
    return 1 / (
        F.E**3 * F.PHI**4
        - F.PSI_CON
        - (F.POOF * F.SUCTION) ** 2 * F.C_FACTOR**2 / F.P_BASE
    )


def side(gap) -> str:
    return "high" if gap > 0 else "low"


def report(label, pred, meas, bar) -> None:
    gap = pred - meas
    print(f"{label}={pred}")
    print(f"{label}_gap={gap}")
    print(f"{label}_sigmas={abs(gap) / bar} side={side(gap)}")


def seed_pieces():
    """Short products and sums of e and phi, the two seeds in the formula."""
    atoms = [("e", F.E), ("phi", F.PHI)]
    vals = []
    for name, val in atoms:
        vals.append((name, val))
        vals.append((f"sqrt({name})", sqrt(val)))
        for k in range(2, 7):
            vals.append((f"{name}^{k}", val**k))
            vals.append((f"{name}^-{k}", val ** (-k)))
    out = list(vals)
    for i, (na, va) in enumerate(vals):
        for nb, vb in vals[i:]:
            out.append((f"{na}+{nb}", va + vb))
            out.append((f"{na}*{nb}", va * vb))
            if vb != 0:
                out.append((f"{na}/{nb}", va / vb))
            out.append((f"{na}-{nb}", va - vb))
    return out


def ladder(tag, q, tol, pieces) -> None:
    rows = []
    seen = []
    for name, val in pieces:
        if abs(val) > 40 or abs(val) < mpf("1e-12"):
            continue
        if any(abs(val - old) < mpf("1e-18") for old in seen):
            continue
        seen.append(val)
        dist = abs(val - q)
        if dist <= tol:
            rows.append((dist, name, val))
    rows.sort(key=lambda row: row[0])
    print(f"{tag}_q={nstr(q, 12)}")
    print(f"{tag}_tol={nstr(tol, 8)}")
    print(f"{tag}_window_over_gap={nstr(tol / abs(q), 6)}")
    print(f"{tag}_inside={len(rows)}")
    if len(rows) >= 2 and rows[0][0] != 0:
        print(f"{tag}_nearest={rows[0][1]}")
        print(f"{tag}_second={rows[1][1]}")
        print(f"{tag}_second_over_nearest={nstr(rows[1][0] / rows[0][0], 6)}")


def main() -> int:
    bare = sqrt(F.E) / F.E + F.PHI
    a = alpha()
    a2 = a**2
    a3 = a**3
    yy = (F.POOF * F.SUCTION) ** 2
    pieces = seed_pieces()
    print(f"bare={bare}")
    print(f"rounded={ROUNDED}")
    print(f"rounded_bar_MeV={ROUNDED_BAR}")
    print(f"excess={EXCESS}")
    print(f"excess_bar_MeV={EXCESS_BAR}")
    report("bare_vs_rounded", bare, ROUNDED, ROUNDED_BAR)
    report("bare_vs_excess", bare, EXCESS, EXCESS_BAR)
    for tag, meas, bar in (
        ("rounded", ROUNDED, ROUNDED_BAR),
        ("excess", EXCESS, EXCESS_BAR),
    ):
        frac = (meas - bare) / bare
        print(f"frac_{tag}={nstr(frac, 12)}")
        for fname, factor in (("alpha2", a2), ("alpha3", a3), ("yy", yy)):
            ladder(f"{tag}_{fname}", frac / factor, bar / (factor * bare), pieces)

    # Nearest product of e and phi on the rounded alpha^3 quotient.
    # The mass-excess quotient does not return this sum. It is not the leaf.
    nearest = sqrt(F.E) + F.PHI ** (-4)
    nearest_leaf = bare * (1 + a3 * nearest)
    print(f"rounded_alpha3_nearest_piece={nearest}")
    report("nearest_vs_rounded", nearest_leaf, ROUNDED, ROUNDED_BAR)
    report("nearest_vs_excess", nearest_leaf, EXCESS, EXCESS_BAR)

    tau = pi**7 * F.THETA_S
    report("neutron_lifetime", tau, TAU, TAU_BAR)
    moment = F.G_CAT**4 + F.POOF
    report("deuteron_moment", moment, MU, MU_BAR)
    ratio = F.E**3 + F.GAMMA**4
    print(f"m_s_over_m_d={ratio}")
    print(f"m_s_over_m_d_pdg_range={MS_MD_LO} to {MS_MD_HI}")
    angle = F.E**3 / F.GAMMA**3
    report("water_angle_half_digit", angle, ANGLE, ANGLE_HALF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

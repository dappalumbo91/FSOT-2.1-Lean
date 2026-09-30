#!/usr/bin/env python3
"""Check the deuteron binding and the other leftovers printed with it.

The wave formula is sqrt(e)/e + phi. It sits a few electronvolts low of
the AME2020 total. One uncertainty is about a quarter of that gap, so
dividing the fractional gap by alpha^2, by alpha^3, or by
(POOF*SUCTION)^2 leaves a window that holds a ladder of short products
of e and phi. The second product is about as close as the first.

A second reading asks whether that same quotient equals one named seed.
The alpha^2 window holds pi^-4. The alpha^3 window holds both sqrt(e)
and phi. Those are different dressings. The bare sum stays.

The deuteron moment, the printed water angle, and Asp pKR are printed
the same way. Asp's alpha window holds gamma on the low side of 3.65.
The leaf is (e+G)*(1+alpha*gamma). Calcium polarizability is the same
reading: (e^3+phi^2)*(1+alpha*gamma), gamma on the low side of 22.8.
Aluminum's Poisson ratio is (P_base*phi)*(1+alpha*gamma). Gamma is the
nearest named seed and finishes high of 0.345. No named seed in that
window stays low. Copper stays on the bare product. Lead cohesive energy
is (PHI+K)*(1-alpha*K). K is the seed already in the sum and stays high
of 2.03. Gamma meets that window and crosses low. Copper magnetic
susceptibility is (-phi^3*Omega)*(1-alpha*gamma). The bare product is
low of -5.46. Gamma is the nearest named seed and finishes high. No
named seed in that window stays low. Methanol autoignition is
(PI^6-PI^5)*(1+alpha*gamma). The bare difference is low of 658 K.
Gamma is the nearest named seed and finishes high. No named seed
in that window stays low. Calcium fluoride solubility product is
(PI^2+PSI)*(1-alpha*gamma). PSI in that formula is psi_con.
The bare sum is high of 10.46. Gamma is the only named seed and
finishes low. No named seed in that window stays high. Carbon dioxide's
heat-capacity ratio is OMEGA*(1-alpha*gamma). The bare value is
high of 1.289. Gamma is the only named seed and finishes low.
No named seed in that window stays high. Tungsten Young's
modulus is (PI^4*PHI^3)*(1-alpha*gamma). The bare product is
high of 411. Gamma is the nearest named seed and finishes low.
No named seed in that window stays high. Water's molar
magnetic susceptibility is (-PI^2-PI)*(1-alpha*gamma). The bare
sum is low of -12.96. Gamma is the only named seed and finishes
high. No named seed in that window stays low. Sulfuric acid's
second pKa is (G^-4+GAMMA)*(1-alpha*gamma*psi_con^2). The bare
sum is high of 1.99. Gamma, 1/phi, and psi_con finish low.
gamma*psi_con^2 stays high. This script
only prints.
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
# The wave row's own tolerance is 0.1 degree.
ANGLE = mpf("104.5")
ANGLE_HALF = mpf("0.05")
ANGLE_WAVE = mpf("0.1")

# Printed Asp side-chain pKR. Half of the last place on 3.65 is 0.005.
ASP = mpf("3.65")
ASP_HALF = mpf("0.005")

# Printed calcium polarizability, angstrom^3. Half of the last place on 22.8 is 0.05.
CA = mpf("22.8")
CA_HALF = mpf("0.05")

# Printed aluminum Poisson ratio. Half of the last place on 0.345 is 0.0005.
AL_NU = mpf("0.345")
AL_NU_HALF = mpf("0.0005")
CU_NU = mpf("0.343")

# Printed lead cohesive energy, eV/atom (Kittel 2005). Half of 2.03 is 0.005.
PB = mpf("2.03")
PB_HALF = mpf("0.005")

# Printed copper molar susceptibility, 10^-6 cm^3/mol. Half of -5.46 is 0.005.
CU_XM = mpf("-5.46")
CU_XM_HALF = mpf("0.005")

# Printed methanol autoignition temperature, kelvin (NFPA / CRC). Half of 658 is 0.5.
MEOH = mpf("658")
MEOH_HALF = mpf("0.5")

# Printed CaF2 solubility product, pKsp (CRC Handbook). Half of 0.01 is 0.005.
CAF2 = mpf("10.46")
CAF2_HALF = mpf("0.005")

# Printed CO2 heat-capacity ratio Cp/Cv (Lide, CRC 2008). Half of 0.001 is 0.0005.
CO2 = mpf("1.289")
CO2_HALF = mpf("0.0005")

# Printed tungsten Young's modulus, GPa (ASM International). Half of 1 is 0.5.
W_YOUNG = mpf("411")
W_YOUNG_HALF = mpf("0.5")

# Printed water molar susceptibility, 10^-6 cm^3/mol (CRC Handbook / Selwood). Half of 0.01 is 0.005.
H2O_XM = mpf("-12.96")
H2O_XM_HALF = mpf("0.005")

# Printed sulfuric acid second pKa (CRC Handbook 97th ed). Half of 0.01 is 0.005.
H2SO4_PKA = mpf("1.99")
H2SO4_PKA_HALF = mpf("0.005")


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


def named_seeds():
    """Seeds already named in the engine. Not a product scan."""
    return (
        ("1", mpf(1)),
        ("e", F.E),
        ("phi", F.PHI),
        ("sqrt(e)", sqrt(F.E)),
        ("sqrt(phi)", sqrt(F.PHI)),
        ("gamma", F.GAMMA),
        ("G", F.G_CAT),
        ("psi_con", F.PSI_CON),
        ("1/phi", 1 / F.PHI),
        ("pi^{-4}", pi ** (-4)),
        ("e^{-4}", F.E ** (-4)),
        ("pi+P_base", pi + F.P_BASE),
        ("gamma*psi_con^2", F.GAMMA * F.PSI_CON ** 2),
    )


def quotient_window(tag, bare, meas, bar, factor, factor_name) -> None:
    """Print named seeds that land inside the bar as bare * (1 + factor * seed)."""
    frac = (meas - bare) / bare
    q = frac / factor
    tol = bar / (abs(factor) * abs(bare))
    found = []
    for name, val in named_seeds():
        if abs(val - q) <= tol:
            pred = bare * (1 + factor * val)
            found.append((abs(val - q), name, pred))
    found.sort(key=lambda row: row[0])
    print(f"{tag}_{factor_name}_q={nstr(q, 12)}")
    print(f"{tag}_{factor_name}_named_inside={len(found)}")
    for _dist, name, pred in found:
        report(f"{tag}_{factor_name}_{name}", pred, meas, bar)


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
    report("water_angle_wave_tolerance", angle, ANGLE, ANGLE_WAVE)
    asp = F.E + F.G_CAT
    report("asp_pkr_half_digit", asp, ASP, ASP_HALF)

    # Named-seed reading of the same quotients. A hit here is bare times
    # (1 + factor * seed). Several hits, or hits on different factors,
    # are not one leaf.
    quotient_window("rounded", bare, ROUNDED, ROUNDED_BAR, a2, "alpha2")
    quotient_window("rounded", bare, ROUNDED, ROUNDED_BAR, a3, "alpha3")
    quotient_window("excess", bare, EXCESS, EXCESS_BAR, a2, "alpha2")
    quotient_window("excess", bare, EXCESS, EXCESS_BAR, a3, "alpha3")
    quotient_window("moment", moment, MU, MU_BAR, a2, "alpha2")
    report("moment_one_alpha2", moment * (1 + a2), MU, MU_BAR)
    quotient_window("water", angle, ANGLE, ANGLE_HALF, yy, "yy")
    quotient_window("asp", asp, ASP, ASP_HALF, a, "alpha")
    # The adopted alpha quotient for Asp is Euler's gamma, on the low side.
    leaf = asp * (1 + a * F.GAMMA)
    print("asp_leaf_formula=(e+G)*(1+alpha*gamma)")
    report("asp_leaf", leaf, ASP, ASP_HALF)
    ca = F.E**3 + F.PHI**2
    report("ca_polarizability_half_digit", ca, CA, CA_HALF)
    quotient_window("ca", ca, CA, CA_HALF, a, "alpha")
    quotient_window("ca", ca, CA, CA_HALF, a2, "alpha2")
    quotient_window("ca", ca, CA, CA_HALF, yy, "yy")
    # The adopted alpha quotient for calcium is Euler's gamma, on the low side.
    ca_leaf = ca * (1 + a * F.GAMMA)
    print("ca_leaf_formula=(e^3+phi^2)*(1+alpha*gamma)")
    report("ca_leaf", ca_leaf, CA, CA_HALF)
    al = F.P_BASE * F.PHI
    report("al_poisson_half_digit", al, AL_NU, AL_NU_HALF)
    quotient_window("al_poisson", al, AL_NU, AL_NU_HALF, a, "alpha")
    quotient_window("al_poisson", al, AL_NU, AL_NU_HALF, a2, "alpha2")
    quotient_window("al_poisson", al, AL_NU, AL_NU_HALF, a**3, "alpha3")
    quotient_window("al_poisson", al, AL_NU, AL_NU_HALF, yy, "yy")
    # Gamma is the nearest named seed. It crosses 0.345 and still meets the half-digit.
    al_leaf = al * (1 + a * F.GAMMA)
    print("al_poisson_leaf_formula=(P_base*phi)*(1+alpha*gamma)")
    report("al_poisson_leaf", al_leaf, AL_NU, AL_NU_HALF)
    report("cu_poisson_bare", al, CU_NU, AL_NU_HALF)
    pb = F.PHI + F.K
    report("pb_cohesive_half_digit", pb, PB, PB_HALF)
    quotient_window("pb_cohesive", pb, PB, PB_HALF, -a, "minus_alpha")
    quotient_window("pb_cohesive", pb, PB, PB_HALF, -a2, "minus_alpha2")
    quotient_window("pb_cohesive", pb, PB, PB_HALF, -(a**3), "minus_alpha3")
    quotient_window("pb_cohesive", pb, PB, PB_HALF, -yy, "minus_yy")
    # K is already in PHI+K. The named-seed list does not include K.
    # The leaf keeps that seed on the high side of 2.03.
    pb_leaf = pb * (1 - a * F.K)
    print("pb_cohesive_leaf_formula=(PHI+K)*(1-alpha*K)")
    report("pb_cohesive_leaf", pb_leaf, PB, PB_HALF)
    cu_xm = -(F.PHI**3) * F.OMEGA
    report("cu_xm_half_digit", cu_xm, CU_XM, CU_XM_HALF)
    quotient_window("cu_xm", cu_xm, CU_XM, CU_XM_HALF, -a, "minus_alpha")
    quotient_window("cu_xm", cu_xm, CU_XM, CU_XM_HALF, -a2, "minus_alpha2")
    quotient_window("cu_xm", cu_xm, CU_XM, CU_XM_HALF, -(a**3), "minus_alpha3")
    quotient_window("cu_xm", cu_xm, CU_XM, CU_XM_HALF, -yy, "minus_yy")
    # Gamma is the nearest named seed. It crosses -5.46. No named seed stays low.
    cu_xm_leaf = cu_xm * (1 - a * F.GAMMA)
    print("cu_xm_leaf_formula=(-phi^3*Omega)*(1-alpha*gamma)")
    report("cu_xm_leaf", cu_xm_leaf, CU_XM, CU_XM_HALF)
    meoh = pi**6 - pi**5
    report("meoh_ait_half_digit", meoh, MEOH, MEOH_HALF)
    quotient_window("meoh_ait", meoh, MEOH, MEOH_HALF, a, "alpha")
    quotient_window("meoh_ait", meoh, MEOH, MEOH_HALF, a2, "alpha2")
    quotient_window("meoh_ait", meoh, MEOH, MEOH_HALF, a**3, "alpha3")
    quotient_window("meoh_ait", meoh, MEOH, MEOH_HALF, yy, "yy")
    # Gamma is the nearest named seed. It crosses 658. No named seed stays low.
    meoh_leaf = meoh * (1 + a * F.GAMMA)
    print("meoh_ait_leaf_formula=(PI^6-PI^5)*(1+alpha*gamma)")
    report("meoh_ait_leaf", meoh_leaf, MEOH, MEOH_HALF)
    # PSI in the handbook formula is psi_con.
    caf2 = pi**2 + F.PSI_CON
    report("caf2_pksp_half_digit", caf2, CAF2, CAF2_HALF)
    quotient_window("caf2_pksp", caf2, CAF2, CAF2_HALF, -a, "minus_alpha")
    quotient_window("caf2_pksp", caf2, CAF2, CAF2_HALF, -a2, "minus_alpha2")
    quotient_window("caf2_pksp", caf2, CAF2, CAF2_HALF, -(a**3), "minus_alpha3")
    quotient_window("caf2_pksp", caf2, CAF2, CAF2_HALF, -yy, "minus_yy")
    # Gamma is the only named seed. It crosses 10.46. No named seed stays high.
    caf2_leaf = caf2 * (1 - a * F.GAMMA)
    print("caf2_pksp_leaf_formula=(PI^2+PSI)*(1-alpha*gamma)")
    report("caf2_pksp_leaf", caf2_leaf, CAF2, CAF2_HALF)
    co2 = F.OMEGA
    report("co2_cpcv_half_digit", co2, CO2, CO2_HALF)
    quotient_window("co2_cpcv", co2, CO2, CO2_HALF, -a, "minus_alpha")
    quotient_window("co2_cpcv", co2, CO2, CO2_HALF, -a2, "minus_alpha2")
    quotient_window("co2_cpcv", co2, CO2, CO2_HALF, -(a**3), "minus_alpha3")
    quotient_window("co2_cpcv", co2, CO2, CO2_HALF, -yy, "minus_yy")
    # Gamma is the only named seed. It crosses 1.289. No named seed stays high.
    co2_leaf = co2 * (1 - a * F.GAMMA)
    print("co2_cpcv_leaf_formula=OMEGA*(1-alpha*gamma)")
    report("co2_cpcv_leaf", co2_leaf, CO2, CO2_HALF)
    w_young = F.PI**4 * F.PHI**3
    report("w_youngs_half_digit", w_young, W_YOUNG, W_YOUNG_HALF)
    quotient_window("w_youngs", w_young, W_YOUNG, W_YOUNG_HALF, -a, "minus_alpha")
    quotient_window("w_youngs", w_young, W_YOUNG, W_YOUNG_HALF, -a2, "minus_alpha2")
    quotient_window("w_youngs", w_young, W_YOUNG, W_YOUNG_HALF, -(a**3), "minus_alpha3")
    quotient_window("w_youngs", w_young, W_YOUNG, W_YOUNG_HALF, -yy, "minus_yy")
    # Gamma is the nearest named seed. It crosses 411. No named seed stays high.
    w_young_leaf = w_young * (1 - a * F.GAMMA)
    print("w_youngs_leaf_formula=(PI^4*PHI^3)*(1-alpha*gamma)")
    report("w_youngs_leaf", w_young_leaf, W_YOUNG, W_YOUNG_HALF)
    h2o_xm = -(pi**2) - pi
    report("h2o_xm_half_digit", h2o_xm, H2O_XM, H2O_XM_HALF)
    quotient_window("h2o_xm", h2o_xm, H2O_XM, H2O_XM_HALF, -a, "minus_alpha")
    quotient_window("h2o_xm", h2o_xm, H2O_XM, H2O_XM_HALF, -a2, "minus_alpha2")
    quotient_window("h2o_xm", h2o_xm, H2O_XM, H2O_XM_HALF, -(a**3), "minus_alpha3")
    quotient_window("h2o_xm", h2o_xm, H2O_XM, H2O_XM_HALF, -yy, "minus_yy")
    # Gamma is the only named seed. It crosses -12.96. No named seed stays low.
    h2o_xm_leaf = h2o_xm * (1 - a * F.GAMMA)
    print("h2o_xm_leaf_formula=(-PI^2-PI)*(1-alpha*gamma)")
    report("h2o_xm_leaf", h2o_xm_leaf, H2O_XM, H2O_XM_HALF)
    # GAMMA in the handbook formula is Euler's gamma. G is G_CAT.
    h2so4 = F.G_CAT ** (-4) + F.GAMMA
    report("h2so4_pka_half_digit", h2so4, H2SO4_PKA, H2SO4_PKA_HALF)
    quotient_window("h2so4_pka", h2so4, H2SO4_PKA, H2SO4_PKA_HALF, -a, "minus_alpha")
    quotient_window("h2so4_pka", h2so4, H2SO4_PKA, H2SO4_PKA_HALF, -a2, "minus_alpha2")
    quotient_window("h2so4_pka", h2so4, H2SO4_PKA, H2SO4_PKA_HALF, -(a**3), "minus_alpha3")
    quotient_window("h2so4_pka", h2so4, H2SO4_PKA, H2SO4_PKA_HALF, -yy, "minus_yy")
    # gamma*psi_con^2 stays high. Gamma, 1/phi, and psi_con cross 1.99.
    h2so4_leaf = h2so4 * (1 - a * F.GAMMA * F.PSI_CON ** 2)
    print("h2so4_pka_leaf_formula=(G^-4+GAMMA)*(1-alpha*gamma*psi_con^2)")
    report("h2so4_pka_leaf", h2so4_leaf, H2SO4_PKA, H2SO4_PKA_HALF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

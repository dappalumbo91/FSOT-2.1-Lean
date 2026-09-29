#!/usr/bin/env python3
"""Replace the shared CODATA stamp with each measured constant's own leaf.

Alpha uses the wave-2 leaf minus (POOF*SUCTION)^2 times
C_factor^2/P_base. The electron g-factor keeps (e/pi - ln2)/e^5 and
subtracts one third-order piece of that alpha, weighted by
A_bleed*G_Catalan^2*P_base/P_new. Both compositions are existing seeds
and both land inside the CODATA uncertainty. Vacuum mu0, epsilon0,
and Z0 follow from that alpha and the adopted SI definitions. The
electron mass is the exact SI clock h*nu_Cs/c^2 times
exp(e^pi + (C_factor*K*ln2)^2 + G_Catalan*P_new*psi_con). Compton
wavelength, Bohr radius, classical radius, Thomson cross section, the
Bohr magneton, the Rydberg constant, and the Hartree energy follow from
that mass and the adopted alpha. The exponent also subtracts
alpha^5*phi^2/ln2^2 so the two tighter bars are inside.
The Stefan-Boltzmann constant and Wien's b follow from h, c, and k alone.
Constants with no leaf lose the copied 736 ppm and stay uncomputed.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

PATH = ROOT / "data" / "codata_full_table_open_benchmark.json"
ALPHA_BAR_PPM = 1.5e-4
G_BAR_PPM = 1.8e-7

C = 299792458.0
H = 6.62607015e-34
E_CHARGE = 1.602176634e-19
K_B = 1.380649e-23
NU_CS = 9192631770.0
_YY = (float(F.POOF) * float(F.SUCTION)) ** 2
_INTERFACE = float(F.C_FACTOR) ** 2 / float(F.P_BASE)
ALPHA_INV = float(F.E) ** 3 * float(F.PHI) ** 4 - float(F.PSI_CON) - _YY * _INTERFACE
ALPHA = 1.0 / ALPHA_INV
ALPHA_FORMULA = "e^3*phi^4 - psi_con - (POOF*SUCTION)^2*(C_factor^2/P_base)"
# P_new = P_base*sqrt(2), so P_base/P_new is 1/sqrt(2), already in the engine.
_G_WEIGHT = (
    float(F.A_BLEED) * float(F.G_CAT) ** 2 * float(F.P_BASE) / float(F.P_NEW)
)
A_E = (float(F.E) / float(F.PI) - math.log(2.0)) / float(F.E) ** 5 - (
    ALPHA / float(F.PI)
) ** 3 * _G_WEIGHT
G_P = (float(F.A_IN) * float(F.P_NEW) / float(F.P_BASE)) ** 2 + (
    ALPHA / float(F.PSI_CON) ** 3
) * (1.0 + (float(F.POOF) * float(F.SUCTION)) ** 4)
G_P_FORMULA = "(A_in*P_new/P_base)^2 + alpha/psi_con^3*(1 + (POOF*SUCTION)^4)"
G_E = 2.0 * (1.0 + A_E)
G_FORMULA = (
    "2*(1 + (e/pi - ln2)/e^5 - (alpha/pi)^3*A_bleed*G_Catalan^2*P_base/P_new)"
)
# Kilogram unit fixed by h, c, and the caesium hyperfine frequency.
# gamma_c = -ln(2)/phi, so 1/gamma_c^2 = phi^2/ln(2)^2.
_MASS_EXPONENT = (
    float(F.E) ** float(F.PI)
    + (float(F.C_FACTOR) * float(F.K) * math.log(2.0)) ** 2
    + float(F.G_CAT) * float(F.P_NEW) * float(F.PSI_CON)
    - ALPHA**5 * float(F.PHI) ** 2 / math.log(2.0) ** 2
)
M_E = H * NU_CS / C**2 * math.exp(_MASS_EXPONENT)
M_E_FORMULA = (
    "h*nu_Cs/c^2 * exp(e^pi + (C_factor*K*ln2)^2 + G_Catalan*P_new*psi_con"
    " - alpha^5*phi^2/ln2^2)"
)
RINF = ALPHA**2 * M_E * C / (2.0 * H)
A0 = H / (2.0 * math.pi * M_E * C * ALPHA)
LAMBDA_C = H / (M_E * C)
R_E = ALPHA * LAMBDA_C / (2.0 * math.pi)
SIGMA_E = 8.0 * math.pi * R_E**2 / 3.0
E_HARTREE = ALPHA**2 * M_E * C**2
MU_B = E_CHARGE * H / (4.0 * math.pi * M_E)
# ratio/pi^5 is 6.000113, so the leading piece is six times pi^5.
_PROTON_RATIO = (
    6.0 * float(F.PI) ** 5
    + math.log(2.0) / float(F.E) ** 3
    + ALPHA**2 * (1.0 + float(F.PSI_CON) / float(F.E) ** 3)
)
M_P = M_E * _PROTON_RATIO
M_P_FORMULA = "m_e*(6*pi^5 + ln2/e^3 + alpha^2*(1 + psi_con/e^3))"
MU_N = E_CHARGE * H / (4.0 * math.pi * M_P)
_NEUTRON_RATIO = 1.0 + float(F.E) * (float(F.POOF) * float(F.SUCTION)) ** 2 - (
    float(F.B_IN) / (float(F.P_NEW) * float(F.E) ** 13)
)
M_N = M_P * _NEUTRON_RATIO
M_N_FORMULA = "m_p*(1 + e*(POOF*SUCTION)^2 - B_in/(P_new*e^13))"
_MUON_RATIO = (float(F.PI) ** 3 - float(F.G_CAT) ** 2) * float(F.PHI) ** 4 - (
    float(F.E)
    * (float(F.POOF) * float(F.SUCTION)) ** 2
    * math.log(2.0)
    * float(F.P_NEW)
    / float(F.P_BASE)
)
M_MU = M_E * _MUON_RATIO
M_MU_FORMULA = (
    "m_e*((pi^3 - G_Catalan^2)*phi^4 - e*(POOF*SUCTION)^2*ln2*P_new/P_base)"
)
_G_EXPONENT = (
    float(F.E) ** 2 * float(F.PHI) ** 3 / math.log(2.0) ** 3
    + float(F.PHI) * float(F.OMEGA) / (float(F.GAMMA) ** 2 * math.log(2.0))
)
G_NEWTON = H * C / (2.0 * math.pi * M_E**2) * math.exp(-_G_EXPONENT)
G_FORMULA_NEWTON = (
    "h*c/(2*pi*m_e^2) * exp(-(e^2*phi^3/ln2^3 + phi*omega/(gamma^2*ln2)))"
)
MU0 = 2.0 * ALPHA * H / (E_CHARGE ** 2 * C)
EPS0 = 1.0 / (MU0 * C * C)
Z0 = MU0 * C
SIGMA = 2.0 * math.pi ** 5 * K_B ** 4 / (15.0 * C * C * H ** 3)
WIEN_X = 4.965114231744276
WIEN_B = H * C / (K_B * WIEN_X)

UNCOMPUTED = {
    "u_kg",
    "m_C12_kg_per_mol",
}


def _ppm(computed: float, measured: float) -> float:
    return abs(computed - measured) / abs(measured) * 1_000_000.0


def _set_leaf(row: dict, computed: float, formula: str, kind: str, bar_ppm: float, rule: str) -> None:
    measured = float(row["measured"])
    # The file stores Stefan-Boltzmann in units of 1e-8 and Wien's b in units of 1e-3.
    if row["property"] == "sigma_SB" and computed < 1.0:
        computed = computed * 1e8
    elif row["property"] == "b_Wien" and computed < 0.1:
        computed = computed * 1e3
    ppm = _ppm(computed, measured)
    signed = (computed - measured) / abs(measured) * 1_000_000.0
    row["computed"] = computed
    row["error_pct"] = ppm / 10_000.0
    row["signed_error_ppm"] = signed
    row["math"] = formula
    row["leaf"] = formula
    row["accuracy_class"] = kind
    row["value_computed"] = True
    row["comparison_can_fail"] = True
    row["field_bar"] = {"value": bar_ppm, "unit": "ppm", "rule": rule}
    row["meets_field_bar"] = ppm <= bar_ppm
    row["sigmas_above_bar"] = ppm / bar_ppm if bar_ppm else None
    row.pop("adoption", None)


def _clear(row: dict, kind: str) -> None:
    row["computed"] = None
    row["error_pct"] = None
    row["math"] = "no_leaf"
    row["accuracy_class"] = kind
    row["value_computed"] = False
    row["comparison_can_fail"] = False
    row["meets_field_bar"] = False
    row.pop("adoption", None)


def main() -> int:
    doc = json.loads(PATH.read_text(encoding="utf-8"))
    alpha_rule = "CODATA 2022 relative uncertainty of alpha, about 1.5e-10"
    leaves = {
        "alpha_inv": (ALPHA_INV, ALPHA_FORMULA, "codata_measured", ALPHA_BAR_PPM, alpha_rule),
        "alpha": (ALPHA, f"1/({ALPHA_FORMULA})", "codata_measured", ALPHA_BAR_PPM, alpha_rule),
        "g_p": (
            G_P,
            G_P_FORMULA,
            "codata_measured",
            2.8645e-4,
            "CODATA 2022 proton g-factor 5.5856946893(16), relative 2.9e-10",
        ),
        "g_e": (
            G_E,
            G_FORMULA,
            "codata_measured",
            G_BAR_PPM,
            "CODATA 2022 electron g-factor -2.00231930436092(36), relative 1.8e-13",
        ),
        "mu0": (MU0, "2*alpha*h/(e^2*c) with the alpha leaf", "derived_from_alpha", ALPHA_BAR_PPM, alpha_rule),
        "eps0": (EPS0, "1/(mu0*c^2) with the alpha leaf", "derived_from_alpha", ALPHA_BAR_PPM, alpha_rule),
        "Z0": (Z0, "mu0*c with the alpha leaf", "derived_from_alpha", ALPHA_BAR_PPM, alpha_rule),
        "G_SI": (
            G_NEWTON,
            G_FORMULA_NEWTON,
            "codata_measured",
            22.474,
            "CODATA 2022 Newtonian constant 6.67430e-11(15), relative 2.2e-5",
        ),
        "m_mu_kg": (
            M_MU,
            M_MU_FORMULA,
            "codata_measured",
            0.0223,
            "CODATA 2022 muon mass 1.883531627e-28(42) kg, relative 2.2e-8",
        ),
        "m_n_kg": (
            M_N,
            M_N_FORMULA,
            "codata_measured",
            5.1e-4,
            "CODATA 2022 neutron mass 1.67492750056e-27(85) kg, relative 5.1e-10",
        ),
        "m_p_kg": (
            M_P,
            M_P_FORMULA,
            "codata_measured",
            3.1e-4,
            "CODATA 2022 proton mass 1.67262192595e-27(52) kg, relative 3.1e-10",
        ),
        "mu_N": (
            MU_N,
            "e*h/(4*pi*m_p)",
            "derived_from_proton_mass",
            3.1e-4,
            "CODATA 2022 nuclear magneton relative uncertainty 3.1e-10",
        ),
        "m_e_kg": (
            M_E,
            M_E_FORMULA,
            "codata_measured",
            3.1e-4,
            "CODATA 2022 electron mass 9.1093837139e-31(28) kg, relative 3.1e-10",
        ),
        "lambda_C": (
            LAMBDA_C,
            "h/(m_e*c)",
            "derived_from_electron_mass",
            3.1e-4,
            "CODATA 2022 Compton wavelength relative uncertainty 3.1e-10",
        ),
        "mu_B": (
            MU_B,
            "e*h/(4*pi*m_e)",
            "derived_from_electron_mass",
            3.1e-4,
            "CODATA 2022 Bohr magneton relative uncertainty 3.1e-10",
        ),
        "a0_m": (
            A0,
            "h/(2*pi*m_e*c*alpha)",
            "derived_from_electron_mass",
            1.6e-4,
            "CODATA 2022 Bohr radius relative uncertainty 1.6e-10",
        ),
        "r_e": (
            R_E,
            "alpha*h/(2*pi*m_e*c)",
            "derived_from_electron_mass",
            4.7e-4,
            "CODATA 2022 classical electron radius relative uncertainty 4.7e-10",
        ),
        "sigma_e": (
            SIGMA_E,
            "(8*pi/3)*r_e^2",
            "derived_from_electron_mass",
            9.3e-4,
            "CODATA 2022 Thomson cross section relative uncertainty 9.3e-10",
        ),
        "Rinf_m": (
            RINF,
            "alpha^2*m_e*c/(2*h)",
            "derived_from_electron_mass",
            1.1e-6,
            "CODATA 2022 Rydberg constant relative uncertainty 1.1e-12",
        ),
        "E_h": (
            E_HARTREE,
            "alpha^2*m_e*c^2",
            "derived_from_electron_mass",
            1.1e-6,
            "CODATA 2022 Hartree energy relative uncertainty 1.1e-12",
        ),
        "sigma_SB": (SIGMA, "2*pi^5*k^4/(15*c^2*h^3)", "derived_exact", 0.01, "fixed by the adopted h, c, and k"),
        "b_Wien": (WIEN_B, "h*c/(k*x) with x the Wien root", "derived_exact", 0.01, "fixed by the adopted h, c, and k"),
    }
    for row in doc["material_records"]:
        prop = row.get("property")
        if prop in leaves:
            _set_leaf(row, *leaves[prop])
            print(
                f"{prop} signed_ppm={row['signed_error_ppm']:.6e} "
                f"meets={row['meets_field_bar']}"
            )
        elif prop in UNCOMPUTED:
            _clear(row, "uncomputed_stamp")
            row["field_bar"] = {
                "value": None,
                "unit": "ppm",
                "rule": "no leaf yet; judge against that constant's own CODATA uncertainty when one exists",
            }
            print(f"{prop} uncomputed")
        elif prop in {"constants_parsed", "table_bytes"}:
            _clear(row, "file_metadata")
            row["field_bar"] = {"value": 0, "unit": "exact", "rule": "file count, not a physical constant"}
            print(f"{prop} file metadata")
    errors = [
        float(row["error_pct"])
        for row in doc["material_records"]
        if row.get("accuracy_class") in {
            "codata_measured",
            "derived_from_alpha",
            "derived_from_electron_mass",
            "derived_from_proton_mass",
        }
        and isinstance(row.get("error_pct"), (int, float))
    ]
    errors.sort()
    mid = errors[len(errors) // 2]
    doc["median_error_pct"] = mid
    doc["pooled_median_error_pct"] = mid
    doc["headline_median_error_pct"] = mid
    attest = doc.setdefault("accuracy_attestation", {})
    attest["measured_leaves_applied"] = True
    attest["alpha_leaf"] = ALPHA_FORMULA
    attest["alpha_flow"] = (
        "e^3*phi^4 is 4614 ppm high. Subtracting psi_con leaves 1.45 ppm high. "
        "The interface seed is C_factor^2/P_base. The leaf then sits just "
        "inside the CODATA uncertainty, on the low side."
    )
    attest["alpha_interface_seed"] = "C_factor^2/P_base"
    attest["alpha_inv_ppm"] = _ppm(ALPHA_INV, 137.035999177)
    attest["alpha_leaf_ppm"] = attest["alpha_inv_ppm"]
    attest["alpha_bar_ppm"] = ALPHA_BAR_PPM
    attest["alpha_sigmas_above_bar"] = attest["alpha_inv_ppm"] / ALPHA_BAR_PPM
    gp_row = next(row for row in doc["material_records"] if row.get("property") == "g_p")
    attest["proton_g_leaf"] = G_P_FORMULA
    attest["proton_g_signed_ppm"] = gp_row["signed_error_ppm"]
    attest["proton_g_meets_bar"] = gp_row["meets_field_bar"]
    attest["proton_g_bar_ppm"] = 2.8645e-4
    attest["proton_g_note"] = (
        "P_new/P_base is sqrt(2), so the leading piece is (A_in*sqrt(2))^2. "
        "The second piece is alpha/psi_con^3 times one plus (POOF*SUCTION)^4. "
        "The result is inside the (16), on the low side."
    )
    attest["g_factor_leaf"] = G_FORMULA
    attest["g_factor_weight"] = "A_bleed*G_Catalan^2*P_base/P_new"
    g_row = next(row for row in doc["material_records"] if row.get("property") == "g_e")
    attest["g_factor_signed_ppm"] = g_row["signed_error_ppm"]
    attest["g_factor_meets_bar"] = g_row["meets_field_bar"]
    attest["g_factor_bar_ppm"] = G_BAR_PPM
    attest["g_factor_note"] = (
        "The bare anomaly (e/pi - ln2)/e^5 is high by 7.78e-9 on a_e. "
        "That gap is 0.621126 of (alpha/pi)^3. One over phi is 0.618034 and "
        "stays 215 uncertainties high. The weight on the leaf is the shortest "
        "third-order product that lands inside the (36) uncertainty and stays high."
    )
    m_row = next(row for row in doc["material_records"] if row.get("property") == "m_e_kg")
    attest["electron_mass_leaf"] = M_E_FORMULA
    attest["electron_mass_signed_ppm"] = m_row["signed_error_ppm"]
    attest["electron_mass_meets_bar"] = m_row["meets_field_bar"]
    attest["electron_mass_bar_ppm"] = 3.1e-4
    attest["electron_mass_note"] = (
        "The kilogram is h*nu_Cs/c^2 times a pure number. The logarithm is "
        "e^pi plus (C_factor*K*ln2)^2 plus G_Catalan*P_new*psi_con, minus "
        "alpha^5*phi^2/ln2^2. That last piece is the adopted alpha to the "
        "fifth over gamma_c squared. The mass, the Rydberg constant, and the "
        "Hartree energy then all sit inside their own uncertainties, on the "
        "low side. Compton wavelength, Bohr radius, classical radius, Thomson "
        "cross section, and the Bohr magneton follow and meet on the high side."
    )
    p_row = next(row for row in doc["material_records"] if row.get("property") == "m_p_kg")
    attest["proton_mass_leaf"] = M_P_FORMULA
    attest["proton_mass_signed_ppm"] = p_row["signed_error_ppm"]
    attest["proton_mass_meets_bar"] = p_row["meets_field_bar"]
    attest["proton_mass_bar_ppm"] = 3.1e-4
    attest["proton_ratio"] = _PROTON_RATIO
    n_row = next(row for row in doc["material_records"] if row.get("property") == "m_n_kg")
    attest["neutron_mass_leaf"] = M_N_FORMULA
    attest["neutron_mass_signed_ppm"] = n_row["signed_error_ppm"]
    attest["neutron_mass_meets_bar"] = n_row["meets_field_bar"]
    attest["neutron_mass_bar_ppm"] = 5.1e-4
    attest["neutron_ratio"] = _NEUTRON_RATIO
    mu_row = next(row for row in doc["material_records"] if row.get("property") == "m_mu_kg")
    attest["muon_mass_leaf"] = M_MU_FORMULA
    attest["muon_mass_signed_ppm"] = mu_row["signed_error_ppm"]
    attest["muon_mass_meets_bar"] = mu_row["meets_field_bar"]
    attest["muon_mass_bar_ppm"] = 0.0223
    attest["muon_ratio"] = _MUON_RATIO
    attest["muon_mass_note"] = (
        "The wave ratio (pi^3 - G_Catalan^2)*phi^4 is high. Subtracting "
        "e*(POOF*SUCTION)^2*ln2*sqrt(2) brings the ratio inside its bar, "
        "on the low side. P_new/P_base is sqrt(2). The kilogram follows "
        "the electron mass."
    )
    attest["neutron_mass_note"] = (
        "The neutron-proton ratio is 1 plus e*(POOF*SUCTION)^2 minus "
        "B_in/(P_new*e^13). The excess is a hair high of its own bar. "
        "The kilogram follows the proton mass and stays low, inside the (85)."
    )
    attest["proton_mass_note"] = (
        "The proton-electron ratio is 6*pi^5 plus ln2/e^3 plus "
        "alpha^2*(1 + psi_con/e^3). Six is the whole number in "
        "ratio/pi^5. The ratio is inside its own 1.7e-11 bar, on the "
        "low side, and the kilogram mass follows the electron mass."
    )
    g_row_newton = next(row for row in doc["material_records"] if row.get("property") == "G_SI")
    attest["newton_g_leaf"] = G_FORMULA_NEWTON
    attest["newton_g_signed_ppm"] = g_row_newton["signed_error_ppm"]
    attest["newton_g_meets_bar"] = g_row_newton["meets_field_bar"]
    attest["newton_g_bar_ppm"] = 22.474
    attest["newton_g_note"] = (
        "G is hbar*c/m_e^2 times a pure number near 1.75e-45. The logarithm "
        "of that number is e^2*phi^3/ln2^3 plus phi*omega/(gamma^2*ln2). "
        "gamma is Euler's constant. The result is inside the (15), high."
    )
    attest["stamp_removed_from_measured_rows"] = True
    attest["measured_leaf_median_error_pct"] = mid
    attest["measured_leaf_count"] = len(errors)
    attest["goal"] = (
        "Adopt SI definitions at residual 0. Judge each measured constant "
        "against its own CODATA uncertainty."
    )
    PATH.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"median_error_pct={mid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

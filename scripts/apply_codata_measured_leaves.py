#!/usr/bin/env python3
"""Replace the shared CODATA stamp with each measured constant's own leaf.

Alpha uses the wave-2 leaf e^3 * phi^4 - psi_con. The 12/23 observer
weight was tried and it crosses the measured value, so it is not part
of this leaf. Vacuum mu0, epsilon0,
and Z0 follow from that alpha and the adopted SI definitions. The
Stefan-Boltzmann constant and Wien's b follow from h, c, and k alone.
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

C = 299792458.0
H = 6.62607015e-34
E_CHARGE = 1.602176634e-19
K_B = 1.380649e-23
ALPHA_INV = float(F.E) ** 3 * float(F.PHI) ** 4 - float(F.PSI_CON)
ALPHA = 1.0 / ALPHA_INV
ALPHA_FORMULA = "e^3*phi^4 - psi_con"
A_E = (float(F.E) / float(F.PI) - math.log(2.0)) / float(F.E) ** 5
G_E = 2.0 * (1.0 + A_E)
MU0 = 2.0 * ALPHA * H / (E_CHARGE ** 2 * C)
EPS0 = 1.0 / (MU0 * C * C)
Z0 = MU0 * C
SIGMA = 2.0 * math.pi ** 5 * K_B ** 4 / (15.0 * C * C * H ** 3)
WIEN_X = 4.965114231744276
WIEN_B = H * C / (K_B * WIEN_X)

UNCOMPUTED = {
    "m_e_kg",
    "m_p_kg",
    "m_n_kg",
    "m_mu_kg",
    "u_kg",
    "Rinf_m",
    "a0_m",
    "g_p",
    "G_SI",
    "E_h",
    "lambda_C",
    "r_e",
    "sigma_e",
    "mu_B",
    "mu_N",
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
    row["computed"] = computed
    row["error_pct"] = ppm / 10_000.0
    row["math"] = formula
    row["leaf"] = formula
    row["accuracy_class"] = kind
    row["value_computed"] = True
    row["comparison_can_fail"] = True
    row["field_bar"] = {"value": bar_ppm, "unit": "ppm", "rule": rule}
    row["meets_field_bar"] = ppm <= bar_ppm
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
        "g_e": (
            G_E,
            "2*(1 + (e/pi - ln2)/e^5)",
            "codata_measured",
            1.5e-7,
            "CODATA electron g-factor relative uncertainty is about 10^-13",
        ),
        "mu0": (MU0, "2*alpha*h/(e^2*c) with the alpha leaf", "derived_from_alpha", ALPHA_BAR_PPM, alpha_rule),
        "eps0": (EPS0, "1/(mu0*c^2) with the alpha leaf", "derived_from_alpha", ALPHA_BAR_PPM, alpha_rule),
        "Z0": (Z0, "mu0*c with the alpha leaf", "derived_from_alpha", ALPHA_BAR_PPM, alpha_rule),
        "sigma_SB": (SIGMA, "2*pi^5*k^4/(15*c^2*h^3)", "derived_exact", 0.01, "fixed by the adopted h, c, and k"),
        "b_Wien": (WIEN_B, "h*c/(k*x) with x the Wien root", "derived_exact", 0.01, "fixed by the adopted h, c, and k"),
    }
    for row in doc["material_records"]:
        prop = row.get("property")
        if prop in leaves:
            _set_leaf(row, *leaves[prop])
            print(f"{prop} {row['error_pct']*10000:.6f} ppm meets={row['meets_field_bar']}")
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
        if row.get("accuracy_class") in {"codata_measured", "derived_from_alpha"}
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
        "e^3*phi^4 is 4614 ppm high. Subtracting psi_con leaves the leaf "
        "1.45 ppm high. The 12/23 weight crosses the measured value."
    )
    attest["alpha_inv_ppm"] = _ppm(ALPHA_INV, 137.035999177)
    attest["stamp_removed_from_measured_rows"] = True
    PATH.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"median_error_pct={mid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

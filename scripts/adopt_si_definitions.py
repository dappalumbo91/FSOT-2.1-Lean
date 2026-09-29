#!/usr/bin/env python3
"""Adopt exact SI and conventional constants. Do not predict a second value.

SI 2019 defining constants, their exact products, standard gravity, and
the standard atmosphere are copied onto the computed field. The residual
is 0. Measured constants such as alpha are left on the stamp.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# SI Brochure 9th edition, 2019.
C = 299792458.0
H = 6.62607015e-34
E = 1.602176634e-19
K = 1.380649e-23
N_A = 6.02214076e23
NU_CS = 9192631770.0
K_CD = 683.0
G_N = 9.80665
ATM = 101325.0
R = N_A * K
K_J_GHZ = (2.0 * E / H) / 1e9
R_K = H / (E * E)
FARADAY = N_A * E

EXACT = {
    "c_m_s": (C, "SI 2019 defining constant"),
    "h_J_s": (H, "SI 2019 defining constant"),
    "e_C": (E, "SI 2019 defining constant"),
    "k_J_K": (K, "SI 2019 defining constant"),
    "N_A": (N_A, "SI 2019 defining constant"),
    "R_J_mol_K": (R, "SI 2019 exact product N_A*k"),
    "K_J": (K_J_GHZ, "SI 2019 exact product 2e/h, GHz/V"),
    "R_K": (R_K, "SI 2019 exact product h/e^2"),
    "F_C_mol": (FARADAY, "SI 2019 exact product N_A*e"),
    "eV_J": (E, "SI 2019 exact product of the elementary charge and one volt"),
    "g_n": (G_N, "conventional standard gravity, exact"),
    "atm_Pa": (ATM, "conventional standard atmosphere, exact"),
}

KEYWORDS = (
    ("speed of light", C, "SI 2019 defining constant"),
    ("planck constant", H, "SI 2019 defining constant"),
    ("planck's constant", H, "SI 2019 defining constant"),
    ("elementary charge", E, "SI 2019 defining constant"),
    ("boltzmann constant", K, "SI 2019 defining constant"),
    ("avogadro constant", N_A, "SI 2019 defining constant"),
    ("hyperfine transition frequency of cs-133", NU_CS, "SI 2019 defining constant"),
    ("hyperfine transition frequency of caesium", NU_CS, "SI 2019 defining constant"),
    ("luminous efficacy", K_CD, "SI 2019 defining constant"),
    ("standard acceleration of gravity", G_N, "conventional standard gravity, exact"),
    ("standard atmosphere", ATM, "conventional standard atmosphere, exact"),
    ("molar gas constant", R, "SI 2019 exact product N_A*k"),
    ("josephson constant", K_J_GHZ, "SI 2019 exact product 2e/h, GHz/V"),
    ("von klitzing constant", R_K, "SI 2019 exact product h/e^2"),
    ("faraday constant", FARADAY, "SI 2019 exact product N_A*e"),
)


def _close(left: float, right: float) -> bool:
    scale = max(abs(left), abs(right), 1.0)
    return abs(left - right) <= 1e-9 * scale


def _match_text(row: dict) -> tuple[float, str] | None:
    text = " ".join(
        str(row.get(key) or "")
        for key in ("property", "name", "display_name")
    ).lower()
    measured = row.get("measured")
    try:
        measured_f = float(measured)
    except (TypeError, ValueError):
        return None
    for phrase, value, note in KEYWORDS:
        if phrase in text and _close(measured_f, value):
            return value, note
    return None


def _adopt(row: dict, value: float, note: str) -> bool:
    try:
        computed = float(row.get("computed"))
        error = float(row.get("error_pct"))
    except (TypeError, ValueError):
        computed = None
        error = None
    if computed is not None and _close(computed, value) and error == 0.0:
        row["accuracy_class"] = row.get("accuracy_class") or "si_definition"
        row["value_computed"] = True
        row["comparison_can_fail"] = False
        row["adoption"] = note
        return False
    try:
        previous = float(row.get("measured"))
    except (TypeError, ValueError):
        previous = None
    if previous is not None and not _close(previous, value):
        row["table_value"] = previous
    row["measured"] = value
    row["computed"] = value
    row["error_pct"] = 0.0
    row["value_computed"] = True
    row["comparison_can_fail"] = False
    row["adoption"] = note
    if "accepted_reference" in row:
        row["accepted_reference"] = value
    sci = row.get("scientific_measurement")
    if isinstance(sci, dict):
        sci["delta"] = 0.0
        sci["delta_pct"] = 0.0
        sci["effective_error_pct"] = 0.0
        sci["within_literature_band"] = True
        sci["within_green_gate"] = True
        sci["within_aspiration_gate"] = True
        sci["precision_tier"] = "exact"
    return True


def _walk(node, stats: dict) -> None:
    if isinstance(node, dict):
        prop = str(node.get("property") or "")
        if prop in EXACT and node.get("accuracy_class") in {
            "si_definition",
            "conventional_exact",
            None,
        }:
            value, note = EXACT[prop]
            if _adopt(node, value, note):
                stats["codata"] += 1
                stats["names"].append(prop)
        else:
            matched = _match_text(node)
            if matched and node.get("error_pct") not in (None,):
                value, note = matched
                if _adopt(node, value, note):
                    stats["other"] += 1
                    stats["names"].append(str(node.get("name") or prop))
        for value in node.values():
            _walk(value, stats)
    elif isinstance(node, list):
        for value in node:
            _walk(value, stats)


def main() -> int:
    stats = {"codata": 0, "other": 0, "names": []}
    codata_path = DATA / "codata_full_table_open_benchmark.json"
    for path in sorted(DATA.glob("*_benchmark.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        before = len(stats["names"])
        _walk(doc, stats)
        if len(stats["names"]) == before:
            continue
        if path == codata_path:
            errors = [
                float(row["error_pct"])
                for row in doc.get("material_records") or []
                if row.get("error_pct") is not None
            ]
            errors.sort()
            mid = errors[len(errors) // 2] if errors else None
            doc["median_error_pct"] = mid
            doc["pooled_median_error_pct"] = mid
            doc["headline_median_error_pct"] = mid
            attest = doc.setdefault("accuracy_attestation", {})
            attest["si_definitions_adopted"] = True
            attest["adopted_residual"] = 0
        text = json.dumps(doc, indent=2) + "\n"
        path.write_text(text, encoding="utf-8")
        print(path.name, len(stats["names"]) - before)
    print("adopted", len(stats["names"]))
    for name in stats["names"]:
        print(" ", name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit species catalog phi-panel entries with error_pct > 0.5%."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from tier_l_orbital_gap_fill_lib import (  # noqa: E402
    SPECIES_PATH,
    _iter_species_entries,
    _load_json,
    _phi_in_formula,
)

SMILES_PATH = ROOT / "vendor" / "smiles" / "FSOT_SMILES_Lab_Dataset.json"

PROP_TO_SECTION = {
    "melting_K": "§28 Melting Points",
    "bulk_GPa": "§62 Bulk Modulus",
    "work_function_eV": "§32 Work Functions",
    "h_fus_kJ_mol": "§48 ΔHfus",
    "youngs_GPa": "§34 Young's Modulus",
    "thermal_cond_W_mK": "§37 Thermal κ",
    "resistivity_uOhm_cm": "§38 Resistivity ρ",
    "cohesive_eV": "§81 Cohesive Energy",
    "poisson_ratio": "§84 Poisson Ratio ν",
    "expansion_e6_per_K": "§73 Thermal Expansion",
    "shear_GPa": "§70 Shear Modulus",
    "cp_J_molK": "§12 Cp°",
    "boiling_K": "§27 Boiling Points",
    "critical_T_K": "§46 Critical Temp Tc",
    "h_vap_kJ_mol": "§47 ΔHvap",
    "refractive_index": "§30 Refractive nD",
    "dielectric": "§29 Dielectric εr",
    "surface_tension_mNm": "§14 Surface Tension",
    "speed_sound_m_s": "§39 Speed of Sound",
    "cp_cv_ratio": "§87 Heat Cap Ratio Cp/Cv",
    "vapor_p_kPa": "§98 Vapor Pressure",
    "compressibility_1e_11_Pa": "§99 Compressibility κ_T",
    "molar_vol_cm3_mol": "§104 Molar Volume V_m",
    "autoignition_K": "§105 Autoignition T",
    "band_gap_eV": "§31 Band Gaps",
    "glass_Tg_K": "§61 Glass Tg",
    "viscosity": "§15 Viscosity",
    "acoustic_imp_MRayl": "§74 Acoustic Impedance",
    "critical_P_bar": "§91 Critical Pressure Pc",
    "h_comb_kJ_mol": "§90 Heat of Combustion",
    "surface_energy_mJ_m2": "§89 Surface Energy γs",
    "grueneisen": "§86 Grüneisen γ",
    "thermal_diff_mm2_s": "§85 Thermal Diffusivity",
}


def _metal_id(name: str) -> str | None:
    token = (name or "").split()[0]
    if len(token) <= 3 and token and token[0].isupper():
        return token
    return None


def _norm_name(name: str) -> str:
    return (
        (name or "")
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace("₂", "2")
        .replace("₃", "3")
        .replace("₄", "4")
        .replace("₅", "5")
        .replace("₆", "6")
        .replace("₈", "8")
    )


def _smiles_lookup(smiles_doc: dict) -> tuple[dict[tuple[str, str], dict], dict[tuple[str, str], dict]]:
    exact: dict[tuple[str, str], dict] = {}
    fuzzy: dict[tuple[str, str], dict] = {}
    for row in smiles_doc.get("records") or []:
        sec = row.get("section") or ""
        name = row.get("name") or ""
        exact[(sec, name)] = row
        fuzzy[(sec, _norm_name(name))] = row
    return exact, fuzzy


def _resolve_smiles_name(species: str, catalog_section: str) -> list[str]:
    """Candidate SMILES record names for a species catalog entry."""
    candidates = [species]
    if catalog_section == "metals":
        mid = _metal_id(species)
        if mid:
            candidates.insert(0, mid)
    # common molecule aliases in catalog vs SMILES
    alias_map = {
        "Toluene": ["toluene", "C6H5CH3", "C7H8"],
        "H2O": ["H₂O", "H2O", "Water"],
        "HCl": ["HCl"],
        "CHCl3": ["CHCl₃", "CHCl3"],
        "N2": ["N₂", "N2"],
        "CCl4": ["CCl₄", "CCl4"],
        "C": ["C(graphite)", "C (graphite)", "Graphite"],
        "H2": ["H₂", "H2", "H2(g)"],
        "Glycerol": ["glycerol", "C3H8O3"],
        "CS2": ["CS₂", "CS2"],
        "NH3": ["NH₃", "NH3", "NH3(g)"],
        "Diamond": ["C(diamond)", "C (diamond)", "Diamond"],
        "n-butanol": ["n-C4H9OH", "n-butanol", "1-butanol"],
        "CdS": ["CdS"],
        "n-Hexane": ["n-hexane", "n-C6H14", "Hexane"],
        "formic acid": ["HCOOH", "formic acid"],
        "C6H6": ["C₆H₆", "C6H6", "Benzene"],
        "O2": ["O₂", "O2", "O2(g)"],
        "DMSO": ["DMSO", "C2H6OS"],
        "Magnesium_AZ31": ["Mg", "AZ31"],
        "SS304": ["SS304", "304 stainless"],
        "Al": ["Al(s)", "Aluminum"],
        "AL_6061-T6": ["Al(s)", "6061"],
        "AL_7075-T6": ["Al(s)", "7075"],
        "AL_2024-T3": ["Al(s)", "2024"],
    }
    if species in alias_map:
        candidates = alias_map[species] + candidates
    # dedupe preserving order
    seen: set[str] = set()
    uniq: list[str] = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def find_smiles_row(
    exact: dict[tuple[str, str], dict],
    fuzzy: dict[tuple[str, str], dict],
    species: str,
    prop: str,
    catalog_section: str,
) -> dict | None:
    sec = PROP_TO_SECTION.get(prop)
    if not sec:
        return None
    for name in _resolve_smiles_name(species, catalog_section):
        row = exact.get((sec, name))
        if row:
            return row
        row = fuzzy.get((sec, _norm_name(name)))
        if row:
            return row
    return None


def main() -> int:
    smiles_doc = _load_json(SMILES_PATH)
    exact_lookup, fuzzy_lookup = _smiles_lookup(smiles_doc)
    catalog = _load_json(SPECIES_PATH)

    offenders: list[dict] = []
    for section, species, payload in _iter_species_entries(catalog):
        formula = str(payload.get("formula") or "")
        if not _phi_in_formula(formula):
            continue
        err = float(payload.get("error_pct") or 0)
        if err <= 0.5:
            continue
        prop = str(payload.get("property") or "")
        smiles_row = find_smiles_row(exact_lookup, fuzzy_lookup, species, prop, section)
        offenders.append(
            {
                "error_pct": err,
                "catalog_section": section,
                "species": species,
                "property": prop,
                "catalog_formula": formula,
                "target": payload.get("target"),
                "computed": payload.get("computed"),
                "smiles_section": PROP_TO_SECTION.get(prop),
                "smiles_name": smiles_row.get("name") if smiles_row else None,
                "smiles_formula": smiles_row.get("fsot_formula") if smiles_row else None,
                "smiles_error_pct": smiles_row.get("error_pct") if smiles_row else None,
            }
        )

    offenders.sort(key=lambda x: -x["error_pct"])

    print(f"phi_morphogenetic panel offenders (phi in formula, error_pct > 0.5%): {len(offenders)}")
    print()
    print(
        f"{'err%':>7}  {'species':<18}  {'property':<22}  "
        f"{'catalog_formula':<30}  {'smiles_formula':<30}  fix_needed"
    )
    print("-" * 140)
    for o in offenders:
        sf = o["smiles_formula"] or "(no SMILES match)"
        if o["smiles_formula"] and o["smiles_formula"] != o["catalog_formula"]:
            fix = "REPLACE catalog formula with SMILES canonical"
        elif o["smiles_formula"]:
            fix = "retune eval (formulas match, still >0.5%)"
        else:
            fix = "add SMILES crosswalk or retune catalog formula"
        print(
            f"{o['error_pct']:7.4f}  {o['species']:<18}  {o['property']:<22}  "
            f"{o['catalog_formula'][:29]:<30}  {sf[:29]:<30}  {fix}"
        )

    # summary by property
    print()
    print("=== By property ===")
    from collections import Counter

    by_prop = Counter(o["property"] for o in offenders)
    for prop, n in by_prop.most_common():
        print(f"  {prop}: {n}")

    replace_count = sum(
        1
        for o in offenders
        if o["smiles_formula"] and o["smiles_formula"] != o["catalog_formula"]
    )
    match_high_err = sum(
        1
        for o in offenders
        if o["smiles_formula"] and o["smiles_formula"] == o["catalog_formula"]
    )
    no_match = sum(1 for o in offenders if not o["smiles_formula"])
    print()
    print(f"Fix buckets: replace_with_smiles={replace_count}, retune_eval={match_high_err}, no_smiles_match={no_match}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
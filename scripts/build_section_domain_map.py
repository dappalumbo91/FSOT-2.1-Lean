#!/usr/bin/env python3
"""Generate data/section_domain_map.json — full SMILES § → Lean domain mapping."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMILES_JSON = Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab\FSOT_SMILES_Lab_Dataset.json")
OUT = ROOT / "data" / "section_domain_map.json"

# Explicit mapping for all 108 SMILES Lab sections → Lean ledger domain
SECTION_DOMAIN: dict[str, str] = {
    "§1 Foundation": "chemical",
    "§2 Transition Metal IE": "chemical",
    "§3 Bond Angles": "chemical",
    "§4a ΔH°f": "chemical",
    "§4b Lattice Energies": "chemical",
    "§5b pKa": "chemical",
    "§5c E°": "chemical",
    "§6 IR Frequencies": "chemical",
    "§8 Entropy S°": "chemical",
    "§9 Electron Affinities": "electron",
    "§10 ΔG°f": "chemical",
    "§11 IE₂": "chemical",
    "§12 Cp°": "chemical",
    "§13 χm Magnetic": "material",
    "§14 Surface Tension": "chemical",
    "§15 Viscosity": "chemical",
    "§16 pKsp": "chemical",
    "§17 pKH Henry's Law": "chemical",
    "§18 Crystal Field Δo": "chemical",
    "§19 NMR δ": "neural",
    "§20 Raman ν": "chemical",
    "§21 Protein ΔG": "medical",
    "§22 Amino Acid pKa": "medical",
    "§23 Drug pKd": "medical",
    "§24 Enzyme kcat": "medical",
    "§25 vdW Radii": "electron",
    "§26 Polarizability": "electron",
    "§27 Boiling Points": "material",
    "§28 Melting Points": "material",
    "§29 Dielectric εr": "material",
    "§30 Refractive nD": "material",
    "§31 Band Gaps": "quantum",
    "§32 Work Functions": "material",
    "§33 Debye Temps": "material",
    "§34 Young's Modulus": "material",
    "§35 Michaelis Km": "medical",
    "§36 Hydrophobicity": "medical",
    "§37 Thermal κ": "material",
    "§38 Resistivity ρ": "material",
    "§39 Speed of Sound": "material",
    "§40 Ionic Radii": "electron",
    "§41 Covalent Radii": "electron",
    "§42 Binding E/A": "nuclear",
    "§43 Dipole Moments": "chemical",
    "§44 UV-Vis λmax": "material",
    "§45 Activation Ea": "chemical",
    "§46 Critical Temp Tc": "material",
    "§47 ΔHvap": "material",
    "§48 ΔHfus": "material",
    "§49 Molar Λ°": "chemical",
    "§50 Diffusion D": "chemical",
    "§51 Solubility logS": "chemical",
    "§52 ¹³C NMR δ": "neural",
    "§53 Fluorescence Φf": "neural",
    "§54 IE₃": "chemical",
    "§55 μeff Magnetic": "material",
    "§56 Hammett σ": "chemical",
    "§57 logP": "chemical",
    "§58 logβ Stability": "chemical",
    "§59 Colligative": "chemical",
    "§60 pKH Extended": "chemical",
    "§61 Glass Tg": "material",
    "§62 Bulk Modulus": "material",
    "§63 Lattice Param": "material",
    "§64 Neutron σ_a": "nuclear",
    "§65 Enzyme pKi": "medical",
    "§66 Particle Masses": "particle",
    "§67 Nuclear μN": "nuclear",
    "§68 Rotational B₀": "chemical",
    "§69 Virial B(T)": "chemical",
    "§70 Shear Modulus": "material",
    "§71 DNA Stacking ΔG": "medical",
    "§72 Electronegativity Ext": "electron",
    "§73 Thermal Expansion": "material",
    "§74 Acoustic Impedance": "material",
    "§75 Superconducting Tc": "material",
    "§76 Magnetic Ordering T": "material",
    "§77 Effective Mass m*": "quantum",
    "§78 X-ray Kα Energy": "particle",
    "§79 Optical Phonon ν": "material",
    "§80 Proton Affinity": "chemical",
    "§81 Cohesive Energy": "material",
    "§82 Mössbauer IS": "nuclear",
    "§83 Electron Mobility": "material",
    "§84 Poisson Ratio ν": "material",
    "§85 Thermal Diffusivity": "material",
    "§86 Grüneisen γ": "material",
    "§87 Heat Cap Ratio Cp/Cv": "chemical",
    "§88 XPS 1s Binding E": "particle",
    "§89 Surface Energy γs": "material",
    "§90 Heat of Combustion": "chemical",
    "§91 Critical Pressure Pc": "material",
    "§92 Protein Fold Rate": "medical",
    "§93 Membrane Potential": "medical",
    "§94 Donor Number DN": "chemical",
    "§95 Hole Mobility μh": "material",
    "§96 Bond Dissoc D₀": "chemical",
    "§97 Higher IE₄+": "chemical",
    "§98 Vapor Pressure": "chemical",
    "§99 Compressibility κ_T": "material",
    "§100 Solvatochromic E_T(30)": "chemical",
    "§101 Atomization ΔH_at": "chemical",
    "§102 Piezoelectric d₃₃": "material",
    "§103 Thermoelectric ZT": "material",
    "§104 Molar Volume V_m": "chemical",
    "§105 Autoignition T": "material",
    "§106 Isotope Frac ‰": "chemical",
    "§107 Electrode Ext E°": "chemical",
}


def main() -> int:
    records = json.loads(SMILES_JSON.read_text(encoding="utf-8"))["records"]
    sections = sorted({r["section"] for r in records})
    missing = [s for s in sections if s not in SECTION_DOMAIN]
    if missing:
        raise SystemExit(f"Unmapped sections ({len(missing)}): {missing}")

    counts: dict[str, int] = {}
    for rec in records:
        dom = SECTION_DOMAIN[rec["section"]]
        counts[dom] = counts.get(dom, 0) + 1

    payload = {
        "version": "1.0",
        "total_sections": len(sections),
        "section_to_domain": SECTION_DOMAIN,
        "domain_record_counts": counts,
        "total_records": len(records),
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  sections: {len(sections)}")
    print(f"  records:  {len(records)}")
    for dom, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"    {dom}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
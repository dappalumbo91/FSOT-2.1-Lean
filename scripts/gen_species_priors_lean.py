#!/usr/bin/env python3
"""Generate FSOT/Formal/SpeciesPriors.lean from species_catalog registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "SpeciesPriors.lean"


def build_lean(registry: dict) -> str:
    sp = registry.get("species_catalog", {})
    counts = sp.get("category_counts", {})
    metals = counts.get("metals", 44)
    molecules = counts.get("molecules", 87)
    polymers = counts.get("polymers", 10)
    species = sp.get("species_count", metals + molecules + polymers)
    props = sp.get("property_count", 684)

    return f"""/-
  FSOT Formal SpeciesPriors — Machine & Molecule catalog certificates.

  Source: FSOT_Machine_And_Molecule/fsot_species_catalog.json
  Generator: scripts/gen_species_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def species_metal_count : ℕ := {metals}
def species_molecule_count : ℕ := {molecules}
def species_polymer_count : ℕ := {polymers}
def species_total_count : ℕ := {species}
def species_property_count : ℕ := {props}

theorem species_total_count_eq_sum :
    species_metal_count + species_molecule_count + species_polymer_count = species_total_count := by
  unfold species_metal_count species_molecule_count species_polymer_count species_total_count; norm_num

theorem species_property_count_pos : 0 < species_property_count := by
  unfold species_property_count; norm_num

/-- Bundle: 141 species across metals/molecules/polymers; material+molecular domain signs. -/
theorem species_catalog_bundle :
    species_total_count = {species} ∧
    species_metal_count = {metals} ∧
    species_molecule_count = {molecules} ∧
    species_polymer_count = {polymers} ∧
    species_metal_count + species_molecule_count + species_polymer_count = species_total_count ∧
    species_property_count = {props} ∧
    (0 : ℝ) < raw_S (get_domain_params "material") ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold species_total_count; norm_num,
    by unfold species_metal_count; norm_num,
    by unfold species_molecule_count; norm_num,
    by unfold species_polymer_count; norm_num,
    species_total_count_eq_sum,
    by unfold species_property_count; norm_num,
    material_raw_S_positive,
    molecular_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SpeciesPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
/-
  FSOT Formal PubchemCompoundPropertiesPriors — Tier 38 public API (PubChem_Compound_Properties).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pubchem_compound_properties_observable_count : ℕ := 12
def pubchem_compound_properties_median_error_pct : ℝ := (0.0012801911752094832 : ℝ)
def pubchem_compound_properties_D_eff : ℕ := 8

theorem pubchem_compound_properties_observable_count_pos : 0 < pubchem_compound_properties_observable_count := by
  unfold pubchem_compound_properties_observable_count; norm_num

theorem pubchem_compound_properties_median_error_under_five_pct :
    pubchem_compound_properties_median_error_pct < (5 : ℝ) := by
  unfold pubchem_compound_properties_median_error_pct; norm_num

theorem pubchem_compound_properties_bundle :
    pubchem_compound_properties_observable_count = 12 ∧
    pubchem_compound_properties_D_eff = 8 ∧
    pubchem_compound_properties_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold pubchem_compound_properties_observable_count; norm_num,
    by unfold pubchem_compound_properties_D_eff; norm_num,
    pubchem_compound_properties_median_error_under_five_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal

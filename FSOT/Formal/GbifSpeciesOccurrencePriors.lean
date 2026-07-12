/-
  FSOT Formal GbifSpeciesOccurrencePriors — Tier 38 public API (GBIF_Species_Occurrence).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def gbif_species_occurrence_observable_count : ℕ := 2000
def gbif_species_occurrence_median_error_pct : ℝ := (0.0 : ℝ)
def gbif_species_occurrence_D_eff : ℕ := 15

theorem gbif_species_occurrence_observable_count_pos : 0 < gbif_species_occurrence_observable_count := by
  unfold gbif_species_occurrence_observable_count; norm_num

theorem gbif_species_occurrence_median_error_under_five_pct :
    gbif_species_occurrence_median_error_pct < (5 : ℝ) := by
  unfold gbif_species_occurrence_median_error_pct; norm_num

theorem gbif_species_occurrence_bundle :
    gbif_species_occurrence_observable_count = 2000 ∧
    gbif_species_occurrence_D_eff = 15 ∧
    gbif_species_occurrence_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold gbif_species_occurrence_observable_count; norm_num,
    by unfold gbif_species_occurrence_D_eff; norm_num,
    gbif_species_occurrence_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal

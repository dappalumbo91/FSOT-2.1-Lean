/-
  FSOT Formal CulinaryFermentationMaillardPanelPriors — Tier 86 scientific expansion (Culinary_Fermentation_Maillard_Panel).
  Generator: scripts/gen_tier86_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def culinary_fermentation_maillard_observable_count : ℕ := 130
def culinary_fermentation_maillard_median_error_pct : ℝ := (0.040788 : ℝ)
def culinary_fermentation_maillard_D_eff : ℕ := 15

theorem culinary_fermentation_maillard_observable_count_pos : 0 < culinary_fermentation_maillard_observable_count := by
  unfold culinary_fermentation_maillard_observable_count; norm_num

theorem culinary_fermentation_maillard_median_error_under_five_pct :
    culinary_fermentation_maillard_median_error_pct < (5 : ℝ) := by
  unfold culinary_fermentation_maillard_median_error_pct; norm_num

theorem culinary_fermentation_maillard_bundle :
    culinary_fermentation_maillard_observable_count = 130 ∧
    culinary_fermentation_maillard_D_eff = 15 ∧
    culinary_fermentation_maillard_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold culinary_fermentation_maillard_observable_count; norm_num,
    by unfold culinary_fermentation_maillard_D_eff; norm_num,
    culinary_fermentation_maillard_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

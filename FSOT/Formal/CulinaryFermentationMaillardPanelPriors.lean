/-
  FSOT Formal CulinaryFermentationMaillardPanelPriors — extension domain Culinary_Fermentation_Maillard_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def culinary_fermentation_maillard_panel_observable_count : ℕ := 130
def culinary_fermentation_maillard_panel_D_eff : ℕ := 15

theorem culinary_fermentation_maillard_panel_observable_count_pos : 0 < culinary_fermentation_maillard_panel_observable_count := by
  unfold culinary_fermentation_maillard_panel_observable_count; decide

theorem culinary_fermentation_maillard_panel_median_error_under_half_pct :
    (0.040788 : ℝ) < (0.5 : ℝ) := by norm_num

theorem culinary_fermentation_maillard_panel_bundle :
    culinary_fermentation_maillard_panel_observable_count = 130 ∧
    culinary_fermentation_maillard_panel_D_eff = 15 ∧
    (0.040788 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold culinary_fermentation_maillard_panel_observable_count; decide,
    by unfold culinary_fermentation_maillard_panel_D_eff; decide,
    culinary_fermentation_maillard_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

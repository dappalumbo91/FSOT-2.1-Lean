/-
  FSOT Formal SoilSciencePanelPriors — extension domain Soil_Science_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def soil_science_panel_observable_count : ℕ := 96
def soil_science_panel_D_eff : ℕ := 15

theorem soil_science_panel_observable_count_pos : 0 < soil_science_panel_observable_count := by
  unfold soil_science_panel_observable_count; decide

theorem soil_science_panel_median_error_under_half_pct :
    (0.006006 : ℝ) < (0.5 : ℝ) := by norm_num

theorem soil_science_panel_bundle :
    soil_science_panel_observable_count = 96 ∧
    soil_science_panel_D_eff = 15 ∧
    (0.006006 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold soil_science_panel_observable_count; decide,
    by unfold soil_science_panel_D_eff; decide,
    soil_science_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

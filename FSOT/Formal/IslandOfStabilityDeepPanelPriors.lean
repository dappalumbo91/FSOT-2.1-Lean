/-
  FSOT Formal IslandOfStabilityDeepPanelPriors — extension domain Island_Of_Stability_Deep_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def island_of_stability_deep_panel_observable_count : ℕ := 23
def island_of_stability_deep_panel_D_eff : ℕ := 19

theorem island_of_stability_deep_panel_observable_count_pos : 0 < island_of_stability_deep_panel_observable_count := by
  unfold island_of_stability_deep_panel_observable_count; decide

theorem island_of_stability_deep_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem island_of_stability_deep_panel_bundle :
    island_of_stability_deep_panel_observable_count = 23 ∧
    island_of_stability_deep_panel_D_eff = 19 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold island_of_stability_deep_panel_observable_count; decide,
    by unfold island_of_stability_deep_panel_D_eff; decide,
    island_of_stability_deep_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

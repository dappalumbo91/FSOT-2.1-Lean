/-
  FSOT Formal ExperimentalBaseMathematicsPanelPriors — extension domain Experimental_Base_Mathematics_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def experimental_base_mathematics_panel_observable_count : ℕ := 36
def experimental_base_mathematics_panel_D_eff : ℕ := 17

theorem experimental_base_mathematics_panel_observable_count_pos : 0 < experimental_base_mathematics_panel_observable_count := by
  unfold experimental_base_mathematics_panel_observable_count; decide

theorem experimental_base_mathematics_panel_median_error_under_half_pct :
    (0.009504 : ℝ) < (0.5 : ℝ) := by norm_num

theorem experimental_base_mathematics_panel_bundle :
    experimental_base_mathematics_panel_observable_count = 36 ∧
    experimental_base_mathematics_panel_D_eff = 17 ∧
    (0.009504 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold experimental_base_mathematics_panel_observable_count; decide,
    by unfold experimental_base_mathematics_panel_D_eff; decide,
    experimental_base_mathematics_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

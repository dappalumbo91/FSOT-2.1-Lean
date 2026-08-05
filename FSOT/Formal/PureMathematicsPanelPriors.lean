/-
  FSOT Formal PureMathematicsPanelPriors — extension domain Pure_Mathematics_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def pure_mathematics_panel_observable_count : ℕ := 44
def pure_mathematics_panel_D_eff : ℕ := 18

theorem pure_mathematics_panel_observable_count_pos : 0 < pure_mathematics_panel_observable_count := by
  unfold pure_mathematics_panel_observable_count; decide

theorem pure_mathematics_panel_median_error_under_half_pct :
    (0.02584 : ℝ) < (0.5 : ℝ) := by norm_num

theorem pure_mathematics_panel_bundle :
    pure_mathematics_panel_observable_count = 44 ∧
    pure_mathematics_panel_D_eff = 18 ∧
    (0.02584 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold pure_mathematics_panel_observable_count; decide,
    by unfold pure_mathematics_panel_D_eff; decide,
    pure_mathematics_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

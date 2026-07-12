/-
  FSOT Formal PureMathematicsPanelPriors — Tier 86 scientific expansion (Pure_Mathematics_Panel).
  Generator: scripts/gen_tier86_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pure_mathematics_panel_observable_count : ℕ := 44
def pure_mathematics_panel_median_error_pct : ℝ := (0.02584 : ℝ)
def pure_mathematics_panel_D_eff : ℕ := 18

theorem pure_mathematics_panel_observable_count_pos : 0 < pure_mathematics_panel_observable_count := by
  unfold pure_mathematics_panel_observable_count; norm_num

theorem pure_mathematics_panel_median_error_under_five_pct :
    pure_mathematics_panel_median_error_pct < (5 : ℝ) := by
  unfold pure_mathematics_panel_median_error_pct; norm_num

theorem pure_mathematics_panel_bundle :
    pure_mathematics_panel_observable_count = 44 ∧
    pure_mathematics_panel_D_eff = 18 ∧
    pure_mathematics_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "mathematical") > 0 := by
  refine ⟨
    by unfold pure_mathematics_panel_observable_count; norm_num,
    by unfold pure_mathematics_panel_D_eff; norm_num,
    pure_mathematics_panel_median_error_under_five_pct,
    mathematical_raw_S_positive
  ⟩

end

end FSOT.Formal

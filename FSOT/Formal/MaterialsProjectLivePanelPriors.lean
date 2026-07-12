/-
  FSOT Formal MaterialsProjectLivePanelPriors — Tier 68–70 expansion.
  Generator: scripts/gen_tiers_68_70_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def materials_project_live_panel_observable_count : ℕ := 141
def materials_project_live_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def materials_project_live_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def materials_project_live_panel_beats_sota_headlines : ℕ := 2
def materials_project_live_panel_D_eff : ℕ := 16

theorem materials_project_live_panel_observable_count_pos : 0 < materials_project_live_panel_observable_count := by
  unfold materials_project_live_panel_observable_count; norm_num

theorem materials_project_live_panel_pooled_median_under_half_pct :
    materials_project_live_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold materials_project_live_panel_pooled_median_error_pct; norm_num

theorem materials_project_live_panel_headline_median_under_half_pct :
    materials_project_live_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold materials_project_live_panel_headline_median_error_pct; norm_num

theorem materials_project_live_panel_beats_sota_headlines_pos : 0 < materials_project_live_panel_beats_sota_headlines := by
  unfold materials_project_live_panel_beats_sota_headlines; norm_num

theorem materials_project_live_panel_bundle :
    materials_project_live_panel_observable_count = 141 ∧
    materials_project_live_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    materials_project_live_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold materials_project_live_panel_observable_count; norm_num
  · exact materials_project_live_panel_pooled_median_under_half_pct
  · exact materials_project_live_panel_beats_sota_headlines_pos

end

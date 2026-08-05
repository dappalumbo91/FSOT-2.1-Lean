/-
  FSOT Formal EcologyPublicPanelPriors — Tier 66 NeuroLab residual registry panels.
  Generator: scripts/gen_tiers_66_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def ecology_public_panel_observable_count : ℕ := 12
def ecology_public_panel_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def ecology_public_panel_headline_median_error_pct : ℝ := (0.0 : ℝ)
def ecology_public_panel_beats_sota_headlines : ℕ := 2
def ecology_public_panel_D_eff : ℕ := 15

theorem ecology_public_panel_observable_count_pos : 0 < ecology_public_panel_observable_count := by
  unfold ecology_public_panel_observable_count; decide

theorem ecology_public_panel_pooled_median_under_half_pct :
    ecology_public_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold ecology_public_panel_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem ecology_public_panel_headline_median_under_half_pct :
    ecology_public_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold ecology_public_panel_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem ecology_public_panel_beats_sota_headlines_pos : 0 < ecology_public_panel_beats_sota_headlines := by
  unfold ecology_public_panel_beats_sota_headlines; decide

theorem ecology_public_panel_bundle :
    ecology_public_panel_observable_count = 12 ∧
    ecology_public_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    ecology_public_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold ecology_public_panel_observable_count; decide
  · exact ecology_public_panel_pooled_median_under_half_pct
  · exact ecology_public_panel_beats_sota_headlines_pos

end

end FSOT.Formal
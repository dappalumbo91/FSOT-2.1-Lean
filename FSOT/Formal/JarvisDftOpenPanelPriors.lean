/-
  FSOT Formal JarvisDftOpenPanelPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def jarvis_dft_open_panel_observable_count : ℕ := 77
def jarvis_dft_open_panel_pooled_median_error_pct : ℝ := (0.01341 : ℝ)
def jarvis_dft_open_panel_headline_median_error_pct : ℝ := (0.01341 : ℝ)
def jarvis_dft_open_panel_D_eff : ℕ := 16

theorem jarvis_dft_open_panel_observable_count_pos : 0 < jarvis_dft_open_panel_observable_count := by
  unfold jarvis_dft_open_panel_observable_count; decide

theorem jarvis_dft_open_panel_pooled_median_under_half_pct :
    jarvis_dft_open_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold jarvis_dft_open_panel_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem jarvis_dft_open_panel_headline_median_under_half_pct :
    jarvis_dft_open_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold jarvis_dft_open_panel_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem jarvis_dft_open_panel_bundle :
    jarvis_dft_open_panel_observable_count = 77 ∧
    jarvis_dft_open_panel_D_eff = 16 ∧
    jarvis_dft_open_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold jarvis_dft_open_panel_observable_count; decide
  · unfold jarvis_dft_open_panel_D_eff; decide
  · exact jarvis_dft_open_panel_pooled_median_under_half_pct

end

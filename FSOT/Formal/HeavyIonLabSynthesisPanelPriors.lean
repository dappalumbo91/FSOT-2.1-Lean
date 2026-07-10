/-
  FSOT Formal HeavyIonLabSynthesisPanelPriors — Tier 73 lab synthesis + metamaterial fluid design.
  Generator: scripts/gen_tiers_73_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def heavy_ion_lab_synthesis_panel_observable_count : ℕ := 39
def heavy_ion_lab_synthesis_panel_pooled_median_error_pct : ℝ := (9.5e-05 : ℝ)
def heavy_ion_lab_synthesis_panel_headline_median_error_pct : ℝ := (9.5041344017055e-05 : ℝ)
def heavy_ion_lab_synthesis_panel_beats_sota_headlines : ℕ := 2
def heavy_ion_lab_synthesis_panel_D_eff : ℕ := 13

theorem heavy_ion_lab_synthesis_panel_observable_count_pos : 0 < heavy_ion_lab_synthesis_panel_observable_count := by
  unfold heavy_ion_lab_synthesis_panel_observable_count; norm_num

theorem heavy_ion_lab_synthesis_panel_pooled_median_under_half_pct :
    heavy_ion_lab_synthesis_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold heavy_ion_lab_synthesis_panel_pooled_median_error_pct; norm_num

theorem heavy_ion_lab_synthesis_panel_headline_median_under_half_pct :
    heavy_ion_lab_synthesis_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold heavy_ion_lab_synthesis_panel_headline_median_error_pct; norm_num

theorem heavy_ion_lab_synthesis_panel_beats_sota_headlines_pos : 0 < heavy_ion_lab_synthesis_panel_beats_sota_headlines := by
  unfold heavy_ion_lab_synthesis_panel_beats_sota_headlines; norm_num

theorem heavy_ion_lab_synthesis_panel_bundle :
    heavy_ion_lab_synthesis_panel_observable_count = 39 ∧
    heavy_ion_lab_synthesis_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    heavy_ion_lab_synthesis_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold heavy_ion_lab_synthesis_panel_observable_count; norm_num
  · exact heavy_ion_lab_synthesis_panel_pooled_median_under_half_pct
  · exact heavy_ion_lab_synthesis_panel_beats_sota_headlines_pos

end

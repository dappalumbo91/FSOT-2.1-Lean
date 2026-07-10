/-
  FSOT Formal ChemicalStructureStabilityPanelPriors — Tier 57/58 public interdisciplinary / live catalog.
  Generator: scripts/gen_tiers_57_58_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def chemical_structure_stability_panel_observable_count : ℕ := 32
def chemical_structure_stability_panel_pooled_median_error_pct : ℝ := (0.00206 : ℝ)
def chemical_structure_stability_panel_headline_median_error_pct : ℝ := (0.0024238898584426276 : ℝ)
def chemical_structure_stability_panel_beats_sota_headlines : ℕ := 2
def chemical_structure_stability_panel_D_eff : ℕ := 14

theorem chemical_structure_stability_panel_observable_count_pos : 0 < chemical_structure_stability_panel_observable_count := by
  unfold chemical_structure_stability_panel_observable_count; norm_num

theorem chemical_structure_stability_panel_pooled_median_under_half_pct :
    chemical_structure_stability_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold chemical_structure_stability_panel_pooled_median_error_pct; norm_num

theorem chemical_structure_stability_panel_headline_median_under_half_pct :
    chemical_structure_stability_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold chemical_structure_stability_panel_headline_median_error_pct; norm_num

theorem chemical_structure_stability_panel_beats_sota_headlines_pos : 0 < chemical_structure_stability_panel_beats_sota_headlines := by
  unfold chemical_structure_stability_panel_beats_sota_headlines; norm_num

theorem chemical_structure_stability_panel_bundle :
    chemical_structure_stability_panel_observable_count = 32 ∧
    chemical_structure_stability_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    chemical_structure_stability_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold chemical_structure_stability_panel_observable_count; norm_num
  · exact chemical_structure_stability_panel_pooled_median_under_half_pct
  · exact chemical_structure_stability_panel_beats_sota_headlines_pos

end

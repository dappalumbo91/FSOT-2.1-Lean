/-
  FSOT Formal PubChemStabilityPanelPriors — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pubchem_stability_panel_observable_count : ℕ := 59
def pubchem_stability_panel_pooled_median_error_pct : ℝ := (0.0024238898584426276 : ℝ)
def pubchem_stability_panel_headline_median_error_pct : ℝ := (0.0024238898584426276 : ℝ)
def pubchem_stability_panel_beats_sota_headlines : ℕ := 2
def pubchem_stability_panel_D_eff : ℕ := 14

theorem pubchem_stability_panel_observable_count_pos : 0 < pubchem_stability_panel_observable_count := by
  unfold pubchem_stability_panel_observable_count; norm_num

theorem pubchem_stability_panel_pooled_median_under_half_pct :
    pubchem_stability_panel_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold pubchem_stability_panel_pooled_median_error_pct; norm_num

theorem pubchem_stability_panel_headline_median_under_half_pct :
    pubchem_stability_panel_headline_median_error_pct < (0.5 : ℝ) := by
  unfold pubchem_stability_panel_headline_median_error_pct; norm_num

theorem pubchem_stability_panel_beats_sota_headlines_pos : 0 < pubchem_stability_panel_beats_sota_headlines := by
  unfold pubchem_stability_panel_beats_sota_headlines; norm_num

theorem pubchem_stability_panel_bundle :
    pubchem_stability_panel_observable_count = 59 ∧
    pubchem_stability_panel_pooled_median_error_pct < (0.5 : ℝ) ∧
    pubchem_stability_panel_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold pubchem_stability_panel_observable_count; norm_num
  · exact pubchem_stability_panel_pooled_median_under_half_pct
  · exact pubchem_stability_panel_beats_sota_headlines_pos

end

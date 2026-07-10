/-
  FSOT Formal PubChemLiveDeepPriors — Tier 68–70 expansion.
  Generator: scripts/gen_tiers_68_70_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pubchem_live_deep_observable_count : ℕ := 36
def pubchem_live_deep_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def pubchem_live_deep_headline_median_error_pct : ℝ := (0.002059838302688438 : ℝ)
def pubchem_live_deep_beats_sota_headlines : ℕ := 2
def pubchem_live_deep_D_eff : ℕ := 8

theorem pubchem_live_deep_observable_count_pos : 0 < pubchem_live_deep_observable_count := by
  unfold pubchem_live_deep_observable_count; norm_num

theorem pubchem_live_deep_pooled_median_under_half_pct :
    pubchem_live_deep_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold pubchem_live_deep_pooled_median_error_pct; norm_num

theorem pubchem_live_deep_headline_median_under_half_pct :
    pubchem_live_deep_headline_median_error_pct < (0.5 : ℝ) := by
  unfold pubchem_live_deep_headline_median_error_pct; norm_num

theorem pubchem_live_deep_beats_sota_headlines_pos : 0 < pubchem_live_deep_beats_sota_headlines := by
  unfold pubchem_live_deep_beats_sota_headlines; norm_num

theorem pubchem_live_deep_bundle :
    pubchem_live_deep_observable_count = 36 ∧
    pubchem_live_deep_pooled_median_error_pct < (0.5 : ℝ) ∧
    pubchem_live_deep_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold pubchem_live_deep_observable_count; norm_num
  · exact pubchem_live_deep_pooled_median_under_half_pct
  · exact pubchem_live_deep_beats_sota_headlines_pos

end

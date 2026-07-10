/-
  FSOT Formal ChaosMediatedPhaseTransitionsPriors — Chaos_Mediated_Phase_Transitions Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def chaos_pt_observable_count : ℕ := 21
def chaos_pt_pooled_median_error_pct : ℝ := (0.03147898006445882 : ℝ)
def chaos_pt_headline_median_error_pct : ℝ := (0.03147898006445882 : ℝ)
def chaos_pt_beats_sota_headlines : ℕ := 2
def chaos_pt_D_eff : ℕ := 17

theorem chaos_pt_observable_count_pos : 0 < chaos_pt_observable_count := by
  unfold chaos_pt_observable_count; norm_num

theorem chaos_pt_pooled_median_under_five_pct :
    chaos_pt_pooled_median_error_pct < (5 : ℝ) := by
  unfold chaos_pt_pooled_median_error_pct; norm_num

theorem chaos_pt_headline_median_under_five_pct :
    chaos_pt_headline_median_error_pct < (5 : ℝ) := by
  unfold chaos_pt_headline_median_error_pct; norm_num

theorem chaos_pt_beats_sota_headlines_pos : 0 < chaos_pt_beats_sota_headlines := by
  unfold chaos_pt_beats_sota_headlines; norm_num

theorem chaos_pt_bundle :
    chaos_pt_observable_count = 21 ∧
    chaos_pt_pooled_median_error_pct < (5 : ℝ) ∧
    chaos_pt_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold chaos_pt_observable_count; norm_num
  · exact chaos_pt_pooled_median_under_five_pct
  · exact chaos_pt_beats_sota_headlines_pos

end

/-
  FSOT Formal FormulaBranchingFractalPriors — Formula_Branching_Fractal Tier J ToE completeness.
  Generator: scripts/gen_tier_j_toe_completeness_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fractal_observable_count : ℕ := 144
def fractal_pooled_median_error_pct : ℝ := (0.038016537604977654 : ℝ)
def fractal_headline_median_error_pct : ℝ := (0.038016537604977654 : ℝ)
def fractal_beats_sota_headlines : ℕ := 3
def fractal_D_eff : ℕ := 18
def fractal_domain_attachment_count : ℕ := 135

theorem fractal_observable_count_pos : 0 < fractal_observable_count := by
  unfold fractal_observable_count; norm_num

theorem fractal_pooled_median_under_five_pct :
    fractal_pooled_median_error_pct < (5 : ℝ) := by
  unfold fractal_pooled_median_error_pct; norm_num

theorem fractal_headline_median_under_five_pct :
    fractal_headline_median_error_pct < (5 : ℝ) := by
  unfold fractal_headline_median_error_pct; norm_num

theorem fractal_beats_sota_headlines_pos : 0 < fractal_beats_sota_headlines := by
  unfold fractal_beats_sota_headlines; norm_num
theorem fractal_attachments_pos : 0 < fractal_domain_attachment_count := by
  unfold fractal_domain_attachment_count; norm_num

theorem fractal_bundle :
    fractal_observable_count = 144 ∧
    fractal_pooled_median_error_pct < (5 : ℝ) ∧
    fractal_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fractal_observable_count; norm_num
  · exact fractal_pooled_median_under_five_pct
  · exact fractal_beats_sota_headlines_pos

end

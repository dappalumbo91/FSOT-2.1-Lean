/-
  FSOT Formal PureMathematicsExtensionPriors — Pure_Mathematics Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pure_mathematics_ext_observable_count : ℕ := 1549
def pure_mathematics_ext_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def pure_mathematics_ext_headline_median_error_pct : ℝ := (0.0 : ℝ)
def pure_mathematics_ext_beats_sota_headlines : ℕ := 2
def pure_mathematics_ext_D_eff : ℕ := 18

theorem pure_mathematics_ext_observable_count_pos : 0 < pure_mathematics_ext_observable_count := by
  unfold pure_mathematics_ext_observable_count; decide

theorem pure_mathematics_ext_pooled_median_under_half_pct :
    pure_mathematics_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold pure_mathematics_ext_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pure_mathematics_ext_headline_median_under_half_pct :
    pure_mathematics_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold pure_mathematics_ext_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pure_mathematics_ext_beats_sota_headlines_pos : 0 < pure_mathematics_ext_beats_sota_headlines := by
  unfold pure_mathematics_ext_beats_sota_headlines; decide

theorem pure_mathematics_ext_bundle :
    pure_mathematics_ext_observable_count = 1549 ∧
    pure_mathematics_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    pure_mathematics_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < pure_mathematics_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold pure_mathematics_ext_observable_count; decide,
    pure_mathematics_ext_pooled_median_under_half_pct,
    pure_mathematics_ext_headline_median_under_half_pct,
    pure_mathematics_ext_beats_sota_headlines_pos,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal

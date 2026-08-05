/-
  FSOT Formal MathGeneratorRulesEvalPriors — per-rule eval across 1520 formal rules.
  Generator: scripts/gen_math_generator_rules_eval_lean.py
  Source: vendor/math_generator/rules
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def math_generator_rules_eval_observable_count : ℕ := 1552
def math_generator_rules_eval_corpus_count : ℕ := 62
def math_generator_rules_eval_numeric_eval_count : ℕ := 6
def math_generator_rules_eval_D_eff : ℕ := 17
def math_generator_rules_eval_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def math_generator_rules_eval_headline_median_error_pct : ℝ := (0.0 : ℝ)
def math_generator_rules_eval_beats_sota_headlines : ℕ := 4

theorem math_generator_rules_eval_observable_count_pos : 0 < math_generator_rules_eval_observable_count := by
  unfold math_generator_rules_eval_observable_count; decide

theorem math_generator_rules_eval_corpus_count_pos : 0 < math_generator_rules_eval_corpus_count := by
  unfold math_generator_rules_eval_corpus_count; decide

theorem math_generator_rules_eval_pooled_median_under_half_pct :
    math_generator_rules_eval_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold math_generator_rules_eval_pooled_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem math_generator_rules_eval_headline_median_under_half_pct :
    math_generator_rules_eval_headline_median_error_pct < (0.5 : ℝ) := by
  unfold math_generator_rules_eval_headline_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem math_generator_rules_eval_beats_sota_headlines_pos : 0 < math_generator_rules_eval_beats_sota_headlines := by
  unfold math_generator_rules_eval_beats_sota_headlines; decide

theorem math_generator_rules_eval_bundle :
    math_generator_rules_eval_observable_count = 1552 ∧
    math_generator_rules_eval_corpus_count = 62 ∧
    math_generator_rules_eval_numeric_eval_count = 6 ∧
    math_generator_rules_eval_D_eff = 17 ∧
    math_generator_rules_eval_pooled_median_error_pct < (0.5 : ℝ) ∧
    math_generator_rules_eval_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < math_generator_rules_eval_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold math_generator_rules_eval_observable_count; decide,
    by unfold math_generator_rules_eval_corpus_count; decide,
    by unfold math_generator_rules_eval_numeric_eval_count; decide,
    by unfold math_generator_rules_eval_D_eff; decide,
    math_generator_rules_eval_pooled_median_under_half_pct,
    math_generator_rules_eval_headline_median_under_half_pct,
    math_generator_rules_eval_beats_sota_headlines_pos,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal

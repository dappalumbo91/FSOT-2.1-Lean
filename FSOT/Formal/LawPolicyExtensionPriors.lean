/-
  FSOT Formal LawPolicyExtensionPriors — Law_Policy Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def law_policy_ext_observable_count : ℕ := 180
def law_policy_ext_pooled_median_error_pct : ℝ := (0.019504399572479934 : ℝ)
def law_policy_ext_headline_median_error_pct : ℝ := (0.019504399572479934 : ℝ)
def law_policy_ext_beats_sota_headlines : ℕ := 2
def law_policy_ext_D_eff : ℕ := 17

theorem law_policy_ext_observable_count_pos : 0 < law_policy_ext_observable_count := by
  unfold law_policy_ext_observable_count; norm_num

theorem law_policy_ext_pooled_median_under_five_pct :
    law_policy_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold law_policy_ext_pooled_median_error_pct; norm_num

theorem law_policy_ext_headline_median_under_five_pct :
    law_policy_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold law_policy_ext_headline_median_error_pct; norm_num

theorem law_policy_ext_beats_sota_headlines_pos : 0 < law_policy_ext_beats_sota_headlines := by
  unfold law_policy_ext_beats_sota_headlines; norm_num

theorem law_policy_ext_bundle :
    law_policy_ext_observable_count = 180 ∧
    law_policy_ext_pooled_median_error_pct < (5 : ℝ) ∧
    law_policy_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < law_policy_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold law_policy_ext_observable_count; norm_num,
    law_policy_ext_pooled_median_under_five_pct,
    law_policy_ext_headline_median_under_five_pct,
    law_policy_ext_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

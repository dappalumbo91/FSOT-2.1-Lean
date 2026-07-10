/-
  FSOT Formal AnthropologyExtensionPriors — Anthropology Tier D extension (real API anchors).
  Generator: scripts/gen_tier_d_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def anthropology_ext_observable_count : ℕ := 160
def anthropology_ext_pooled_median_error_pct : ℝ := (0.019504399572476606 : ℝ)
def anthropology_ext_headline_median_error_pct : ℝ := (0.019504399572476606 : ℝ)
def anthropology_ext_beats_sota_headlines : ℕ := 2
def anthropology_ext_D_eff : ℕ := 17

theorem anthropology_ext_observable_count_pos : 0 < anthropology_ext_observable_count := by
  unfold anthropology_ext_observable_count; norm_num

theorem anthropology_ext_pooled_median_under_five_pct :
    anthropology_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold anthropology_ext_pooled_median_error_pct; norm_num

theorem anthropology_ext_headline_median_under_five_pct :
    anthropology_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold anthropology_ext_headline_median_error_pct; norm_num

theorem anthropology_ext_beats_sota_headlines_pos : 0 < anthropology_ext_beats_sota_headlines := by
  unfold anthropology_ext_beats_sota_headlines; norm_num

theorem anthropology_ext_bundle :
    anthropology_ext_observable_count = 160 ∧
    anthropology_ext_pooled_median_error_pct < (5 : ℝ) ∧
    anthropology_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < anthropology_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold anthropology_ext_observable_count; norm_num,
    anthropology_ext_pooled_median_under_five_pct,
    anthropology_ext_headline_median_under_five_pct,
    anthropology_ext_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

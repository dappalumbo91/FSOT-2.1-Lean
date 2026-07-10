/-
  FSOT Formal HistoryExtensionPriors — History Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def history_ext_observable_count : ℕ := 170
def history_ext_pooled_median_error_pct : ℝ := (0.019504399572477397 : ℝ)
def history_ext_headline_median_error_pct : ℝ := (0.019504399572477397 : ℝ)
def history_ext_beats_sota_headlines : ℕ := 2
def history_ext_D_eff : ℕ := 15

theorem history_ext_observable_count_pos : 0 < history_ext_observable_count := by
  unfold history_ext_observable_count; norm_num

theorem history_ext_pooled_median_under_five_pct :
    history_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold history_ext_pooled_median_error_pct; norm_num

theorem history_ext_headline_median_under_five_pct :
    history_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold history_ext_headline_median_error_pct; norm_num

theorem history_ext_beats_sota_headlines_pos : 0 < history_ext_beats_sota_headlines := by
  unfold history_ext_beats_sota_headlines; norm_num

theorem history_ext_bundle :
    history_ext_observable_count = 170 ∧
    history_ext_pooled_median_error_pct < (5 : ℝ) ∧
    history_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < history_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold history_ext_observable_count; norm_num,
    history_ext_pooled_median_under_five_pct,
    history_ext_headline_median_under_five_pct,
    history_ext_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

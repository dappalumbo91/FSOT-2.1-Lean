/-
  FSOT Formal BotanyExtensionPriors — Botany Tier D extension (real API anchors).
  Generator: scripts/gen_tier_d_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def botany_ext_observable_count : ℕ := 426
def botany_ext_pooled_median_error_pct : ℝ := (0.022236250385193387 : ℝ)
def botany_ext_headline_median_error_pct : ℝ := (0.022236250385193387 : ℝ)
def botany_ext_beats_sota_headlines : ℕ := 2
def botany_ext_D_eff : ℕ := 14

theorem botany_ext_observable_count_pos : 0 < botany_ext_observable_count := by
  unfold botany_ext_observable_count; decide

theorem botany_ext_pooled_median_under_half_pct :
    botany_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold botany_ext_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem botany_ext_headline_median_under_half_pct :
    botany_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold botany_ext_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem botany_ext_beats_sota_headlines_pos : 0 < botany_ext_beats_sota_headlines := by
  unfold botany_ext_beats_sota_headlines; decide

theorem botany_ext_bundle :
    botany_ext_observable_count = 426 ∧
    botany_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    botany_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < botany_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold botany_ext_observable_count; decide,
    botany_ext_pooled_median_under_half_pct,
    botany_ext_headline_median_under_half_pct,
    botany_ext_beats_sota_headlines_pos,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal FinanceMarketsExtensionPriors — Finance_Markets Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def finance_markets_ext_observable_count : ℕ := 245
def finance_markets_ext_pooled_median_error_pct : ℝ := (0.025840180827434747 : ℝ)
def finance_markets_ext_headline_median_error_pct : ℝ := (0.025840180827434747 : ℝ)
def finance_markets_ext_beats_sota_headlines : ℕ := 2
def finance_markets_ext_D_eff : ℕ := 19

theorem finance_markets_ext_observable_count_pos : 0 < finance_markets_ext_observable_count := by
  unfold finance_markets_ext_observable_count; decide

theorem finance_markets_ext_pooled_median_under_half_pct :
    finance_markets_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold finance_markets_ext_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem finance_markets_ext_headline_median_under_half_pct :
    finance_markets_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold finance_markets_ext_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem finance_markets_ext_beats_sota_headlines_pos : 0 < finance_markets_ext_beats_sota_headlines := by
  unfold finance_markets_ext_beats_sota_headlines; decide

theorem finance_markets_ext_bundle :
    finance_markets_ext_observable_count = 245 ∧
    finance_markets_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    finance_markets_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < finance_markets_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold finance_markets_ext_observable_count; decide,
    finance_markets_ext_pooled_median_under_half_pct,
    finance_markets_ext_headline_median_under_half_pct,
    finance_markets_ext_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

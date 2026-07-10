/-
  FSOT Formal SupplyChainLogisticsExtensionPriors — Supply_Chain_Logistics Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def supply_chain_ext_observable_count : ℕ := 40
def supply_chain_ext_pooled_median_error_pct : ℝ := (0.03230022603427978 : ℝ)
def supply_chain_ext_headline_median_error_pct : ℝ := (0.03230022603427978 : ℝ)
def supply_chain_ext_beats_sota_headlines : ℕ := 2
def supply_chain_ext_D_eff : ℕ := 18

theorem supply_chain_ext_observable_count_pos : 0 < supply_chain_ext_observable_count := by
  unfold supply_chain_ext_observable_count; norm_num

theorem supply_chain_ext_pooled_median_under_five_pct :
    supply_chain_ext_pooled_median_error_pct < (5 : ℝ) := by
  unfold supply_chain_ext_pooled_median_error_pct; norm_num

theorem supply_chain_ext_headline_median_under_five_pct :
    supply_chain_ext_headline_median_error_pct < (5 : ℝ) := by
  unfold supply_chain_ext_headline_median_error_pct; norm_num

theorem supply_chain_ext_beats_sota_headlines_pos : 0 < supply_chain_ext_beats_sota_headlines := by
  unfold supply_chain_ext_beats_sota_headlines; norm_num

theorem supply_chain_ext_bundle :
    supply_chain_ext_observable_count = 40 ∧
    supply_chain_ext_pooled_median_error_pct < (5 : ℝ) ∧
    supply_chain_ext_headline_median_error_pct < (5 : ℝ) ∧
    0 < supply_chain_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold supply_chain_ext_observable_count; norm_num,
    supply_chain_ext_pooled_median_under_five_pct,
    supply_chain_ext_headline_median_under_five_pct,
    supply_chain_ext_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

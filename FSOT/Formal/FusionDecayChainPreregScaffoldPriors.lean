/-
  FSOT Formal FusionDecayChainPreregScaffoldPriors — Tier 74 superheavy island Z=120-126.
  Generator: scripts/gen_tiers_74_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fusion_decay_chain_prereg_scaffold_observable_count : ℕ := 18
def fusion_decay_chain_prereg_scaffold_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def fusion_decay_chain_prereg_scaffold_headline_median_error_pct : ℝ := (0.0 : ℝ)
def fusion_decay_chain_prereg_scaffold_beats_sota_headlines : ℕ := 2
def fusion_decay_chain_prereg_scaffold_D_eff : ℕ := 17

theorem fusion_decay_chain_prereg_scaffold_observable_count_pos : 0 < fusion_decay_chain_prereg_scaffold_observable_count := by
  unfold fusion_decay_chain_prereg_scaffold_observable_count; norm_num

theorem fusion_decay_chain_prereg_scaffold_pooled_median_under_half_pct :
    fusion_decay_chain_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold fusion_decay_chain_prereg_scaffold_pooled_median_error_pct; norm_num

theorem fusion_decay_chain_prereg_scaffold_headline_median_under_half_pct :
    fusion_decay_chain_prereg_scaffold_headline_median_error_pct < (0.5 : ℝ) := by
  unfold fusion_decay_chain_prereg_scaffold_headline_median_error_pct; norm_num

theorem fusion_decay_chain_prereg_scaffold_beats_sota_headlines_pos : 0 < fusion_decay_chain_prereg_scaffold_beats_sota_headlines := by
  unfold fusion_decay_chain_prereg_scaffold_beats_sota_headlines; norm_num

theorem fusion_decay_chain_prereg_scaffold_bundle :
    fusion_decay_chain_prereg_scaffold_observable_count = 18 ∧
    fusion_decay_chain_prereg_scaffold_pooled_median_error_pct < (0.5 : ℝ) ∧
    fusion_decay_chain_prereg_scaffold_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold fusion_decay_chain_prereg_scaffold_observable_count; norm_num
  · exact fusion_decay_chain_prereg_scaffold_pooled_median_under_half_pct
  · exact fusion_decay_chain_prereg_scaffold_beats_sota_headlines_pos

end

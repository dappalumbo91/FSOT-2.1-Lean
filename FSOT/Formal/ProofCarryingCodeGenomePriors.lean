/-
  FSOT Formal ProofCarryingCodeGenomePriors — Proof_Carrying_Code_Genome Tier L orbital gap fill.
  Generator: scripts/gen_tier_l_orbital_gap_fill_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def proof_cg_observable_count : ℕ := 25
def proof_cg_pooled_median_error_pct : ℝ := (0.0051685586271776884 : ℝ)
def proof_cg_headline_median_error_pct : ℝ := (0.0051685586271776884 : ℝ)
def proof_cg_beats_sota_headlines : ℕ := 2
def proof_cg_D_eff : ℕ := 16
def proof_cg_oss_affinity_pair_count : ℕ := 8

theorem proof_cg_observable_count_pos : 0 < proof_cg_observable_count := by
  unfold proof_cg_observable_count; norm_num

theorem proof_cg_pooled_median_under_half_pct :
    proof_cg_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold proof_cg_pooled_median_error_pct; norm_num

theorem proof_cg_headline_median_under_half_pct :
    proof_cg_headline_median_error_pct < (0.5 : ℝ) := by
  unfold proof_cg_headline_median_error_pct; norm_num

theorem proof_cg_beats_sota_headlines_pos : 0 < proof_cg_beats_sota_headlines := by
  unfold proof_cg_beats_sota_headlines; norm_num
theorem proof_cg_oss_pairs_pos : 0 < proof_cg_oss_affinity_pair_count := by unfold proof_cg_oss_affinity_pair_count; norm_num

theorem proof_cg_bundle :
    proof_cg_observable_count = 25 ∧
    proof_cg_pooled_median_error_pct < (0.5 : ℝ) ∧
    proof_cg_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold proof_cg_observable_count; norm_num
  · exact proof_cg_pooled_median_under_half_pct
  · exact proof_cg_beats_sota_headlines_pos

end

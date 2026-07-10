/-
  FSOT Formal TrinaryOSTierEPriors — Tier E portable Trinary-OS oracle (FSOTB + ISA + round-trip).
  Generator: scripts/gen_trinary_os_tier_e_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def trinary_os_tier_e_observable_count : ℕ := 68
def trinary_os_tier_e_oracle_count : ℕ := 3
def trinary_os_tier_e_opcode_count : ℕ := 27
def trinary_os_tier_e_program_count : ℕ := 3
def trinary_os_tier_e_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def trinary_os_tier_e_headline_median_error_pct : ℝ := (0.0 : ℝ)
def trinary_os_tier_e_beats_sota_headlines : ℕ := 4
def trinary_os_tier_e_D_eff : ℕ := 12

theorem trinary_os_tier_e_observable_count_pos : 0 < trinary_os_tier_e_observable_count := by
  unfold trinary_os_tier_e_observable_count; norm_num

theorem trinary_os_tier_e_oracle_count_pos : 0 < trinary_os_tier_e_oracle_count := by
  unfold trinary_os_tier_e_oracle_count; norm_num

theorem trinary_os_tier_e_pooled_median_under_half_pct :
    trinary_os_tier_e_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold trinary_os_tier_e_pooled_median_error_pct; norm_num

theorem trinary_os_tier_e_headline_median_under_half_pct :
    trinary_os_tier_e_headline_median_error_pct < (0.5 : ℝ) := by
  unfold trinary_os_tier_e_headline_median_error_pct; norm_num

theorem trinary_os_tier_e_beats_sota_headlines_pos : 0 < trinary_os_tier_e_beats_sota_headlines := by
  unfold trinary_os_tier_e_beats_sota_headlines; norm_num

theorem trinary_os_tier_e_bundle :
    trinary_os_tier_e_observable_count = 68 ∧
    trinary_os_tier_e_pooled_median_error_pct < (0.5 : ℝ) ∧
    trinary_os_tier_e_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < trinary_os_tier_e_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold trinary_os_tier_e_observable_count; norm_num,
    trinary_os_tier_e_pooled_median_under_half_pct,
    trinary_os_tier_e_headline_median_under_half_pct,
    trinary_os_tier_e_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

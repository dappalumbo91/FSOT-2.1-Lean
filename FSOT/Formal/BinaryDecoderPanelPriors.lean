/-
  FSOT Formal BinaryDecoderPanelPriors — Tier 88 application wiring (Binary_Decoder_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def binary_decoder_observable_count : ℕ := 8
def binary_decoder_median_error_pct : ℝ := (0.008488 : ℝ)
def binary_decoder_D_eff : ℕ := 13

theorem binary_decoder_observable_count_pos : 0 < binary_decoder_observable_count := by
  unfold binary_decoder_observable_count; norm_num

theorem binary_decoder_median_error_under_five_pct :
    binary_decoder_median_error_pct < (5 : ℝ) := by
  unfold binary_decoder_median_error_pct; norm_num

theorem binary_decoder_bundle :
    binary_decoder_observable_count = 8 ∧
    binary_decoder_D_eff = 13 ∧
    binary_decoder_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold binary_decoder_observable_count; norm_num,
    by unfold binary_decoder_D_eff; norm_num,
    binary_decoder_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

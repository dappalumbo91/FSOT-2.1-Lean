/-
  FSOT Formal BinaryDecoderRendleshamPriors — Rendlesham binary decoder crosswalk.
  Generator: scripts/gen_binary_decoder_rendlesham_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def binary_decoder_rendlesham_observable_count : ℕ := 10
def binary_decoder_rendlesham_median_error_pct : ℝ := (0.0 : ℝ)
def binary_decoder_rendlesham_D_eff : ℕ := 12

theorem binary_decoder_rendlesham_observable_count_pos : 0 < binary_decoder_rendlesham_observable_count := by
  unfold binary_decoder_rendlesham_observable_count; norm_num

theorem binary_decoder_rendlesham_median_error_under_five_pct :
    binary_decoder_rendlesham_median_error_pct < (5 : ℝ) := by
  unfold binary_decoder_rendlesham_median_error_pct; norm_num

theorem binary_decoder_rendlesham_bundle :
    binary_decoder_rendlesham_observable_count = 10 ∧
    binary_decoder_rendlesham_D_eff = 12 ∧
    binary_decoder_rendlesham_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold binary_decoder_rendlesham_observable_count; norm_num,
    by unfold binary_decoder_rendlesham_D_eff; norm_num,
    binary_decoder_rendlesham_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

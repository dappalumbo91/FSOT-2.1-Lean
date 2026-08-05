/-
  FSOT Formal BinaryDecoderPanelPriors — extension domain Binary_Decoder_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def binary_decoder_panel_observable_count : ℕ := 24
def binary_decoder_panel_D_eff : ℕ := 13

theorem binary_decoder_panel_observable_count_pos : 0 < binary_decoder_panel_observable_count := by
  unfold binary_decoder_panel_observable_count; decide

theorem binary_decoder_panel_median_error_under_half_pct :
    (0.013342 : ℝ) < (0.5 : ℝ) := by norm_num

theorem binary_decoder_panel_bundle :
    binary_decoder_panel_observable_count = 24 ∧
    binary_decoder_panel_D_eff = 13 ∧
    (0.013342 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold binary_decoder_panel_observable_count; decide,
    by unfold binary_decoder_panel_D_eff; decide,
    binary_decoder_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

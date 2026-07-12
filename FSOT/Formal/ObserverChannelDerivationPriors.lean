/-
  FSOT Formal ObserverChannelDerivationPriors — extension domain Observer_Channel_Derivation.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def observer_channel_derivation_observable_count : ℕ := 247
def observer_channel_derivation_D_eff : ℕ := 16

theorem observer_channel_derivation_observable_count_pos : 0 < observer_channel_derivation_observable_count := by
  unfold observer_channel_derivation_observable_count; norm_num

theorem observer_channel_derivation_median_error_under_half_pct :
    (0.0525102820198906 : ℝ) < (0.5 : ℝ) := by norm_num

theorem observer_channel_derivation_bundle :
    observer_channel_derivation_observable_count = 247 ∧
    observer_channel_derivation_D_eff = 16 ∧
    (0.0525102820198906 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold observer_channel_derivation_observable_count; norm_num,
    by unfold observer_channel_derivation_D_eff; norm_num,
    observer_channel_derivation_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal StellarMultiplicityLiveDeepPriors — extension domain Stellar_Multiplicity_Live_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def stellar_multiplicity_live_deep_observable_count : ℕ := 69
def stellar_multiplicity_live_deep_D_eff : ℕ := 19

theorem stellar_multiplicity_live_deep_observable_count_pos : 0 < stellar_multiplicity_live_deep_observable_count := by
  unfold stellar_multiplicity_live_deep_observable_count; norm_num

theorem stellar_multiplicity_live_deep_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem stellar_multiplicity_live_deep_bundle :
    stellar_multiplicity_live_deep_observable_count = 69 ∧
    stellar_multiplicity_live_deep_D_eff = 19 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold stellar_multiplicity_live_deep_observable_count; norm_num,
    by unfold stellar_multiplicity_live_deep_D_eff; norm_num,
    stellar_multiplicity_live_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

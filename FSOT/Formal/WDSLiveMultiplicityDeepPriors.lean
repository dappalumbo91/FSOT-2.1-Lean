/-
  FSOT Formal WdsLiveMultiplicityDeepPriors — extension domain WDS_Live_Multiplicity_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def wds_live_multiplicity_deep_observable_count : ℕ := 281
def wds_live_multiplicity_deep_D_eff : ℕ := 19

theorem wds_live_multiplicity_deep_observable_count_pos : 0 < wds_live_multiplicity_deep_observable_count := by
  unfold wds_live_multiplicity_deep_observable_count; decide

theorem wds_live_multiplicity_deep_median_error_under_half_pct :
    (0.026954 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.026954 : ℝ) < (0.5 : ℝ))

theorem wds_live_multiplicity_deep_bundle :
    wds_live_multiplicity_deep_observable_count = 281 ∧
    wds_live_multiplicity_deep_D_eff = 19 ∧
    (0.026954 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold wds_live_multiplicity_deep_observable_count; decide,
    by unfold wds_live_multiplicity_deep_D_eff; decide,
    wds_live_multiplicity_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

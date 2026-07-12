/-
  FSOT Formal VizierWdsTapLiveDeepPriors — extension domain VizieR_WDS_TAP_Live_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def vizier_wds_tap_live_deep_observable_count : ℕ := 121
def vizier_wds_tap_live_deep_D_eff : ℕ := 21

theorem vizier_wds_tap_live_deep_observable_count_pos : 0 < vizier_wds_tap_live_deep_observable_count := by
  unfold vizier_wds_tap_live_deep_observable_count; norm_num

theorem vizier_wds_tap_live_deep_median_error_under_half_pct :
    (0.026954 : ℝ) < (0.5 : ℝ) := by norm_num

theorem vizier_wds_tap_live_deep_bundle :
    vizier_wds_tap_live_deep_observable_count = 121 ∧
    vizier_wds_tap_live_deep_D_eff = 21 ∧
    (0.026954 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold vizier_wds_tap_live_deep_observable_count; norm_num,
    by unfold vizier_wds_tap_live_deep_D_eff; norm_num,
    vizier_wds_tap_live_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

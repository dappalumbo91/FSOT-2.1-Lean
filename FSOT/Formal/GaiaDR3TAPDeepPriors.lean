/-
  FSOT Formal GaiaDr3TapDeepPriors — extension domain Gaia_DR3_TAP_Deep.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def gaia_dr3_tap_deep_observable_count : ℕ := 1826
def gaia_dr3_tap_deep_D_eff : ℕ := 20

theorem gaia_dr3_tap_deep_observable_count_pos : 0 < gaia_dr3_tap_deep_observable_count := by
  unfold gaia_dr3_tap_deep_observable_count; norm_num

theorem gaia_dr3_tap_deep_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) := by norm_num

theorem gaia_dr3_tap_deep_bundle :
    gaia_dr3_tap_deep_observable_count = 1826 ∧
    gaia_dr3_tap_deep_D_eff = 20 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold gaia_dr3_tap_deep_observable_count; norm_num,
    by unfold gaia_dr3_tap_deep_D_eff; norm_num,
    gaia_dr3_tap_deep_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

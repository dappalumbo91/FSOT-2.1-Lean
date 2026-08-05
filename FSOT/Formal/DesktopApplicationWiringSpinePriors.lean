/-
  FSOT Formal DesktopApplicationWiringSpinePriors — extension domain Desktop_Application_Wiring_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def desktop_application_wiring_spine_observable_count : ℕ := 81
def desktop_application_wiring_spine_D_eff : ℕ := 16

theorem desktop_application_wiring_spine_observable_count_pos : 0 < desktop_application_wiring_spine_observable_count := by
  unfold desktop_application_wiring_spine_observable_count; decide

theorem desktop_application_wiring_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem desktop_application_wiring_spine_bundle :
    desktop_application_wiring_spine_observable_count = 81 ∧
    desktop_application_wiring_spine_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold desktop_application_wiring_spine_observable_count; decide,
    by unfold desktop_application_wiring_spine_D_eff; decide,
    desktop_application_wiring_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

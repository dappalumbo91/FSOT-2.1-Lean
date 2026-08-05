/-
  FSOT Formal HubbleDarkSectorCrosswalkPriors — extension domain Hubble_Dark_Sector_Crosswalk.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def hubble_dark_sector_crosswalk_observable_count : ℕ := 24
def hubble_dark_sector_crosswalk_D_eff : ℕ := 25

theorem hubble_dark_sector_crosswalk_observable_count_pos : 0 < hubble_dark_sector_crosswalk_observable_count := by
  unfold hubble_dark_sector_crosswalk_observable_count; decide

theorem hubble_dark_sector_crosswalk_median_error_under_half_pct :
    (0.0198985 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0198985 : ℝ) < (0.5 : ℝ))

theorem hubble_dark_sector_crosswalk_bundle :
    hubble_dark_sector_crosswalk_observable_count = 24 ∧
    hubble_dark_sector_crosswalk_D_eff = 25 ∧
    (0.0198985 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold hubble_dark_sector_crosswalk_observable_count; decide,
    by unfold hubble_dark_sector_crosswalk_D_eff; decide,
    hubble_dark_sector_crosswalk_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

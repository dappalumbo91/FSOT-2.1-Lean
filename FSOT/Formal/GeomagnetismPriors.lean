/-
  FSOT Formal GeomagnetismPriors — NOAA SWPC Dst/GOES storm classifier.
  Generator: scripts/gen_geomagnetism_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def geomagnetism_observable_count : ℕ := 525
def geomagnetism_match_count : ℕ := 525
def geomagnetism_D_eff : ℕ := 13
def geomagnetism_match_rate : ℝ := (1.0 : ℝ)

theorem geomagnetism_observable_count_pos : 0 < geomagnetism_observable_count := by
  unfold geomagnetism_observable_count; norm_num

theorem geomagnetism_match_le_total : geomagnetism_match_count ≤ geomagnetism_observable_count := by
  unfold geomagnetism_match_count geomagnetism_observable_count; norm_num

theorem geomagnetism_bundle :
    geomagnetism_observable_count = 525 ∧
    geomagnetism_match_count = 525 ∧
    geomagnetism_D_eff = 13 ∧
    geomagnetism_match_count ≤ geomagnetism_observable_count ∧
    raw_S (get_domain_params "electron") > 0 := by
  refine ⟨
    by unfold geomagnetism_observable_count; norm_num,
    by unfold geomagnetism_match_count; norm_num,
    by unfold geomagnetism_D_eff; norm_num,
    geomagnetism_match_le_total,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal

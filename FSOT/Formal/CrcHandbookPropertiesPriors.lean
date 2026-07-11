/-
  FSOT Formal CrcHandbookPropertiesPriors — reference anchor (CRC_Handbook_Properties).
  Generator: scripts/gen_reference_anchors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def crc_handbook_properties_observable_count : ℕ := 391
def crc_handbook_properties_median_error_pct : ℝ := (0.026922 : ℝ)
def crc_handbook_properties_D_eff : ℕ := 11

theorem crc_handbook_properties_observable_count_pos : 0 < crc_handbook_properties_observable_count := by
  unfold crc_handbook_properties_observable_count; norm_num

theorem crc_handbook_properties_median_error_under_five_pct :
    crc_handbook_properties_median_error_pct < (5 : ℝ) := by
  unfold crc_handbook_properties_median_error_pct; norm_num

theorem crc_handbook_properties_bundle :
    crc_handbook_properties_observable_count = 391 ∧
    crc_handbook_properties_D_eff = 11 ∧
    crc_handbook_properties_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "chemical") > 0 := by
  refine ⟨
    by unfold crc_handbook_properties_observable_count; norm_num,
    by unfold crc_handbook_properties_D_eff; norm_num,
    crc_handbook_properties_median_error_under_five_pct,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal

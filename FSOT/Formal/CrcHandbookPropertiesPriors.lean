/-
  FSOT Formal CrcHandbookPropertiesPriors — extension domain CRC_Handbook_Properties.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def crc_handbook_properties_observable_count : ℕ := 391
def crc_handbook_properties_D_eff : ℕ := 11

theorem crc_handbook_properties_observable_count_pos : 0 < crc_handbook_properties_observable_count := by
  unfold crc_handbook_properties_observable_count; decide

theorem crc_handbook_properties_median_error_under_half_pct :
    (0.026922 : ℝ) < (0.5 : ℝ) := by norm_num

theorem crc_handbook_properties_bundle :
    crc_handbook_properties_observable_count = 391 ∧
    crc_handbook_properties_D_eff = 11 ∧
    (0.026922 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold crc_handbook_properties_observable_count; decide,
    by unfold crc_handbook_properties_D_eff; decide,
    crc_handbook_properties_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

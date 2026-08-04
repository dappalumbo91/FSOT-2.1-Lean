/-
  FSOT Formal FsotCPackParityPanelPriors — hardware depth (FSOT_C_Pack_Parity_Panel).
  Generator: scripts/gen_hardware_depth_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fsot_c_pack_parity_observable_count : ℕ := 23
def fsot_c_pack_parity_median_error_pct : ℝ := (0.0 : ℝ)
def fsot_c_pack_parity_D_eff : ℕ := 10

theorem fsot_c_pack_parity_observable_count_pos : 0 < fsot_c_pack_parity_observable_count := by
  unfold fsot_c_pack_parity_observable_count; norm_num

theorem fsot_c_pack_parity_median_error_under_half_pct :
    fsot_c_pack_parity_median_error_pct < (0.5 : ℝ) := by
  unfold fsot_c_pack_parity_median_error_pct; norm_num

theorem fsot_c_pack_parity_bundle :
    fsot_c_pack_parity_observable_count = 23 ∧
    fsot_c_pack_parity_D_eff = 10 ∧
    fsot_c_pack_parity_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fsot_c_pack_parity_observable_count; norm_num,
    by unfold fsot_c_pack_parity_D_eff; norm_num,
    fsot_c_pack_parity_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

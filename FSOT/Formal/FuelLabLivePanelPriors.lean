/-
  FSOT Formal FuelLabLivePanelPriors — Tier 88 application wiring (Fuel_Lab_Live_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fuel_lab_live_observable_count : ℕ := 25
def fuel_lab_live_median_error_pct : ℝ := (0.039349 : ℝ)
def fuel_lab_live_D_eff : ℕ := 16

theorem fuel_lab_live_observable_count_pos : 0 < fuel_lab_live_observable_count := by
  unfold fuel_lab_live_observable_count; norm_num

theorem fuel_lab_live_median_error_under_five_pct :
    fuel_lab_live_median_error_pct < (5 : ℝ) := by
  unfold fuel_lab_live_median_error_pct; norm_num

theorem fuel_lab_live_bundle :
    fuel_lab_live_observable_count = 25 ∧
    fuel_lab_live_D_eff = 16 ∧
    fuel_lab_live_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fuel_lab_live_observable_count; norm_num,
    by unfold fuel_lab_live_D_eff; norm_num,
    fuel_lab_live_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

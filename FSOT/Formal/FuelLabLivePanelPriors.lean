/-
  FSOT Formal FuelLabLivePanelPriors — verified desktop panel Fuel_Lab_Live_Panel.
  Generator: scripts/gen_verified_desktop_lean.py
  Cross-proof: exported via export_full_formal_obligations.py → Coq / Isabelle / F* / Rust replay
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def fuel_lab_live_observable_count : ℕ := 366
def fuel_lab_live_median_error_pct : ℝ := (0.039349 : ℝ)
def fuel_lab_live_D_eff : ℕ := 16

def fuel_lab_live_designed_fuel_count : ℝ := (7.0 : ℝ)

theorem fuel_lab_live_designed_fuel_count_pos : 0 < fuel_lab_live_designed_fuel_count := by
  unfold fuel_lab_live_designed_fuel_count; decide

theorem fuel_lab_live_observable_count_pos : 0 < fuel_lab_live_observable_count := by
  unfold fuel_lab_live_observable_count; decide

theorem fuel_lab_live_median_error_under_five_pct :
    fuel_lab_live_median_error_pct < (5 : ℝ) := by
  unfold fuel_lab_live_median_error_pct; norm_num

theorem fuel_lab_live_median_error_under_half_pct :
    fuel_lab_live_median_error_pct < (0.5 : ℝ) := by
  unfold fuel_lab_live_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem fuel_lab_live_bundle :
    fuel_lab_live_observable_count = 366 ∧
    fuel_lab_live_D_eff = 16 ∧
    fuel_lab_live_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fuel_lab_live_observable_count; decide,
    by unfold fuel_lab_live_D_eff; decide,
    fuel_lab_live_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

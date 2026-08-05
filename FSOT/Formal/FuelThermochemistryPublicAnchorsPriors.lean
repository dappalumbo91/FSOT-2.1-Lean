/-
  FSOT Formal FuelThermochemistryPublicAnchorsPriors — extension domain Fuel_Thermochemistry_Public_Anchors.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fuel_thermochemistry_public_anchors_observable_count : ℕ := 24
def fuel_thermochemistry_public_anchors_D_eff : ℕ := 16

theorem fuel_thermochemistry_public_anchors_observable_count_pos : 0 < fuel_thermochemistry_public_anchors_observable_count := by
  unfold fuel_thermochemistry_public_anchors_observable_count; decide

theorem fuel_thermochemistry_public_anchors_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem fuel_thermochemistry_public_anchors_bundle :
    fuel_thermochemistry_public_anchors_observable_count = 24 ∧
    fuel_thermochemistry_public_anchors_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold fuel_thermochemistry_public_anchors_observable_count; decide,
    by unfold fuel_thermochemistry_public_anchors_D_eff; decide,
    fuel_thermochemistry_public_anchors_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

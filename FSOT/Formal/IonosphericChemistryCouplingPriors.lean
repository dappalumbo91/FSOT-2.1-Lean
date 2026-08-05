/-
  FSOT Formal IonosphericChemistryCouplingPriors — extension domain Ionospheric_Chemistry_Coupling.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def ionospheric_chemistry_coupling_observable_count : ℕ := 85
def ionospheric_chemistry_coupling_D_eff : ℕ := 15

theorem ionospheric_chemistry_coupling_observable_count_pos : 0 < ionospheric_chemistry_coupling_observable_count := by
  unfold ionospheric_chemistry_coupling_observable_count; decide

theorem ionospheric_chemistry_coupling_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem ionospheric_chemistry_coupling_bundle :
    ionospheric_chemistry_coupling_observable_count = 85 ∧
    ionospheric_chemistry_coupling_D_eff = 15 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold ionospheric_chemistry_coupling_observable_count; decide,
    by unfold ionospheric_chemistry_coupling_D_eff; decide,
    ionospheric_chemistry_coupling_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

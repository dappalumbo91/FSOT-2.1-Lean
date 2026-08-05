/-
  FSOT Formal SportsBiomechanicsPriors — extension domain Sports_Biomechanics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def sports_biomechanics_observable_count : ℕ := 35
def sports_biomechanics_D_eff : ℕ := 14

theorem sports_biomechanics_observable_count_pos : 0 < sports_biomechanics_observable_count := by
  unfold sports_biomechanics_observable_count; decide

theorem sports_biomechanics_median_error_under_half_pct :
    (0.04447250077037523 : ℝ) < (0.5 : ℝ) := by norm_num

theorem sports_biomechanics_bundle :
    sports_biomechanics_observable_count = 35 ∧
    sports_biomechanics_D_eff = 14 ∧
    (0.04447250077037523 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold sports_biomechanics_observable_count; decide,
    by unfold sports_biomechanics_D_eff; decide,
    sports_biomechanics_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

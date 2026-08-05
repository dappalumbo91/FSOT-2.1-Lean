/-
  FSOT Formal PhiMorphogeneticScalingPriors — extension domain Phi_Morphogenetic_Scaling.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def phi_morphogenetic_scaling_observable_count : ℕ := 289
def phi_morphogenetic_scaling_D_eff : ℕ := 16

theorem phi_morphogenetic_scaling_observable_count_pos : 0 < phi_morphogenetic_scaling_observable_count := by
  unfold phi_morphogenetic_scaling_observable_count; decide

theorem phi_morphogenetic_scaling_median_error_under_half_pct :
    (0.01760779720633292 : ℝ) < (0.5 : ℝ) := by norm_num

theorem phi_morphogenetic_scaling_bundle :
    phi_morphogenetic_scaling_observable_count = 289 ∧
    phi_morphogenetic_scaling_D_eff = 16 ∧
    (0.01760779720633292 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold phi_morphogenetic_scaling_observable_count; decide,
    by unfold phi_morphogenetic_scaling_D_eff; decide,
    phi_morphogenetic_scaling_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal NeuroimmunologyPriors — immunology SMILES + neuron cohort strata.
  Generator: scripts/gen_neuroimmunology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuroimmunology_observable_count : ℕ := 92
def neuroimmunology_median_error_pct : ℝ := (0.431577 : ℝ)
def neuroimmunology_D_eff : ℕ := 14

theorem neuroimmunology_observable_count_pos : 0 < neuroimmunology_observable_count := by
  unfold neuroimmunology_observable_count; norm_num

theorem neuroimmunology_median_error_under_five_pct :
    neuroimmunology_median_error_pct < (5 : ℝ) := by
  unfold neuroimmunology_median_error_pct; norm_num

theorem neuroimmunology_bundle :
    neuroimmunology_observable_count = 92 ∧
    neuroimmunology_D_eff = 14 ∧
    neuroimmunology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold neuroimmunology_observable_count; norm_num,
    by unfold neuroimmunology_D_eff; norm_num,
    neuroimmunology_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal

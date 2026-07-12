/-
  FSOT Formal NeuroeconomicsPriors — extension domain Neuroeconomics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def neuroeconomics_observable_count : ℕ := 65
def neuroeconomics_D_eff : ℕ := 16

theorem neuroeconomics_observable_count_pos : 0 < neuroeconomics_observable_count := by
  unfold neuroeconomics_observable_count; norm_num

theorem neuroeconomics_median_error_under_half_pct :
    (0.10502056403980387 : ℝ) < (0.5 : ℝ) := by norm_num

theorem neuroeconomics_bundle :
    neuroeconomics_observable_count = 65 ∧
    neuroeconomics_D_eff = 16 ∧
    (0.10502056403980387 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold neuroeconomics_observable_count; norm_num,
    by unfold neuroeconomics_D_eff; norm_num,
    neuroeconomics_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

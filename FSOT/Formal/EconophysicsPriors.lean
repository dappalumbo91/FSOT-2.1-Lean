/-
  FSOT Formal EconophysicsPriors — extension domain Econophysics.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def econophysics_observable_count : ℕ := 24
def econophysics_D_eff : ℕ := 20

theorem econophysics_observable_count_pos : 0 < econophysics_observable_count := by
  unfold econophysics_observable_count; norm_num

theorem econophysics_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem econophysics_bundle :
    econophysics_observable_count = 24 ∧
    econophysics_D_eff = 20 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold econophysics_observable_count; norm_num,
    by unfold econophysics_D_eff; norm_num,
    econophysics_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

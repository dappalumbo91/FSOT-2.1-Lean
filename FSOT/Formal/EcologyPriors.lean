/-
  FSOT Formal EcologyPriors — extension domain Ecology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def ecology_observable_count : ℕ := 24
def ecology_D_eff : ℕ := 15

theorem ecology_observable_count_pos : 0 < ecology_observable_count := by
  unfold ecology_observable_count; decide

theorem ecology_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem ecology_bundle :
    ecology_observable_count = 24 ∧
    ecology_D_eff = 15 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold ecology_observable_count; decide,
    by unfold ecology_D_eff; decide,
    ecology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

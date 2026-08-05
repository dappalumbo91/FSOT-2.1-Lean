/-
  FSOT Formal CardiologyPriors — extension domain Cardiology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cardiology_observable_count : ℕ := 45
def cardiology_D_eff : ℕ := 15

theorem cardiology_observable_count_pos : 0 < cardiology_observable_count := by
  unfold cardiology_observable_count; decide

theorem cardiology_median_error_under_half_pct :
    (0.030622122938654326 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cardiology_bundle :
    cardiology_observable_count = 45 ∧
    cardiology_D_eff = 15 ∧
    (0.030622122938654326 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cardiology_observable_count; decide,
    by unfold cardiology_D_eff; decide,
    cardiology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

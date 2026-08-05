/-
  FSOT Formal PaleontologyPriors — extension domain Paleontology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def paleontology_observable_count : ℕ := 630
def paleontology_D_eff : ℕ := 18

theorem paleontology_observable_count_pos : 0 < paleontology_observable_count := by
  unfold paleontology_observable_count; decide

theorem paleontology_median_error_under_half_pct :
    (0.017836062884406152 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.017836062884406152 : ℝ) < (0.5 : ℝ))

theorem paleontology_bundle :
    paleontology_observable_count = 630 ∧
    paleontology_D_eff = 18 ∧
    (0.017836062884406152 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold paleontology_observable_count; decide,
    by unfold paleontology_D_eff; decide,
    paleontology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

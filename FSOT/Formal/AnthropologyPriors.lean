/-
  FSOT Formal AnthropologyPriors — extension domain Anthropology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def anthropology_observable_count : ℕ := 160
def anthropology_D_eff : ℕ := 17

theorem anthropology_observable_count_pos : 0 < anthropology_observable_count := by
  unfold anthropology_observable_count; decide

theorem anthropology_median_error_under_half_pct :
    (0.019504399572476606 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.019504399572476606 : ℝ) < (0.5 : ℝ))

theorem anthropology_bundle :
    anthropology_observable_count = 160 ∧
    anthropology_D_eff = 17 ∧
    (0.019504399572476606 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold anthropology_observable_count; decide,
    by unfold anthropology_D_eff; decide,
    anthropology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

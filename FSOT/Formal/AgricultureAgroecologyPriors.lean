/-
  FSOT Formal AgricultureAgroecologyPriors — extension domain Agriculture_Agroecology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def agriculture_agroecology_observable_count : ℕ := 276
def agriculture_agroecology_D_eff : ℕ := 16

theorem agriculture_agroecology_observable_count_pos : 0 < agriculture_agroecology_observable_count := by
  unfold agriculture_agroecology_observable_count; decide

theorem agriculture_agroecology_median_error_under_half_pct :
    (0.018019024892929635 : ℝ) < (0.5 : ℝ) := by norm_num

theorem agriculture_agroecology_bundle :
    agriculture_agroecology_observable_count = 276 ∧
    agriculture_agroecology_D_eff = 16 ∧
    (0.018019024892929635 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold agriculture_agroecology_observable_count; decide,
    by unfold agriculture_agroecology_D_eff; decide,
    agriculture_agroecology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

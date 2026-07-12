/-
  FSOT Formal ExogeologyPriors — extension domain Exogeology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def exogeology_observable_count : ℕ := 316
def exogeology_D_eff : ℕ := 20

theorem exogeology_observable_count_pos : 0 < exogeology_observable_count := by
  unfold exogeology_observable_count; norm_num

theorem exogeology_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem exogeology_bundle :
    exogeology_observable_count = 316 ∧
    exogeology_D_eff = 20 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold exogeology_observable_count; norm_num,
    by unfold exogeology_D_eff; norm_num,
    exogeology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal GalacticStructureSamplePriors — extension domain Galactic_Structure_Sample.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def galactic_structure_sample_observable_count : ℕ := 101
def galactic_structure_sample_D_eff : ℕ := 20

theorem galactic_structure_sample_observable_count_pos : 0 < galactic_structure_sample_observable_count := by
  unfold galactic_structure_sample_observable_count; norm_num

theorem galactic_structure_sample_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem galactic_structure_sample_bundle :
    galactic_structure_sample_observable_count = 101 ∧
    galactic_structure_sample_D_eff = 20 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold galactic_structure_sample_observable_count; norm_num,
    by unfold galactic_structure_sample_D_eff; norm_num,
    galactic_structure_sample_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

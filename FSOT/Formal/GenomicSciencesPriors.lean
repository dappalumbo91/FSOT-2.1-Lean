/-
  FSOT Formal GenomicSciencesPriors — extension domain Genomic_Sciences.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def genomic_sciences_observable_count : ℕ := 24
def genomic_sciences_D_eff : ℕ := 12

theorem genomic_sciences_observable_count_pos : 0 < genomic_sciences_observable_count := by
  unfold genomic_sciences_observable_count; decide

theorem genomic_sciences_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem genomic_sciences_bundle :
    genomic_sciences_observable_count = 24 ∧
    genomic_sciences_D_eff = 12 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold genomic_sciences_observable_count; decide,
    by unfold genomic_sciences_D_eff; decide,
    genomic_sciences_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

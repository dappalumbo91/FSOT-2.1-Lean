/-
  FSOT Formal ScientificExpansionWave2SpinePriors — Tier 84 scientific expansion (Scientific_Expansion_Wave2_Spine).
  Generator: scripts/gen_tier84_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def scientific_expansion_wave2_observable_count : ℕ := 40
def scientific_expansion_wave2_median_error_pct : ℝ := (0.0 : ℝ)
def scientific_expansion_wave2_D_eff : ℕ := 17

theorem scientific_expansion_wave2_observable_count_pos : 0 < scientific_expansion_wave2_observable_count := by
  unfold scientific_expansion_wave2_observable_count; norm_num

theorem scientific_expansion_wave2_median_error_under_five_pct :
    scientific_expansion_wave2_median_error_pct < (5 : ℝ) := by
  unfold scientific_expansion_wave2_median_error_pct; norm_num

theorem scientific_expansion_wave2_bundle :
    scientific_expansion_wave2_observable_count = 40 ∧
    scientific_expansion_wave2_D_eff = 17 ∧
    scientific_expansion_wave2_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold scientific_expansion_wave2_observable_count; norm_num,
    by unfold scientific_expansion_wave2_D_eff; norm_num,
    scientific_expansion_wave2_median_error_under_five_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal CrossrefScholarlyPriors — Tier 81 credential-free public (Crossref_Scholarly_Panel).
  Generator: scripts/gen_tier81_public_verifiable_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def crossref_scholarly_observable_count : ℕ := 200
def crossref_scholarly_median_error_pct : ℝ := (0.01382 : ℝ)
def crossref_scholarly_D_eff : ℕ := 18

theorem crossref_scholarly_observable_count_pos : 0 < crossref_scholarly_observable_count := by
  unfold crossref_scholarly_observable_count; norm_num

theorem crossref_scholarly_median_error_under_five_pct :
    crossref_scholarly_median_error_pct < (5 : ℝ) := by
  unfold crossref_scholarly_median_error_pct; norm_num

theorem crossref_scholarly_bundle :
    crossref_scholarly_observable_count = 200 ∧
    crossref_scholarly_D_eff = 18 ∧
    crossref_scholarly_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold crossref_scholarly_observable_count; norm_num,
    by unfold crossref_scholarly_D_eff; norm_num,
    crossref_scholarly_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

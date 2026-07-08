/-
  FSOT Formal TokenizationSmokePriors — Dictionary tokenization smoke crosswalk.
  Generator: scripts/gen_tokenization_smoke_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def tokenization_smoke_observable_count : ℕ := 9
def tokenization_smoke_median_error_pct : ℝ := (0.0 : ℝ)
def tokenization_smoke_D_eff : ℕ := 12

theorem tokenization_smoke_observable_count_pos : 0 < tokenization_smoke_observable_count := by
  unfold tokenization_smoke_observable_count; norm_num

theorem tokenization_smoke_median_error_under_five_pct :
    tokenization_smoke_median_error_pct < (5 : ℝ) := by
  unfold tokenization_smoke_median_error_pct; norm_num

theorem tokenization_smoke_bundle :
    tokenization_smoke_observable_count = 9 ∧
    tokenization_smoke_D_eff = 12 ∧
    tokenization_smoke_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold tokenization_smoke_observable_count; norm_num,
    by unfold tokenization_smoke_D_eff; norm_num,
    tokenization_smoke_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

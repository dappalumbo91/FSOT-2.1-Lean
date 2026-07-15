/-
  FSOT Formal CanonicalOraclePanelPriors — Tier 88 application wiring (Canonical_Oracle_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def canonical_oracle_observable_count : ℕ := 6
def canonical_oracle_median_error_pct : ℝ := (0.013294 : ℝ)
def canonical_oracle_D_eff : ℕ := 18

theorem canonical_oracle_observable_count_pos : 0 < canonical_oracle_observable_count := by
  unfold canonical_oracle_observable_count; norm_num

theorem canonical_oracle_median_error_under_five_pct :
    canonical_oracle_median_error_pct < (5 : ℝ) := by
  unfold canonical_oracle_median_error_pct; norm_num

theorem canonical_oracle_bundle :
    canonical_oracle_observable_count = 6 ∧
    canonical_oracle_D_eff = 18 ∧
    canonical_oracle_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "mathematical") > 0 := by
  refine ⟨
    by unfold canonical_oracle_observable_count; norm_num,
    by unfold canonical_oracle_D_eff; norm_num,
    canonical_oracle_median_error_under_five_pct,
    mathematical_raw_S_positive
  ⟩

end

end FSOT.Formal

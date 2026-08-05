/-
  FSOT Formal OstiDoeSciencePriors — Tier 80 government open data (OSTI_DOE_Science_Panel).
  Generator: scripts/gen_tier80_government_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def osti_doe_science_observable_count : ℕ := 100
def osti_doe_science_median_error_pct : ℝ := (0.01382 : ℝ)
def osti_doe_science_D_eff : ℕ := 18

theorem osti_doe_science_observable_count_pos : 0 < osti_doe_science_observable_count := by
  unfold osti_doe_science_observable_count; decide

theorem osti_doe_science_median_error_under_five_pct :
    osti_doe_science_median_error_pct < (5 : ℝ) := by
  unfold osti_doe_science_median_error_pct
  exact (by norm_num : (0.01382  : ℝ) < (5 : ℝ))

theorem osti_doe_science_bundle :
    osti_doe_science_observable_count = 100 ∧
    osti_doe_science_D_eff = 18 ∧
    osti_doe_science_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "nuclear") > 0 := by
  refine ⟨
    by unfold osti_doe_science_observable_count; decide,
    by unfold osti_doe_science_D_eff; decide,
    osti_doe_science_median_error_under_five_pct,
    nuclear_raw_S_positive
  ⟩

end

end FSOT.Formal

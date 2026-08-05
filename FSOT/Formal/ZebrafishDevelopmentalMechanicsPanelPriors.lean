/-
  FSOT Formal ZebrafishDevelopmentalMechanicsPanelPriors — Tier 95 Zebrahub developmental (Zebrafish_Developmental_Mechanics_Panel).
  Generator: scripts/gen_tier95_zebrahub_development_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def zebrafish_developmental_mechanics_observable_count : ℕ := 31
def zebrafish_developmental_mechanics_median_error_pct : ℝ := (0.017789 : ℝ)
def zebrafish_developmental_mechanics_D_eff : ℕ := 21

theorem zebrafish_developmental_mechanics_observable_count_pos : 0 < zebrafish_developmental_mechanics_observable_count := by
  unfold zebrafish_developmental_mechanics_observable_count; decide

theorem zebrafish_developmental_mechanics_median_error_under_five_pct :
    zebrafish_developmental_mechanics_median_error_pct < (5 : ℝ) := by
  unfold zebrafish_developmental_mechanics_median_error_pct; norm_num

theorem zebrafish_developmental_mechanics_bundle :
    zebrafish_developmental_mechanics_observable_count = 31 ∧
    zebrafish_developmental_mechanics_D_eff = 21 ∧
    zebrafish_developmental_mechanics_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold zebrafish_developmental_mechanics_observable_count; decide,
    by unfold zebrafish_developmental_mechanics_D_eff; decide,
    zebrafish_developmental_mechanics_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal

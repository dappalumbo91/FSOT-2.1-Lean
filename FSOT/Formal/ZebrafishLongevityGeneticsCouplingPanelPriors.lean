/-
  FSOT Formal ZebrafishLongevityGeneticsCouplingPanelPriors — Tier 95 Zebrahub developmental (Zebrafish_Longevity_Genetics_Coupling_Panel).
  Generator: scripts/gen_tier95_zebrahub_development_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def zebrafish_longevity_genetics_coupling_observable_count : ℕ := 15
def zebrafish_longevity_genetics_coupling_median_error_pct : ℝ := (0.013342 : ℝ)
def zebrafish_longevity_genetics_coupling_D_eff : ℕ := 22

theorem zebrafish_longevity_genetics_coupling_observable_count_pos : 0 < zebrafish_longevity_genetics_coupling_observable_count := by
  unfold zebrafish_longevity_genetics_coupling_observable_count; decide

theorem zebrafish_longevity_genetics_coupling_median_error_under_five_pct :
    zebrafish_longevity_genetics_coupling_median_error_pct < (5 : ℝ) := by
  unfold zebrafish_longevity_genetics_coupling_median_error_pct; norm_num

theorem zebrafish_longevity_genetics_coupling_bundle :
    zebrafish_longevity_genetics_coupling_observable_count = 15 ∧
    zebrafish_longevity_genetics_coupling_D_eff = 22 ∧
    zebrafish_longevity_genetics_coupling_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold zebrafish_longevity_genetics_coupling_observable_count; decide,
    by unfold zebrafish_longevity_genetics_coupling_D_eff; decide,
    zebrafish_longevity_genetics_coupling_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal LongevityMegaDeepNcbiPanelPriors — Tier 94 longevity genetics (Longevity_MegaDeep_NCBI_Panel).
  Generator: scripts/gen_tier94_longevity_genetics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def longevity_megadeep_ncbi_observable_count : ℕ := 1746
def longevity_megadeep_ncbi_median_error_pct : ℝ := (0.017789 : ℝ)
def longevity_megadeep_ncbi_D_eff : ℕ := 23

theorem longevity_megadeep_ncbi_observable_count_pos : 0 < longevity_megadeep_ncbi_observable_count := by
  unfold longevity_megadeep_ncbi_observable_count; decide

theorem longevity_megadeep_ncbi_median_error_under_five_pct :
    longevity_megadeep_ncbi_median_error_pct < (5 : ℝ) := by
  unfold longevity_megadeep_ncbi_median_error_pct
  exact (by norm_num : (0.017789  : ℝ) < (5 : ℝ))

theorem longevity_megadeep_ncbi_bundle :
    longevity_megadeep_ncbi_observable_count = 1746 ∧
    longevity_megadeep_ncbi_D_eff = 23 ∧
    longevity_megadeep_ncbi_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold longevity_megadeep_ncbi_observable_count; decide,
    by unfold longevity_megadeep_ncbi_D_eff; decide,
    longevity_megadeep_ncbi_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal

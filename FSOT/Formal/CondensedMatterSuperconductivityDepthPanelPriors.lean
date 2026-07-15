/-
  FSOT Formal CondensedMatterSuperconductivityDepthPanelPriors — Tier 87 depth wave (Condensed_Matter_Superconductivity_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def condensed_matter_superconductivity_depth_observable_count : ℕ := 15
def condensed_matter_superconductivity_depth_median_error_pct : ℝ := (0.033841 : ℝ)
def condensed_matter_superconductivity_depth_D_eff : ℕ := 16

theorem condensed_matter_superconductivity_depth_observable_count_pos : 0 < condensed_matter_superconductivity_depth_observable_count := by
  unfold condensed_matter_superconductivity_depth_observable_count; norm_num

theorem condensed_matter_superconductivity_depth_median_error_under_five_pct :
    condensed_matter_superconductivity_depth_median_error_pct < (5 : ℝ) := by
  unfold condensed_matter_superconductivity_depth_median_error_pct; norm_num

theorem condensed_matter_superconductivity_depth_bundle :
    condensed_matter_superconductivity_depth_observable_count = 15 ∧
    condensed_matter_superconductivity_depth_D_eff = 16 ∧
    condensed_matter_superconductivity_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold condensed_matter_superconductivity_depth_observable_count; norm_num,
    by unfold condensed_matter_superconductivity_depth_D_eff; norm_num,
    condensed_matter_superconductivity_depth_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal

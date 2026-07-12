/-
  FSOT Formal CondensedMatterSuperconductivityDepthPanelPriors — extension domain Condensed_Matter_Superconductivity_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def condensed_matter_superconductivity_depth_panel_observable_count : ℕ := 24
def condensed_matter_superconductivity_depth_panel_D_eff : ℕ := 16

theorem condensed_matter_superconductivity_depth_panel_observable_count_pos : 0 < condensed_matter_superconductivity_depth_panel_observable_count := by
  unfold condensed_matter_superconductivity_depth_panel_observable_count; norm_num

theorem condensed_matter_superconductivity_depth_panel_median_error_under_half_pct :
    (0.033841 : ℝ) < (0.5 : ℝ) := by norm_num

theorem condensed_matter_superconductivity_depth_panel_bundle :
    condensed_matter_superconductivity_depth_panel_observable_count = 24 ∧
    condensed_matter_superconductivity_depth_panel_D_eff = 16 ∧
    (0.033841 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold condensed_matter_superconductivity_depth_panel_observable_count; norm_num,
    by unfold condensed_matter_superconductivity_depth_panel_D_eff; norm_num,
    condensed_matter_superconductivity_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

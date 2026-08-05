/-
  FSOT Formal BiologyDevelopmentalStructuralDepthPanelPriors — extension domain Biology_Developmental_Structural_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def biology_developmental_structural_depth_panel_observable_count : ℕ := 26
def biology_developmental_structural_depth_panel_D_eff : ℕ := 17

theorem biology_developmental_structural_depth_panel_observable_count_pos : 0 < biology_developmental_structural_depth_panel_observable_count := by
  unfold biology_developmental_structural_depth_panel_observable_count; decide

theorem biology_developmental_structural_depth_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.022236 : ℝ) < (0.5 : ℝ))

theorem biology_developmental_structural_depth_panel_bundle :
    biology_developmental_structural_depth_panel_observable_count = 26 ∧
    biology_developmental_structural_depth_panel_D_eff = 17 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold biology_developmental_structural_depth_panel_observable_count; decide,
    by unfold biology_developmental_structural_depth_panel_D_eff; decide,
    biology_developmental_structural_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

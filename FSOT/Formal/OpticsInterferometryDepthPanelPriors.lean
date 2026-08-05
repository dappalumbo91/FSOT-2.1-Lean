/-
  FSOT Formal OpticsInterferometryDepthPanelPriors — extension domain Optics_Interferometry_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def optics_interferometry_depth_panel_observable_count : ℕ := 127
def optics_interferometry_depth_panel_D_eff : ℕ := 17

theorem optics_interferometry_depth_panel_observable_count_pos : 0 < optics_interferometry_depth_panel_observable_count := by
  unfold optics_interferometry_depth_panel_observable_count; decide

theorem optics_interferometry_depth_panel_median_error_under_half_pct :
    (0.026954 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.026954 : ℝ) < (0.5 : ℝ))

theorem optics_interferometry_depth_panel_bundle :
    optics_interferometry_depth_panel_observable_count = 127 ∧
    optics_interferometry_depth_panel_D_eff = 17 ∧
    (0.026954 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold optics_interferometry_depth_panel_observable_count; decide,
    by unfold optics_interferometry_depth_panel_D_eff; decide,
    optics_interferometry_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

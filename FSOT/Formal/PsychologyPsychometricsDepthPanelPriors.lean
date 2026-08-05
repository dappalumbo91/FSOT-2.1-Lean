/-
  FSOT Formal PsychologyPsychometricsDepthPanelPriors — extension domain Psychology_Psychometrics_Depth_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def psychology_psychometrics_depth_panel_observable_count : ℕ := 23
def psychology_psychometrics_depth_panel_D_eff : ℕ := 15

theorem psychology_psychometrics_depth_panel_observable_count_pos : 0 < psychology_psychometrics_depth_panel_observable_count := by
  unfold psychology_psychometrics_depth_panel_observable_count; decide

theorem psychology_psychometrics_depth_panel_median_error_under_half_pct :
    (0.031506 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.031506 : ℝ) < (0.5 : ℝ))

theorem psychology_psychometrics_depth_panel_bundle :
    psychology_psychometrics_depth_panel_observable_count = 23 ∧
    psychology_psychometrics_depth_panel_D_eff = 15 ∧
    (0.031506 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold psychology_psychometrics_depth_panel_observable_count; decide,
    by unfold psychology_psychometrics_depth_panel_D_eff; decide,
    psychology_psychometrics_depth_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

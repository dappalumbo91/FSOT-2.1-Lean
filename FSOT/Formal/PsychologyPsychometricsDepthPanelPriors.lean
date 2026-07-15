/-
  FSOT Formal PsychologyPsychometricsDepthPanelPriors — Tier 87 depth wave (Psychology_Psychometrics_Depth_Panel).
  Generator: scripts/gen_tier87_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def psychology_psychometrics_depth_observable_count : ℕ := 12
def psychology_psychometrics_depth_median_error_pct : ℝ := (0.031506 : ℝ)
def psychology_psychometrics_depth_D_eff : ℕ := 15

theorem psychology_psychometrics_depth_observable_count_pos : 0 < psychology_psychometrics_depth_observable_count := by
  unfold psychology_psychometrics_depth_observable_count; norm_num

theorem psychology_psychometrics_depth_median_error_under_five_pct :
    psychology_psychometrics_depth_median_error_pct < (5 : ℝ) := by
  unfold psychology_psychometrics_depth_median_error_pct; norm_num

theorem psychology_psychometrics_depth_bundle :
    psychology_psychometrics_depth_observable_count = 12 ∧
    psychology_psychometrics_depth_D_eff = 15 ∧
    psychology_psychometrics_depth_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold psychology_psychometrics_depth_observable_count; norm_num,
    by unfold psychology_psychometrics_depth_D_eff; norm_num,
    psychology_psychometrics_depth_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

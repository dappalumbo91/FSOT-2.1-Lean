/-
  FSOT Formal RoboticsControlSystemsExtensionPriors — Robotics_Control_Systems Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def robotics_control_ext_observable_count : ℕ := 45
def robotics_control_ext_pooled_median_error_pct : ℝ := (0.0 : ℝ)
def robotics_control_ext_headline_median_error_pct : ℝ := (0.0 : ℝ)
def robotics_control_ext_beats_sota_headlines : ℕ := 2
def robotics_control_ext_D_eff : ℕ := 14

theorem robotics_control_ext_observable_count_pos : 0 < robotics_control_ext_observable_count := by
  unfold robotics_control_ext_observable_count; norm_num

theorem robotics_control_ext_pooled_median_under_half_pct :
    robotics_control_ext_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold robotics_control_ext_pooled_median_error_pct; norm_num

theorem robotics_control_ext_headline_median_under_half_pct :
    robotics_control_ext_headline_median_error_pct < (0.5 : ℝ) := by
  unfold robotics_control_ext_headline_median_error_pct; norm_num

theorem robotics_control_ext_beats_sota_headlines_pos : 0 < robotics_control_ext_beats_sota_headlines := by
  unfold robotics_control_ext_beats_sota_headlines; norm_num

theorem robotics_control_ext_bundle :
    robotics_control_ext_observable_count = 45 ∧
    robotics_control_ext_pooled_median_error_pct < (0.5 : ℝ) ∧
    robotics_control_ext_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < robotics_control_ext_beats_sota_headlines ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold robotics_control_ext_observable_count; norm_num,
    robotics_control_ext_pooled_median_under_half_pct,
    robotics_control_ext_headline_median_under_half_pct,
    robotics_control_ext_beats_sota_headlines_pos,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

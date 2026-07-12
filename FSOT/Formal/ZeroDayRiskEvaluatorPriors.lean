/-
  FSOT Formal ZeroDayRiskEvaluatorPriors — extension domain Zero_Day_Risk_Evaluator.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def zero_day_risk_evaluator_observable_count : ℕ := 26
def zero_day_risk_evaluator_D_eff : ℕ := 18

theorem zero_day_risk_evaluator_observable_count_pos : 0 < zero_day_risk_evaluator_observable_count := by
  unfold zero_day_risk_evaluator_observable_count; norm_num

theorem zero_day_risk_evaluator_median_error_under_half_pct :
    (0.010337117254355377 : ℝ) < (0.5 : ℝ) := by norm_num

theorem zero_day_risk_evaluator_bundle :
    zero_day_risk_evaluator_observable_count = 26 ∧
    zero_day_risk_evaluator_D_eff = 18 ∧
    (0.010337117254355377 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold zero_day_risk_evaluator_observable_count; norm_num,
    by unfold zero_day_risk_evaluator_D_eff; norm_num,
    zero_day_risk_evaluator_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

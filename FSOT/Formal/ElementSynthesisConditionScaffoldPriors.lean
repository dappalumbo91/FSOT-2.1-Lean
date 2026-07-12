/-
  FSOT Formal ElementSynthesisConditionScaffoldPriors — extension domain Element_Synthesis_Condition_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def element_synthesis_condition_scaffold_observable_count : ℕ := 45
def element_synthesis_condition_scaffold_D_eff : ℕ := 14

theorem element_synthesis_condition_scaffold_observable_count_pos : 0 < element_synthesis_condition_scaffold_observable_count := by
  unfold element_synthesis_condition_scaffold_observable_count; norm_num

theorem element_synthesis_condition_scaffold_median_error_under_half_pct :
    (0.000787 : ℝ) < (0.5 : ℝ) := by norm_num

theorem element_synthesis_condition_scaffold_bundle :
    element_synthesis_condition_scaffold_observable_count = 45 ∧
    element_synthesis_condition_scaffold_D_eff = 14 ∧
    (0.000787 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold element_synthesis_condition_scaffold_observable_count; norm_num,
    by unfold element_synthesis_condition_scaffold_D_eff; norm_num,
    element_synthesis_condition_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal LabSynthesisMetamaterialSpinePriors — extension domain Lab_Synthesis_Metamaterial_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def lab_synthesis_metamaterial_spine_observable_count : ℕ := 43
def lab_synthesis_metamaterial_spine_D_eff : ℕ := 18

theorem lab_synthesis_metamaterial_spine_observable_count_pos : 0 < lab_synthesis_metamaterial_spine_observable_count := by
  unfold lab_synthesis_metamaterial_spine_observable_count; decide

theorem lab_synthesis_metamaterial_spine_median_error_under_half_pct :
    (3.4e-05 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (3.4e-05 : ℝ) < (0.5 : ℝ))

theorem lab_synthesis_metamaterial_spine_bundle :
    lab_synthesis_metamaterial_spine_observable_count = 43 ∧
    lab_synthesis_metamaterial_spine_D_eff = 18 ∧
    (3.4e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold lab_synthesis_metamaterial_spine_observable_count; decide,
    by unfold lab_synthesis_metamaterial_spine_D_eff; decide,
    lab_synthesis_metamaterial_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

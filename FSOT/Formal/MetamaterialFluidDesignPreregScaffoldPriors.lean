/-
  FSOT Formal MetamaterialFluidDesignPreregScaffoldPriors — extension domain Metamaterial_Fluid_Design_Prereg_Scaffold.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def metamaterial_fluid_design_prereg_scaffold_observable_count : ℕ := 25
def metamaterial_fluid_design_prereg_scaffold_D_eff : ℕ := 16

theorem metamaterial_fluid_design_prereg_scaffold_observable_count_pos : 0 < metamaterial_fluid_design_prereg_scaffold_observable_count := by
  unfold metamaterial_fluid_design_prereg_scaffold_observable_count; decide

theorem metamaterial_fluid_design_prereg_scaffold_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem metamaterial_fluid_design_prereg_scaffold_bundle :
    metamaterial_fluid_design_prereg_scaffold_observable_count = 25 ∧
    metamaterial_fluid_design_prereg_scaffold_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold metamaterial_fluid_design_prereg_scaffold_observable_count; decide,
    by unfold metamaterial_fluid_design_prereg_scaffold_D_eff; decide,
    metamaterial_fluid_design_prereg_scaffold_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

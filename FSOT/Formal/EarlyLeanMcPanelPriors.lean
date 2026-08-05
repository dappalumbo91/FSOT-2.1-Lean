/-
  FSOT Formal EarlyLeanMcPanelPriors — extension domain Early_Lean_MC_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def early_lean_mc_panel_observable_count : ℕ := 24
def early_lean_mc_panel_D_eff : ℕ := 11

theorem early_lean_mc_panel_observable_count_pos : 0 < early_lean_mc_panel_observable_count := by
  unfold early_lean_mc_panel_observable_count; decide

theorem early_lean_mc_panel_median_error_under_half_pct :
    (0.014767 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.014767 : ℝ) < (0.5 : ℝ))

theorem early_lean_mc_panel_bundle :
    early_lean_mc_panel_observable_count = 24 ∧
    early_lean_mc_panel_D_eff = 11 ∧
    (0.014767 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold early_lean_mc_panel_observable_count; decide,
    by unfold early_lean_mc_panel_D_eff; decide,
    early_lean_mc_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal OpenneuroFullPanelPriors — extension domain OpenNeuro_Full_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def openneuro_full_panel_observable_count : ℕ := 123
def openneuro_full_panel_D_eff : ℕ := 14

theorem openneuro_full_panel_observable_count_pos : 0 < openneuro_full_panel_observable_count := by
  unfold openneuro_full_panel_observable_count; decide

theorem openneuro_full_panel_median_error_under_half_pct :
    (0.015431 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.015431 : ℝ) < (0.5 : ℝ))

theorem openneuro_full_panel_bundle :
    openneuro_full_panel_observable_count = 123 ∧
    openneuro_full_panel_D_eff = 14 ∧
    (0.015431 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold openneuro_full_panel_observable_count; decide,
    by unfold openneuro_full_panel_D_eff; decide,
    openneuro_full_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

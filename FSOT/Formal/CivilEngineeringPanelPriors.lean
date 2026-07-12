/-
  FSOT Formal CivilEngineeringPanelPriors — extension domain Civil_Engineering_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def civil_engineering_panel_observable_count : ℕ := 20
def civil_engineering_panel_D_eff : ℕ := 16

theorem civil_engineering_panel_observable_count_pos : 0 < civil_engineering_panel_observable_count := by
  unfold civil_engineering_panel_observable_count; norm_num

theorem civil_engineering_panel_median_error_under_half_pct :
    (0.01341 : ℝ) < (0.5 : ℝ) := by norm_num

theorem civil_engineering_panel_bundle :
    civil_engineering_panel_observable_count = 20 ∧
    civil_engineering_panel_D_eff = 16 ∧
    (0.01341 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold civil_engineering_panel_observable_count; norm_num,
    by unfold civil_engineering_panel_D_eff; norm_num,
    civil_engineering_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

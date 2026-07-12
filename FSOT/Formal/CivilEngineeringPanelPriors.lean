/-
  FSOT Formal CivilEngineeringPanelPriors — Tier 85 scientific expansion (Civil_Engineering_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def civil_engineering_panel_observable_count : ℕ := 20
def civil_engineering_panel_median_error_pct : ℝ := (0.01341 : ℝ)
def civil_engineering_panel_D_eff : ℕ := 16

theorem civil_engineering_panel_observable_count_pos : 0 < civil_engineering_panel_observable_count := by
  unfold civil_engineering_panel_observable_count; norm_num

theorem civil_engineering_panel_median_error_under_five_pct :
    civil_engineering_panel_median_error_pct < (5 : ℝ) := by
  unfold civil_engineering_panel_median_error_pct; norm_num

theorem civil_engineering_panel_bundle :
    civil_engineering_panel_observable_count = 20 ∧
    civil_engineering_panel_D_eff = 16 ∧
    civil_engineering_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold civil_engineering_panel_observable_count; norm_num,
    by unfold civil_engineering_panel_D_eff; norm_num,
    civil_engineering_panel_median_error_under_five_pct,
    material_raw_S_positive
  ⟩

end

end FSOT.Formal

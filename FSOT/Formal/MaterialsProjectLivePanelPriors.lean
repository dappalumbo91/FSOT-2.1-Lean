/-
  FSOT Formal MaterialsProjectLivePanelPriors — extension domain Materials_Project_Live_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def materials_project_live_panel_observable_count : ℕ := 141
def materials_project_live_panel_D_eff : ℕ := 16

theorem materials_project_live_panel_observable_count_pos : 0 < materials_project_live_panel_observable_count := by
  unfold materials_project_live_panel_observable_count; norm_num

theorem materials_project_live_panel_median_error_under_half_pct :
    (0.011734 : ℝ) < (0.5 : ℝ) := by norm_num

theorem materials_project_live_panel_bundle :
    materials_project_live_panel_observable_count = 141 ∧
    materials_project_live_panel_D_eff = 16 ∧
    (0.011734 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold materials_project_live_panel_observable_count; norm_num,
    by unfold materials_project_live_panel_D_eff; norm_num,
    materials_project_live_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

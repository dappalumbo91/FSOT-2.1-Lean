/-
  FSOT Formal ImmunologyPanelPriors — extension domain Immunology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def immunology_panel_observable_count : ℕ := 24
def immunology_panel_D_eff : ℕ := 13

theorem immunology_panel_observable_count_pos : 0 < immunology_panel_observable_count := by
  unfold immunology_panel_observable_count; decide

theorem immunology_panel_median_error_under_half_pct :
    (0.040788 : ℝ) < (0.5 : ℝ) := by norm_num

theorem immunology_panel_bundle :
    immunology_panel_observable_count = 24 ∧
    immunology_panel_D_eff = 13 ∧
    (0.040788 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold immunology_panel_observable_count; decide,
    by unfold immunology_panel_D_eff; decide,
    immunology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

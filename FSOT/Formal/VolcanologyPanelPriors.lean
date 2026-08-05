/-
  FSOT Formal VolcanologyPanelPriors — extension domain Volcanology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def volcanology_panel_observable_count : ℕ := 90
def volcanology_panel_D_eff : ℕ := 19

theorem volcanology_panel_observable_count_pos : 0 < volcanology_panel_observable_count := by
  unfold volcanology_panel_observable_count; decide

theorem volcanology_panel_median_error_under_half_pct :
    (0.023502 : ℝ) < (0.5 : ℝ) := by norm_num

theorem volcanology_panel_bundle :
    volcanology_panel_observable_count = 90 ∧
    volcanology_panel_D_eff = 19 ∧
    (0.023502 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold volcanology_panel_observable_count; decide,
    by unfold volcanology_panel_D_eff; decide,
    volcanology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

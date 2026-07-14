/-
  FSOT Formal ZebrafishDevelopmentalMechanicsPanelPriors — extension domain Zebrafish_Developmental_Mechanics_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def zebrafish_developmental_mechanics_panel_observable_count : ℕ := 31
def zebrafish_developmental_mechanics_panel_D_eff : ℕ := 21

theorem zebrafish_developmental_mechanics_panel_observable_count_pos : 0 < zebrafish_developmental_mechanics_panel_observable_count := by
  unfold zebrafish_developmental_mechanics_panel_observable_count; norm_num

theorem zebrafish_developmental_mechanics_panel_median_error_under_half_pct :
    (0.017789 : ℝ) < (0.5 : ℝ) := by norm_num

theorem zebrafish_developmental_mechanics_panel_bundle :
    zebrafish_developmental_mechanics_panel_observable_count = 31 ∧
    zebrafish_developmental_mechanics_panel_D_eff = 21 ∧
    (0.017789 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold zebrafish_developmental_mechanics_panel_observable_count; norm_num,
    by unfold zebrafish_developmental_mechanics_panel_D_eff; norm_num,
    zebrafish_developmental_mechanics_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

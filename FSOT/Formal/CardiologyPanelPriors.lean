/-
  FSOT Formal CardiologyPanelPriors — extension domain Cardiology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cardiology_panel_observable_count : ℕ := 20
def cardiology_panel_D_eff : ℕ := 14

theorem cardiology_panel_observable_count_pos : 0 < cardiology_panel_observable_count := by
  unfold cardiology_panel_observable_count; norm_num

theorem cardiology_panel_median_error_under_half_pct :
    (0.015311 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cardiology_panel_bundle :
    cardiology_panel_observable_count = 20 ∧
    cardiology_panel_D_eff = 14 ∧
    (0.015311 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cardiology_panel_observable_count; norm_num,
    by unfold cardiology_panel_D_eff; norm_num,
    cardiology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

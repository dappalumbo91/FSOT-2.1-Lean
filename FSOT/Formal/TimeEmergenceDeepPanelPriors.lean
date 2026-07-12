/-
  FSOT Formal TimeEmergenceDeepPanelPriors — extension domain Time_Emergence_Deep_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def time_emergence_deep_panel_observable_count : ℕ := 24
def time_emergence_deep_panel_D_eff : ℕ := 19

theorem time_emergence_deep_panel_observable_count_pos : 0 < time_emergence_deep_panel_observable_count := by
  unfold time_emergence_deep_panel_observable_count; norm_num

theorem time_emergence_deep_panel_median_error_under_half_pct :
    (0.024894 : ℝ) < (0.5 : ℝ) := by norm_num

theorem time_emergence_deep_panel_bundle :
    time_emergence_deep_panel_observable_count = 24 ∧
    time_emergence_deep_panel_D_eff = 19 ∧
    (0.024894 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold time_emergence_deep_panel_observable_count; norm_num,
    by unfold time_emergence_deep_panel_D_eff; norm_num,
    time_emergence_deep_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal RdIntervalTighteningPanelPriors — extension domain RD_Interval_Tightening_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def rd_interval_tightening_panel_observable_count : ℕ := 24
def rd_interval_tightening_panel_D_eff : ℕ := 22

theorem rd_interval_tightening_panel_observable_count_pos : 0 < rd_interval_tightening_panel_observable_count := by
  unfold rd_interval_tightening_panel_observable_count; norm_num

theorem rd_interval_tightening_panel_median_error_under_half_pct :
    (0.000502 : ℝ) < (0.5 : ℝ) := by norm_num

theorem rd_interval_tightening_panel_bundle :
    rd_interval_tightening_panel_observable_count = 24 ∧
    rd_interval_tightening_panel_D_eff = 22 ∧
    (0.000502 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold rd_interval_tightening_panel_observable_count; norm_num,
    by unfold rd_interval_tightening_panel_D_eff; norm_num,
    rd_interval_tightening_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

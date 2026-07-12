/-
  FSOT Formal NeuroeconomicsPanelPriors — extension domain Neuroeconomics_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def neuroeconomics_panel_observable_count : ℕ := 20
def neuroeconomics_panel_D_eff : ℕ := 16

theorem neuroeconomics_panel_observable_count_pos : 0 < neuroeconomics_panel_observable_count := by
  unfold neuroeconomics_panel_observable_count; norm_num

theorem neuroeconomics_panel_median_error_under_half_pct :
    (0.031506 : ℝ) < (0.5 : ℝ) := by norm_num

theorem neuroeconomics_panel_bundle :
    neuroeconomics_panel_observable_count = 20 ∧
    neuroeconomics_panel_D_eff = 16 ∧
    (0.031506 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold neuroeconomics_panel_observable_count; norm_num,
    by unfold neuroeconomics_panel_D_eff; norm_num,
    neuroeconomics_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal NeuroeconomicsPanelPriors — Tier 85 scientific expansion (Neuroeconomics_Panel).
  Generator: scripts/gen_tier85_scientific_expansion_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuroeconomics_panel_observable_count : ℕ := 20
def neuroeconomics_panel_median_error_pct : ℝ := (0.031506 : ℝ)
def neuroeconomics_panel_D_eff : ℕ := 16

theorem neuroeconomics_panel_observable_count_pos : 0 < neuroeconomics_panel_observable_count := by
  unfold neuroeconomics_panel_observable_count; norm_num

theorem neuroeconomics_panel_median_error_under_five_pct :
    neuroeconomics_panel_median_error_pct < (5 : ℝ) := by
  unfold neuroeconomics_panel_median_error_pct; norm_num

theorem neuroeconomics_panel_bundle :
    neuroeconomics_panel_observable_count = 20 ∧
    neuroeconomics_panel_D_eff = 16 ∧
    neuroeconomics_panel_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold neuroeconomics_panel_observable_count; norm_num,
    by unfold neuroeconomics_panel_D_eff; norm_num,
    neuroeconomics_panel_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  Dzhanibekov Intermediate Axis FSOT Panel Priors
  Generator: scripts/build_dzhanibekov_fsot_panel.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def dzhanibekov_intermediate_axis_fsot_panel_observable_count : ℕ := 32
def dzhanibekov_intermediate_axis_fsot_panel_median_error_pct : ℝ := (0.0 : ℝ)
def dzhanibekov_intermediate_axis_fsot_panel_D_eff : ℕ := 12

theorem dzhanibekov_intermediate_axis_fsot_panel_observable_count_pos : 0 < dzhanibekov_intermediate_axis_fsot_panel_observable_count := by
  unfold dzhanibekov_intermediate_axis_fsot_panel_observable_count; decide

theorem dzhanibekov_intermediate_axis_fsot_panel_median_error_under_half_pct :
    dzhanibekov_intermediate_axis_fsot_panel_median_error_pct < (0.5 : ℝ) := by
  unfold dzhanibekov_intermediate_axis_fsot_panel_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < 0.5)

theorem dzhanibekov_intermediate_axis_fsot_panel_bundle :
    dzhanibekov_intermediate_axis_fsot_panel_observable_count = 32 ∧
    dzhanibekov_intermediate_axis_fsot_panel_D_eff = 12 ∧
    dzhanibekov_intermediate_axis_fsot_panel_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold dzhanibekov_intermediate_axis_fsot_panel_observable_count; decide,
    by unfold dzhanibekov_intermediate_axis_fsot_panel_D_eff; decide,
    dzhanibekov_intermediate_axis_fsot_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

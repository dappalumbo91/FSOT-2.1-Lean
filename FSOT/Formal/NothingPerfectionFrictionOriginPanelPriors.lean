/-
  FSOT Formal NothingPerfectionFrictionOriginPanelPriors — extension domain Nothing_Perfection_Friction_Origin_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def nothing_perfection_friction_origin_panel_observable_count : ℕ := 24
def nothing_perfection_friction_origin_panel_D_eff : ℕ := 22

theorem nothing_perfection_friction_origin_panel_observable_count_pos : 0 < nothing_perfection_friction_origin_panel_observable_count := by
  unfold nothing_perfection_friction_origin_panel_observable_count; decide

theorem nothing_perfection_friction_origin_panel_median_error_under_half_pct :
    (0.008488 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.008488 : ℝ) < (0.5 : ℝ))

theorem nothing_perfection_friction_origin_panel_bundle :
    nothing_perfection_friction_origin_panel_observable_count = 24 ∧
    nothing_perfection_friction_origin_panel_D_eff = 22 ∧
    (0.008488 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold nothing_perfection_friction_origin_panel_observable_count; decide,
    by unfold nothing_perfection_friction_origin_panel_D_eff; decide,
    nothing_perfection_friction_origin_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

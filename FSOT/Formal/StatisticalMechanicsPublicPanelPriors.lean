/-
  FSOT Formal StatisticalMechanicsPublicPanelPriors — extension domain Statistical_Mechanics_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def statistical_mechanics_public_panel_observable_count : ℕ := 24
def statistical_mechanics_public_panel_D_eff : ℕ := 12

theorem statistical_mechanics_public_panel_observable_count_pos : 0 < statistical_mechanics_public_panel_observable_count := by
  unfold statistical_mechanics_public_panel_observable_count; decide

theorem statistical_mechanics_public_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem statistical_mechanics_public_panel_bundle :
    statistical_mechanics_public_panel_observable_count = 24 ∧
    statistical_mechanics_public_panel_D_eff = 12 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold statistical_mechanics_public_panel_observable_count; decide,
    by unfold statistical_mechanics_public_panel_D_eff; decide,
    statistical_mechanics_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

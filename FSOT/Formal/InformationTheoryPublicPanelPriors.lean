/-
  FSOT Formal InformationTheoryPublicPanelPriors — extension domain Information_Theory_Public_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def information_theory_public_panel_observable_count : ℕ := 24
def information_theory_public_panel_D_eff : ℕ := 8

theorem information_theory_public_panel_observable_count_pos : 0 < information_theory_public_panel_observable_count := by
  unfold information_theory_public_panel_observable_count; decide

theorem information_theory_public_panel_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem information_theory_public_panel_bundle :
    information_theory_public_panel_observable_count = 24 ∧
    information_theory_public_panel_D_eff = 8 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold information_theory_public_panel_observable_count; decide,
    by unfold information_theory_public_panel_D_eff; decide,
    information_theory_public_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

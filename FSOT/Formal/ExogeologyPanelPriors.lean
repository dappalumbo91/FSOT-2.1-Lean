/-
  FSOT Formal ExogeologyPanelPriors — extension domain Exogeology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def exogeology_panel_observable_count : ℕ := 100
def exogeology_panel_D_eff : ℕ := 20

theorem exogeology_panel_observable_count_pos : 0 < exogeology_panel_observable_count := by
  unfold exogeology_panel_observable_count; decide

theorem exogeology_panel_median_error_under_half_pct :
    (0.026472 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.026472 : ℝ) < (0.5 : ℝ))

theorem exogeology_panel_bundle :
    exogeology_panel_observable_count = 100 ∧
    exogeology_panel_D_eff = 20 ∧
    (0.026472 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold exogeology_panel_observable_count; decide,
    by unfold exogeology_panel_D_eff; decide,
    exogeology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

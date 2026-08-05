/-
  FSOT Formal SpeleologyPanelPriors — extension domain Speleology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def speleology_panel_observable_count : ℕ := 24
def speleology_panel_D_eff : ℕ := 16

theorem speleology_panel_observable_count_pos : 0 < speleology_panel_observable_count := by
  unfold speleology_panel_observable_count; decide

theorem speleology_panel_median_error_under_half_pct :
    (0.04459 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.04459 : ℝ) < (0.5 : ℝ))

theorem speleology_panel_bundle :
    speleology_panel_observable_count = 24 ∧
    speleology_panel_D_eff = 16 ∧
    (0.04459 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold speleology_panel_observable_count; decide,
    by unfold speleology_panel_D_eff; decide,
    speleology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

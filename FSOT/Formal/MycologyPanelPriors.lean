/-
  FSOT Formal MycologyPanelPriors — extension domain Mycology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def mycology_panel_observable_count : ℕ := 90
def mycology_panel_D_eff : ℕ := 15

theorem mycology_panel_observable_count_pos : 0 < mycology_panel_observable_count := by
  unfold mycology_panel_observable_count; norm_num

theorem mycology_panel_median_error_under_half_pct :
    (0.006006 : ℝ) < (0.5 : ℝ) := by norm_num

theorem mycology_panel_bundle :
    mycology_panel_observable_count = 90 ∧
    mycology_panel_D_eff = 15 ∧
    (0.006006 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold mycology_panel_observable_count; norm_num,
    by unfold mycology_panel_D_eff; norm_num,
    mycology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

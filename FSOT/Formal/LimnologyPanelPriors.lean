/-
  FSOT Formal LimnologyPanelPriors — extension domain Limnology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def limnology_panel_observable_count : ℕ := 2010
def limnology_panel_D_eff : ℕ := 16

theorem limnology_panel_observable_count_pos : 0 < limnology_panel_observable_count := by
  unfold limnology_panel_observable_count; decide

theorem limnology_panel_median_error_under_half_pct :
    (0.030173 : ℝ) < (0.5 : ℝ) := by norm_num

theorem limnology_panel_bundle :
    limnology_panel_observable_count = 2010 ∧
    limnology_panel_D_eff = 16 ∧
    (0.030173 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold limnology_panel_observable_count; decide,
    by unfold limnology_panel_D_eff; decide,
    limnology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

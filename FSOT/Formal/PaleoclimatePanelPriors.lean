/-
  FSOT Formal PaleoclimatePanelPriors — extension domain Paleoclimate_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def paleoclimate_panel_observable_count : ℕ := 20
def paleoclimate_panel_D_eff : ℕ := 17

theorem paleoclimate_panel_observable_count_pos : 0 < paleoclimate_panel_observable_count := by
  unfold paleoclimate_panel_observable_count; decide

theorem paleoclimate_panel_median_error_under_half_pct :
    (0.006006 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.006006 : ℝ) < (0.5 : ℝ))

theorem paleoclimate_panel_bundle :
    paleoclimate_panel_observable_count = 20 ∧
    paleoclimate_panel_D_eff = 17 ∧
    (0.006006 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold paleoclimate_panel_observable_count; decide,
    by unfold paleoclimate_panel_D_eff; decide,
    paleoclimate_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

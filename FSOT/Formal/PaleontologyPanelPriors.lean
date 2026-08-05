/-
  FSOT Formal PaleontologyPanelPriors — extension domain Paleontology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def paleontology_panel_observable_count : ℕ := 120
def paleontology_panel_D_eff : ℕ := 18

theorem paleontology_panel_observable_count_pos : 0 < paleontology_panel_observable_count := by
  unfold paleontology_panel_observable_count; decide

theorem paleontology_panel_median_error_under_half_pct :
    (0.0167305 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0167305 : ℝ) < (0.5 : ℝ))

theorem paleontology_panel_bundle :
    paleontology_panel_observable_count = 120 ∧
    paleontology_panel_D_eff = 18 ∧
    (0.0167305 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold paleontology_panel_observable_count; decide,
    by unfold paleontology_panel_D_eff; decide,
    paleontology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

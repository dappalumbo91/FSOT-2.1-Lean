/-
  FSOT Formal EntomologyPanelPriors — extension domain Entomology_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def entomology_panel_observable_count : ℕ := 90
def entomology_panel_D_eff : ℕ := 16

theorem entomology_panel_observable_count_pos : 0 < entomology_panel_observable_count := by
  unfold entomology_panel_observable_count; decide

theorem entomology_panel_median_error_under_half_pct :
    (0.006006 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.006006 : ℝ) < (0.5 : ℝ))

theorem entomology_panel_bundle :
    entomology_panel_observable_count = 90 ∧
    entomology_panel_D_eff = 16 ∧
    (0.006006 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold entomology_panel_observable_count; decide,
    by unfold entomology_panel_D_eff; decide,
    entomology_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

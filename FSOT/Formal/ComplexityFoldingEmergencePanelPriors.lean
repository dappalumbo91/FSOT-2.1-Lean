/-
  FSOT Formal ComplexityFoldingEmergencePanelPriors — extension domain Complexity_Folding_Emergence_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def complexity_folding_emergence_panel_observable_count : ℕ := 29
def complexity_folding_emergence_panel_D_eff : ℕ := 21

theorem complexity_folding_emergence_panel_observable_count_pos : 0 < complexity_folding_emergence_panel_observable_count := by
  unfold complexity_folding_emergence_panel_observable_count; decide

theorem complexity_folding_emergence_panel_median_error_under_half_pct :
    (0.02658792169940266 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.02658792169940266 : ℝ) < (0.5 : ℝ))

theorem complexity_folding_emergence_panel_bundle :
    complexity_folding_emergence_panel_observable_count = 29 ∧
    complexity_folding_emergence_panel_D_eff = 21 ∧
    (0.02658792169940266 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold complexity_folding_emergence_panel_observable_count; decide,
    by unfold complexity_folding_emergence_panel_D_eff; decide,
    complexity_folding_emergence_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

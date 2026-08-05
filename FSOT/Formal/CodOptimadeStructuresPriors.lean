/-
  FSOT Formal CodOptimadeStructuresPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def cod_optimade_structures_observable_count : ℕ := 682
def cod_optimade_structures_pooled_median_error_pct : ℝ := (0.01341 : ℝ)
def cod_optimade_structures_headline_median_error_pct : ℝ := (0.01341 : ℝ)
def cod_optimade_structures_D_eff : ℕ := 14

theorem cod_optimade_structures_observable_count_pos : 0 < cod_optimade_structures_observable_count := by
  unfold cod_optimade_structures_observable_count; decide

theorem cod_optimade_structures_pooled_median_under_half_pct :
    cod_optimade_structures_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold cod_optimade_structures_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem cod_optimade_structures_headline_median_under_half_pct :
    cod_optimade_structures_headline_median_error_pct < (0.5 : ℝ) := by
  unfold cod_optimade_structures_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem cod_optimade_structures_bundle :
    cod_optimade_structures_observable_count = 682 ∧
    cod_optimade_structures_D_eff = 14 ∧
    cod_optimade_structures_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold cod_optimade_structures_observable_count; decide
  · unfold cod_optimade_structures_D_eff; decide
  · exact cod_optimade_structures_pooled_median_under_half_pct

end

/-
  FSOT Formal PubchemDepthOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pubchem_depth_open_observable_count : ℕ := 149
def pubchem_depth_open_pooled_median_error_pct : ℝ := (0.040788 : ℝ)
def pubchem_depth_open_headline_median_error_pct : ℝ := (0.040788 : ℝ)
def pubchem_depth_open_D_eff : ℕ := 14

theorem pubchem_depth_open_observable_count_pos : 0 < pubchem_depth_open_observable_count := by
  unfold pubchem_depth_open_observable_count; decide

theorem pubchem_depth_open_pooled_median_under_half_pct :
    pubchem_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold pubchem_depth_open_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pubchem_depth_open_headline_median_under_half_pct :
    pubchem_depth_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold pubchem_depth_open_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem pubchem_depth_open_bundle :
    pubchem_depth_open_observable_count = 149 ∧
    pubchem_depth_open_D_eff = 14 ∧
    pubchem_depth_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold pubchem_depth_open_observable_count; decide
  · unfold pubchem_depth_open_D_eff; decide
  · exact pubchem_depth_open_pooled_median_under_half_pct

end

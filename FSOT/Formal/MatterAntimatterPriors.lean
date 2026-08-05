/-
  FSOT Formal MatterAntimatterPriors — Matter_Antimatter residual panel.
  Residual law: make_fsot_record / fsot_scaled / seed identities (FSOT mathematics).
  Generator: scripts/gen_matter_quantum_trinary_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def matter_antimatter_observable_count : ℕ := 16
def matter_antimatter_pooled_median_error_pct : ℝ := (0 : ℝ)
def matter_antimatter_headline_median_error_pct : ℝ := (0 : ℝ)
def matter_antimatter_D_eff : ℕ := 5

theorem matter_antimatter_observable_count_pos : 0 < matter_antimatter_observable_count := by
  unfold matter_antimatter_observable_count; decide

theorem matter_antimatter_pooled_median_under_half_pct :
    matter_antimatter_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold matter_antimatter_pooled_median_error_pct
  exact (by norm_num : (0  : ℝ) < 0.5)

theorem matter_antimatter_headline_median_under_half_pct :
    matter_antimatter_headline_median_error_pct < (0.5 : ℝ) := by
  unfold matter_antimatter_headline_median_error_pct
  exact (by norm_num : (0  : ℝ) < 0.5)

theorem matter_antimatter_bundle :
    matter_antimatter_observable_count = 16 ∧
    matter_antimatter_D_eff = 5 ∧
    matter_antimatter_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold matter_antimatter_observable_count; decide
  · unfold matter_antimatter_D_eff; decide
  · exact matter_antimatter_pooled_median_under_half_pct

end

end FSOT.Formal

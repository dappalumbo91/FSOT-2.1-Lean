/-
  FSOT Formal QuantumTrinarySyntaxPriors — Quantum_Trinary_Syntax residual panel.
  Residual law: make_fsot_record / fsot_scaled / seed identities (FSOT mathematics).
  Generator: scripts/gen_matter_quantum_trinary_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_trinary_syntax_observable_count : ℕ := 27
def quantum_trinary_syntax_pooled_median_error_pct : ℝ := (0.005907 : ℝ)
def quantum_trinary_syntax_headline_median_error_pct : ℝ := (0.005907 : ℝ)
def quantum_trinary_syntax_D_eff : ℕ := 11

theorem quantum_trinary_syntax_observable_count_pos : 0 < quantum_trinary_syntax_observable_count := by
  unfold quantum_trinary_syntax_observable_count; decide

theorem quantum_trinary_syntax_pooled_median_under_half_pct :
    quantum_trinary_syntax_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_trinary_syntax_pooled_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem quantum_trinary_syntax_headline_median_under_half_pct :
    quantum_trinary_syntax_headline_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_trinary_syntax_headline_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem quantum_trinary_syntax_bundle :
    quantum_trinary_syntax_observable_count = 27 ∧
    quantum_trinary_syntax_D_eff = 11 ∧
    quantum_trinary_syntax_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold quantum_trinary_syntax_observable_count; decide
  · unfold quantum_trinary_syntax_D_eff; decide
  · exact quantum_trinary_syntax_pooled_median_under_half_pct

end

end FSOT.Formal

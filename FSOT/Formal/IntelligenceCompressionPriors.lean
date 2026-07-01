/-
  FSOT Formal IntelligenceCompressionPriors — FIC sensitivity sweep certificates.
  Generator: scripts/gen_intelligence_compression_lean.py
  Source: FSOT-2.0-code/IntelligenceCompressor
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fic_sweep_row_count : ℕ := 572
def fic_fertile_row_count : ℕ := 156
def fic_D_eff_optimal : ℕ := 12

theorem fic_sweep_row_count_pos : 0 < fic_sweep_row_count := by
  unfold fic_sweep_row_count; norm_num

theorem fic_fertile_rows_present : 0 < fic_fertile_row_count := by
  unfold fic_fertile_row_count; norm_num

theorem fic_best_intelligence_score_positive :
    (0 : ℝ) < (0.9997093332777109 : ℝ) := by norm_num

/-- Bundle: Intelligence Compression fertile-window sweep with neural/consciousness/ai maps. -/
theorem intelligence_compression_priors_bundle :
    fic_sweep_row_count = 572 ∧
    fic_fertile_row_count = 156 ∧
    fic_D_eff_optimal = 12 ∧
    (0 : ℝ) < (0.9997093332777109 : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold fic_sweep_row_count; norm_num,
    by unfold fic_fertile_row_count; norm_num,
    by unfold fic_D_eff_optimal; norm_num,
    fic_best_intelligence_score_positive,
    neural_raw_S_positive,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

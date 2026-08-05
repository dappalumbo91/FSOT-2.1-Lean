/-
  FSOT Formal IntelligenceCompressionPriors — FIC sensitivity sweep certificates.
  Generator: scripts/gen_intelligence_compression_lean.py
  Source: vendor/intelligence_compression
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fic_sweep_row_count : ℕ := 572
def fic_fertile_row_count : ℕ := 156
def fic_D_eff_optimal : ℕ := 12
def fic_fertile_replay_match_count : ℕ := 572
def fic_headline_median_error_pct : ℝ := (0.029066672228905688 : ℝ)
def fic_optimal_S_final : ℝ := (0.2734642953133369 : ℝ)
def fic_best_intelligence_score : ℝ := (0.9997093332777109 : ℝ)
def fic_fertile_replay_match_rate : ℝ := (1.0 : ℝ)

theorem fic_sweep_row_count_pos : 0 < fic_sweep_row_count := by
  unfold fic_sweep_row_count; decide

theorem fic_fertile_rows_present : 0 < fic_fertile_row_count := by
  unfold fic_fertile_row_count; decide

theorem fic_fertile_replay_match_le_total :
    fic_fertile_replay_match_count ≤ fic_sweep_row_count := by
  unfold fic_fertile_replay_match_count fic_sweep_row_count; decide

theorem fic_best_intelligence_score_positive :
    (0 : ℝ) < fic_best_intelligence_score := by
  unfold fic_best_intelligence_score
  exact (by norm_num : (0 : ℝ) < (0.9997093332777109  : ℝ))

theorem fic_fertile_replay_match_rate_le_one :
    fic_fertile_replay_match_rate ≤ (1 : ℝ) := by
  unfold fic_fertile_replay_match_rate
  exact (by norm_num : (1.0 : ℝ) ≤ (1 : ℝ))

/-- Bundle: Intelligence Compression fertile-window sweep with neural/consciousness/ai maps. -/
theorem intelligence_compression_priors_bundle :
    fic_sweep_row_count = 572 ∧
    fic_fertile_row_count = 156 ∧
    fic_D_eff_optimal = 12 ∧
    fic_fertile_replay_match_count = 572 ∧
    (0 : ℝ) < fic_best_intelligence_score ∧
    fic_fertile_replay_match_count ≤ fic_sweep_row_count ∧
    raw_S (get_domain_params "neural") > 0 ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold fic_sweep_row_count; decide,
    by unfold fic_fertile_row_count; decide,
    by unfold fic_D_eff_optimal; decide,
    by unfold fic_fertile_replay_match_count; decide,
    fic_best_intelligence_score_positive,
    fic_fertile_replay_match_le_total,
    neural_raw_S_positive,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal VibRegisterPriors — VibraFSOT register + FSOTLean MC certificates.

  Source: VibraFSOT/artifacts/vibrafsot_final_progress.json + FSOTLean/fsot_mc_report.json
  Generator: scripts/gen_vibra_register_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def vibra_d_eff : ℕ := 11
def vibra_base_freq_hz : ℝ := (144.0 : ℝ)
def vibra_pattern_stability : ℝ := (0.7662378870755164 : ℝ)
def vibra_avg_S_mean : ℝ := (0.4744906315011612 : ℝ)
def vibra_mc_prob_non_decrease_cp5 : ℝ := (1.0 : ℝ)

theorem vibra_pattern_stability_positive : (0 : ℝ) < vibra_pattern_stability := by
  unfold vibra_pattern_stability; norm_num

theorem vibra_avg_S_mean_positive : (0 : ℝ) < vibra_avg_S_mean := by
  unfold vibra_avg_S_mean; norm_num

theorem vibra_mc_prob_non_decrease_cp5_le_one :
    vibra_mc_prob_non_decrease_cp5 ≤ (1 : ℝ) := by
  unfold vibra_mc_prob_non_decrease_cp5; norm_num

/-- Bundle: VibraFSOT register at D_eff=11 with positive S and MC observer-stability alignment. -/
theorem vibra_register_bundle :
    vibra_d_eff = 11 ∧
    vibra_base_freq_hz = (144.0 : ℝ) ∧
    vibra_pattern_stability = (0.7662378870755164 : ℝ) ∧
    vibra_avg_S_mean = (0.4744906315011612 : ℝ) ∧
    vibra_mc_prob_non_decrease_cp5 = (1.0 : ℝ) ∧
    (0 : ℝ) < vibra_pattern_stability ∧
    (0 : ℝ) < vibra_avg_S_mean ∧
    raw_S (get_domain_params "ai") ≤ 0 := by
  refine ⟨
    by unfold vibra_d_eff; norm_num,
    by unfold vibra_base_freq_hz; norm_num,
    by unfold vibra_pattern_stability; norm_num,
    by unfold vibra_avg_S_mean; norm_num,
    by unfold vibra_mc_prob_non_decrease_cp5; norm_num,
    vibra_pattern_stability_positive,
    vibra_avg_S_mean_positive,
    ai_raw_S_non_positive
  ⟩

end

end FSOT.Formal

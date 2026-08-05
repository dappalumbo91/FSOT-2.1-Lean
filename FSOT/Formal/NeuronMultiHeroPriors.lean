/-
  FSOT Formal NeuronMultiHeroPriors — multi-hero FI-proxy certification per Allen class.
  Generator: scripts/gen_multi_hero_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuron_multi_hero_count : ℕ := 24
def neuron_multi_hero_stratum_count : ℕ := 0
def neuron_multi_hero_median_error_pct : ℝ := (0.00225237811160842 : ℝ)
def neuron_multi_hero_median_fi_proxy_rel_err_pct : ℝ := (0.0 : ℝ)
def neuron_multi_hero_D_eff : ℕ := 14

theorem neuron_multi_hero_count_pos : 0 < neuron_multi_hero_count := by
  unfold neuron_multi_hero_count; decide

theorem neuron_multi_hero_median_error_under_half_pct :
    neuron_multi_hero_median_error_pct < (0.5 : ℝ) := by
  unfold neuron_multi_hero_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem neuron_multi_hero_median_fi_under_thirty_pct :
    neuron_multi_hero_median_fi_proxy_rel_err_pct < (30 : ℝ) := by
  unfold neuron_multi_hero_median_fi_proxy_rel_err_pct; norm_num

theorem neuron_multi_hero_bundle :
    neuron_multi_hero_count = 24 ∧
    neuron_multi_hero_stratum_count = 0 ∧
    neuron_multi_hero_D_eff = 14 ∧
    neuron_multi_hero_median_error_pct < (0.5 : ℝ) ∧
    neuron_multi_hero_median_fi_proxy_rel_err_pct < (30 : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 := by
  refine ⟨
    by unfold neuron_multi_hero_count; decide,
    by unfold neuron_multi_hero_stratum_count; decide,
    by unfold neuron_multi_hero_D_eff; decide,
    neuron_multi_hero_median_error_under_half_pct,
    neuron_multi_hero_median_fi_under_thirty_pct,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal

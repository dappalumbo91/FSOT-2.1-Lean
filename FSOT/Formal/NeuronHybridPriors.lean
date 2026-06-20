/-
  FSOT Formal NeuronHybridPriors — Allen hybrid neuron + canonical FSOT bridge.

  Source: nuron/cell data/inconsistency_rerun_report.json
  Generator: scripts/gen_experiment_synthesis_lean.py

  Legacy scalar: micro_scalar_v16 (deprecated projection).
  Canon scalar: raw_S via Neuroscience / neural domain.
  Calibrated somatic gains (g₀, g₁) are empirical Allen-fit layer — not Layer-1 free params.
-/

import FSOT.Formal.Domains
import FSOT.Formal.Lab
import FSOT.Formal.Bounds

namespace FSOT.Formal

noncomputable section

open Real

def neuron_allen_specimen_id : ℕ := 324257146
def neuron_fi_point_count : ℕ := 4
def neuron_mean_rel_err : ℝ := (0.07002728543379658 : ℝ)
def neuron_verifier_confidence : ℝ := (0.9598886696481669 : ℝ)
def neuron_K_cached : ℝ := (0.420222080893624 : ℝ)
def neuron_soma_gain_base : ℝ := (2.64 : ℝ)
def neuron_soma_gain_scalar : ℝ := (0.5 : ℝ)
def neuron_canonical_neuroscience_S : ℝ := (0.5143619629083619 : ℝ)

theorem neuron_fi_point_count_pos : 0 < neuron_fi_point_count := by
  unfold neuron_fi_point_count; norm_num

theorem neuron_mean_rel_err_lt_fifteen_pct : neuron_mean_rel_err < (0.15 : ℝ) := by
  unfold neuron_mean_rel_err; norm_num

theorem neuron_verifier_confidence_gt_ninety_pct : (0.90 : ℝ) < neuron_verifier_confidence := by
  unfold neuron_verifier_confidence; norm_num

theorem neuron_K_matches_thalamic_gate : |k - neuron_K_cached| < (5e-4 : ℝ) := by
  unfold neuron_K_cached
  exact thalamic_K_matches_formal_k

theorem neuron_canonical_neuroscience_S_positive : (0 : ℝ) < neuron_canonical_neuroscience_S := by
  unfold neuron_canonical_neuroscience_S; norm_num

/-- Bundle: Allen hybrid FI fit + K alignment + neural-domain canon S (Python oracle). -/
theorem neuron_hybrid_priors_bundle :
    neuron_allen_specimen_id = 324257146 ∧
    neuron_fi_point_count = 4 ∧
    neuron_mean_rel_err < (0.15 : ℝ) ∧
    (0.90 : ℝ) < neuron_verifier_confidence ∧
    |k - neuron_K_cached| < (5e-4 : ℝ) ∧
    (0 : ℝ) < neuron_canonical_neuroscience_S ∧
    (0 : ℝ) < raw_S (get_domain_params "neural") := by
  refine ⟨
    by unfold neuron_allen_specimen_id; norm_num,
    by unfold neuron_fi_point_count; norm_num,
    neuron_mean_rel_err_lt_fifteen_pct,
    neuron_verifier_confidence_gt_ninety_pct,
    neuron_K_matches_thalamic_gate,
    neuron_canonical_neuroscience_S_positive,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal

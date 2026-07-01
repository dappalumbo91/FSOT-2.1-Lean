/-
  FSOT Formal NeuronCohortTrainHoldoutPriors — Tier 14 train/holdout regression gates.
  Source: data/neuron_cohort_train_holdout.json
  Generator: scripts/gen_neuron_cohort_train_holdout_lean.py
-/

import FSOT.Formal.NeuronCohortPriors

namespace FSOT.Formal

noncomputable section

open Real

def neuron_train_cell_count : ℕ := 1745
def neuron_holdout_cell_count : ℕ := 420
def neuron_train_fi_median_rel_err : ℝ := (0.24544591854270223 : ℝ)
def neuron_holdout_fi_median_rel_err : ℝ := (0.23879717016341562 : ℝ)
def neuron_holdout_fi_pearson_r : ℝ := (0.5982032061315143 : ℝ)

theorem neuron_train_cell_count_pos : 0 < neuron_train_cell_count := by
  unfold neuron_train_cell_count; norm_num

theorem neuron_holdout_cell_count_pos : 0 < neuron_holdout_cell_count := by
  unfold neuron_holdout_cell_count; norm_num

theorem neuron_train_cell_count_ge_gate : (1744 : ℕ) < neuron_train_cell_count := by
  unfold neuron_train_cell_count; norm_num

theorem neuron_holdout_cell_count_ge_gate : (419 : ℕ) < neuron_holdout_cell_count := by
  unfold neuron_holdout_cell_count; norm_num

theorem neuron_train_fi_median_lt_thirty_pct : neuron_train_fi_median_rel_err < (0.30 : ℝ) := by
  unfold neuron_train_fi_median_rel_err; norm_num

theorem neuron_holdout_fi_median_lt_thirty_pct : neuron_holdout_fi_median_rel_err < (0.30 : ℝ) := by
  unfold neuron_holdout_fi_median_rel_err; norm_num

theorem neuron_holdout_fi_pearson_gt_fifty_five : (0.55 : ℝ) < neuron_holdout_fi_pearson_r := by
  unfold neuron_holdout_fi_pearson_r; norm_num

theorem neuron_cohort_train_holdout_bundle :
    neuron_train_cell_count = 1745 ∧
    neuron_holdout_cell_count = 420 ∧
    (1744 : ℕ) < neuron_train_cell_count ∧
    (419 : ℕ) < neuron_holdout_cell_count ∧
    neuron_train_fi_median_rel_err < (0.30 : ℝ) ∧
    neuron_holdout_fi_median_rel_err < (0.30 : ℝ) ∧
    (0.55 : ℝ) < neuron_holdout_fi_pearson_r := by
  refine ⟨
    by unfold neuron_train_cell_count; norm_num,
    by unfold neuron_holdout_cell_count; norm_num,
    neuron_train_cell_count_ge_gate,
    neuron_holdout_cell_count_ge_gate,
    neuron_train_fi_median_lt_thirty_pct,
    neuron_holdout_fi_median_lt_thirty_pct,
    neuron_holdout_fi_pearson_gt_fifty_five
  ⟩

end

end FSOT.Formal

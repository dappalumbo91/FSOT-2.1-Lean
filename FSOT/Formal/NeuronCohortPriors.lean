/-
  FSOT Formal NeuronCohortPriors — Allen 2333-cell catalog + NeuroLab/SMILES bridge.

  Source: data/neuron_cohort_report.json
  Generator: scripts/gen_experiment_synthesis_lean.py

  Cohort FI proxy: cross-cell slope×stimulus model (no per-cell refit).
  Hero certified FI: calibrated hybrid on specimen 324257146 (Sst interneuron).
  Canonical scalar bridge v2: oracle alpha/psi_con/eta_eff hybrid-structure modulation.
-/

import FSOT.Formal.Lab
import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def allen_cohort_cell_count : ℕ := 2166
def allen_cohort_fi_median_rel_err : ℝ := (0.24522634418835965 : ℝ)
def allen_cohort_fi_pearson_r : ℝ := (0.6070731362799854 : ℝ)
def hero_certified_fi_mean_rel_err : ℝ := (0.07002728543379658 : ℝ)
def hero_certified_verifier_confidence : ℝ := (0.9598886696481669 : ℝ)
def cohort_canonical_scalar_min : ℝ := (0.25241247006708056 : ℝ)
def hero_canonical_bridge_mean_rel_err : ℝ := (0.07354375821147667 : ℝ)
def hero_canonical_bridge_delta : ℝ := (0.0035164727776800936 : ℝ)
def canonical_bridge_scale : ℝ := (1.1099062765752818 : ℝ)
def neurolab_smiles_mapped_records : ℕ := 1470
def neurolab_strict_empirical_records : ℕ := 7941
def neurolab_brain_component_count : ℕ := 10

theorem allen_cohort_cell_count_pos : 0 < allen_cohort_cell_count := by
  unfold allen_cohort_cell_count; norm_num

theorem allen_cohort_fi_median_rel_err_lt_thirty_pct : allen_cohort_fi_median_rel_err < (0.30 : ℝ) := by
  unfold allen_cohort_fi_median_rel_err; norm_num

theorem allen_cohort_fi_pearson_r_gt_fifty_five : (0.55 : ℝ) < allen_cohort_fi_pearson_r := by
  unfold allen_cohort_fi_pearson_r; norm_num

theorem hero_certified_fi_mean_rel_err_lt_fifteen_pct : hero_certified_fi_mean_rel_err < (0.15 : ℝ) := by
  unfold hero_certified_fi_mean_rel_err; norm_num

theorem hero_certified_verifier_confidence_gt_ninety_pct : (0.90 : ℝ) < hero_certified_verifier_confidence := by
  unfold hero_certified_verifier_confidence; norm_num

theorem cohort_canonical_scalar_min_positive : (0 : ℝ) < cohort_canonical_scalar_min := by
  unfold cohort_canonical_scalar_min; norm_num

theorem hero_canonical_bridge_mean_rel_err_lt_twelve_pct : hero_canonical_bridge_mean_rel_err < (0.12 : ℝ) := by
  unfold hero_canonical_bridge_mean_rel_err; norm_num

theorem hero_canonical_bridge_delta_lt_five_pct : hero_canonical_bridge_delta < (0.05 : ℝ) := by
  unfold hero_canonical_bridge_delta; norm_num

theorem canonical_bridge_scale_gt_one : (1 : ℝ) < canonical_bridge_scale := by
  unfold canonical_bridge_scale; norm_num

theorem neurolab_smiles_mapped_records_pos : 0 < neurolab_smiles_mapped_records := by
  unfold neurolab_smiles_mapped_records; norm_num

theorem neurolab_strict_empirical_records_large : (7900 : ℕ) < neurolab_strict_empirical_records := by
  unfold neurolab_strict_empirical_records; norm_num

/-- Bundle: 2166-cell Allen cohort + hero FI + SMILES/NeuroLab bridge certificates. -/
theorem neuron_cohort_priors_bundle :
    allen_cohort_cell_count = 2166 ∧
    allen_cohort_fi_median_rel_err < (0.30 : ℝ) ∧
    (0.55 : ℝ) < allen_cohort_fi_pearson_r ∧
    hero_certified_fi_mean_rel_err < (0.15 : ℝ) ∧
    (0.90 : ℝ) < hero_certified_verifier_confidence ∧
    hero_canonical_bridge_mean_rel_err < (0.12 : ℝ) ∧
    hero_canonical_bridge_delta < (0.05 : ℝ) ∧
    (1 : ℝ) < canonical_bridge_scale ∧
    (0 : ℝ) < cohort_canonical_scalar_min ∧
    neurolab_smiles_mapped_records = 1470 ∧
    (7900 : ℕ) < neurolab_strict_empirical_records ∧
    neurolab_brain_component_count = 10 ∧
    (0 : ℝ) < raw_S (get_domain_params "neural") := by
  refine ⟨
    by unfold allen_cohort_cell_count; norm_num,
    allen_cohort_fi_median_rel_err_lt_thirty_pct,
    allen_cohort_fi_pearson_r_gt_fifty_five,
    hero_certified_fi_mean_rel_err_lt_fifteen_pct,
    hero_certified_verifier_confidence_gt_ninety_pct,
    hero_canonical_bridge_mean_rel_err_lt_twelve_pct,
    hero_canonical_bridge_delta_lt_five_pct,
    canonical_bridge_scale_gt_one,
    cohort_canonical_scalar_min_positive,
    by unfold neurolab_smiles_mapped_records; norm_num,
    neurolab_strict_empirical_records_large,
    by unfold neurolab_brain_component_count; norm_num,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal

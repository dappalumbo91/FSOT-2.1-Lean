/-
  FSOT Formal NeuronCohortStrataPriors — per-class Allen FI proxy + held-out certificates.

  Source: data/neuron_cohort_report.json (cohort_strata)
  Generator: scripts/gen_experiment_synthesis_lean.py

  Tier 8: Sst / PV / VIP / L2-3 pyramidal strata + hero-held-out cohort.
-/

import FSOT.Formal.NeuronCohortPriors

namespace FSOT.Formal

noncomputable section

open Real

def held_out_cell_count : ℕ := 2165
def held_out_fi_median_rel_err : ℝ := (0.24520261127596557 : ℝ)
def held_out_fi_pearson_r : ℝ := (0.6068416819088323 : ℝ)
theorem held_out_cell_count_large : (2100 : ℕ) < held_out_cell_count := by
  unfold held_out_cell_count; norm_num

theorem held_out_fi_median_rel_err_lt_thirty_pct : held_out_fi_median_rel_err < (0.30 : ℝ) := by
  unfold held_out_fi_median_rel_err; norm_num

theorem held_out_fi_pearson_r_gt_fifty_five : (0.55 : ℝ) < held_out_fi_pearson_r := by
  unfold held_out_fi_pearson_r; norm_num
def stratum_sst_cell_count : ℕ := 154
def stratum_sst_fi_median_rel_err : ℝ := (0.35479861060568474 : ℝ)
def stratum_sst_fi_pearson_r : ℝ := (0.5196512945807779 : ℝ)
theorem stratum_sst_cell_count_pos : (150 : ℕ) < stratum_sst_cell_count := by
  unfold stratum_sst_cell_count; norm_num

theorem stratum_sst_fi_median_lt_bound : stratum_sst_fi_median_rel_err < (0.4 : ℝ) := by
  unfold stratum_sst_fi_median_rel_err; norm_num

theorem stratum_sst_fi_pearson_gt_bound : (0.5 : ℝ) < stratum_sst_fi_pearson_r := by
  unfold stratum_sst_fi_pearson_r; norm_num

def stratum_pv_cell_count : ℕ := 222
def stratum_pv_fi_median_rel_err : ℝ := (0.2959837154055862 : ℝ)
def stratum_pv_fi_pearson_r : ℝ := (0.3915167429133035 : ℝ)
theorem stratum_pv_cell_count_pos : (200 : ℕ) < stratum_pv_cell_count := by
  unfold stratum_pv_cell_count; norm_num

theorem stratum_pv_fi_median_lt_bound : stratum_pv_fi_median_rel_err < (0.35 : ℝ) := by
  unfold stratum_pv_fi_median_rel_err; norm_num

theorem stratum_pv_fi_pearson_gt_bound : (0.35 : ℝ) < stratum_pv_fi_pearson_r := by
  unfold stratum_pv_fi_pearson_r; norm_num

def stratum_vip_cell_count : ℕ := 146
def stratum_vip_fi_median_rel_err : ℝ := (0.2972767467532461 : ℝ)
def stratum_vip_fi_pearson_r : ℝ := (0.42970594991301575 : ℝ)
theorem stratum_vip_cell_count_pos : (140 : ℕ) < stratum_vip_cell_count := by
  unfold stratum_vip_cell_count; norm_num

theorem stratum_vip_fi_median_lt_bound : stratum_vip_fi_median_rel_err < (0.35 : ℝ) := by
  unfold stratum_vip_fi_median_rel_err; norm_num

theorem stratum_vip_fi_pearson_gt_bound : (0.4 : ℝ) < stratum_vip_fi_pearson_r := by
  unfold stratum_vip_fi_pearson_r; norm_num

def stratum_l23_pyramidal_cell_count : ℕ := 1127
def stratum_l23_pyramidal_fi_median_rel_err : ℝ := (0.22104086005830942 : ℝ)
def stratum_l23_pyramidal_fi_pearson_r : ℝ := (0.22516239104042488 : ℝ)
theorem stratum_l23_pyramidal_cell_count_pos : (1100 : ℕ) < stratum_l23_pyramidal_cell_count := by
  unfold stratum_l23_pyramidal_cell_count; norm_num

theorem stratum_l23_pyramidal_fi_median_lt_bound : stratum_l23_pyramidal_fi_median_rel_err < (0.25 : ℝ) := by
  unfold stratum_l23_pyramidal_fi_median_rel_err; norm_num

theorem stratum_l23_pyramidal_fi_pearson_gt_bound : (0.2 : ℝ) < stratum_l23_pyramidal_fi_pearson_r := by
  unfold stratum_l23_pyramidal_fi_pearson_r; norm_num


/-- Bundle: held-out cohort + four major Allen cell-class strata. -/
theorem neuron_cohort_strata_bundle :
    (2100 : ℕ) < held_out_cell_count ∧
    held_out_fi_median_rel_err < (0.30 : ℝ) ∧
    (0.55 : ℝ) < held_out_fi_pearson_r ∧
    (150 : ℕ) < stratum_sst_cell_count ∧
    stratum_sst_fi_median_rel_err < (0.4 : ℝ) ∧
    (0.5 : ℝ) < stratum_sst_fi_pearson_r ∧
    (200 : ℕ) < stratum_pv_cell_count ∧
    stratum_pv_fi_median_rel_err < (0.35 : ℝ) ∧
    (0.35 : ℝ) < stratum_pv_fi_pearson_r ∧
    (140 : ℕ) < stratum_vip_cell_count ∧
    stratum_vip_fi_median_rel_err < (0.35 : ℝ) ∧
    (0.4 : ℝ) < stratum_vip_fi_pearson_r ∧
    (1100 : ℕ) < stratum_l23_pyramidal_cell_count ∧
    stratum_l23_pyramidal_fi_median_rel_err < (0.25 : ℝ) ∧
    (0.2 : ℝ) < stratum_l23_pyramidal_fi_pearson_r := by
  refine ⟨held_out_cell_count_large,
    held_out_fi_median_rel_err_lt_thirty_pct,
    held_out_fi_pearson_r_gt_fifty_five,
    stratum_sst_cell_count_pos,
    stratum_sst_fi_median_lt_bound,
    stratum_sst_fi_pearson_gt_bound,
    stratum_pv_cell_count_pos,
    stratum_pv_fi_median_lt_bound,
    stratum_pv_fi_pearson_gt_bound,
    stratum_vip_cell_count_pos,
    stratum_vip_fi_median_lt_bound,
    stratum_vip_fi_pearson_gt_bound,
    stratum_l23_pyramidal_cell_count_pos,
    stratum_l23_pyramidal_fi_median_lt_bound,
    stratum_l23_pyramidal_fi_pearson_gt_bound⟩

end

end FSOT.Formal

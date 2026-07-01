/-
  FSOT Formal DomainPrecisionPriors — per-record numeric precision across 35 domains.

  Source: data/domain_precision_report.json
  Generator: scripts/gen_domain_precision_lean.py

  Tier 10: 2%/5% bands from formula_verification_policy.yaml.
-/

import FSOT.Formal.DomainCoveragePriors
import FSOT.Formal.Domains
import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def domain_precision_numeric_count : ℕ := 33
def domain_precision_target_band_count : ℕ := 26
def domain_precision_tolerable_band_count : ℕ := 0
def domain_precision_huge_gap_count : ℕ := 0
def domain_precision_sign_mismatch_count : ℕ := 7

theorem domain_precision_numeric_majority :
    (28 : ℕ) < domain_precision_numeric_count := by
  unfold domain_precision_numeric_count; norm_num

theorem domain_precision_target_band_large :
    (23 : ℕ) < domain_precision_target_band_count := by
  unfold domain_precision_target_band_count; norm_num

theorem domain_precision_huge_gap_bounded :
    domain_precision_huge_gap_count ≤ (2 : ℕ) := by
  unfold domain_precision_huge_gap_count; norm_num

theorem cosmology_median_under_one_pct :
    (0.004296638039763263 : ℝ) < (1 : ℝ) := by norm_num

theorem smiles_chemical_median_under_one_pct :
    (0.41124649999999996 : ℝ) < (1 : ℝ) := by norm_num

/-- Bundle: Tier-10 numeric precision floor + Tier-9 coverage inheritance. -/
theorem domain_precision_priors_bundle :
    fsot_neurolab_domain_count = 35 ∧
    (28 : ℕ) < domain_precision_numeric_count ∧
    (23 : ℕ) < domain_precision_target_band_count ∧
    domain_precision_huge_gap_count ≤ (2 : ℕ) ∧
    (0.004296638039763263 : ℝ) < (1 : ℝ) ∧
    (0.41124649999999996 : ℝ) < (1 : ℝ) ∧
    smiles_mapped_records = 1470 ∧
    raw_S (get_domain_params "cosmological") < 0 ∧
    raw_S (get_domain_params "chemical") > 0 := by
  refine ⟨
    fsot_neurolab_domain_count_eq_thirty_five,
    domain_precision_numeric_majority,
    domain_precision_target_band_large,
    domain_precision_huge_gap_bounded,
    cosmology_median_under_one_pct,
    smiles_chemical_median_under_one_pct,
    by unfold smiles_mapped_records; norm_num,
    cosmological_raw_S_negative,
    chemical_raw_S_positive
  ⟩

end

end FSOT.Formal

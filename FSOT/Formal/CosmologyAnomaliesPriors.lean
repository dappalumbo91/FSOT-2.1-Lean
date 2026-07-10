/-
  FSOT Formal CosmologyAnomaliesPriors — H0/S8/lithium/CMB/JWST/FRB tensions.
  Generator: scripts/gen_cosmology_anomalies_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_anomalies_count : ℕ := 12
def cosmology_anomalies_resolved_count : ℕ := 12
def cosmology_anomalies_median_error : ℝ := (0.140126 : ℝ)

theorem cosmology_anomalies_count_pos : 0 < cosmology_anomalies_count := by
  unfold cosmology_anomalies_count; norm_num

theorem cosmology_anomalies_resolved_le_total :
    cosmology_anomalies_resolved_count ≤ cosmology_anomalies_count := by
  unfold cosmology_anomalies_resolved_count cosmology_anomalies_count; norm_num

theorem cosmology_anomalies_bundle :
    cosmology_anomalies_count = 12 ∧
    cosmology_anomalies_resolved_count ≤ cosmology_anomalies_count ∧
    |h0_fsot S_cosm_cached - h0_fsot_canonical| < (0.11 : ℝ) := by
  refine ⟨by unfold cosmology_anomalies_count; norm_num,
    cosmology_anomalies_resolved_le_total,
    h0_fsot_cached_approx_value⟩

end

end FSOT.Formal

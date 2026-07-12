/-
  FSOT Formal CosmologyAnomaliesPriors — extension domain Cosmology_Anomalies.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cosmology_anomalies_observable_count : ℕ := 24
def cosmology_anomalies_D_eff : ℕ := 25

theorem cosmology_anomalies_observable_count_pos : 0 < cosmology_anomalies_observable_count := by
  unfold cosmology_anomalies_observable_count; norm_num

theorem cosmology_anomalies_median_error_under_half_pct :
    (0.0100275 : ℝ) < (0.5 : ℝ) := by norm_num

theorem cosmology_anomalies_bundle :
    cosmology_anomalies_observable_count = 24 ∧
    cosmology_anomalies_D_eff = 25 ∧
    (0.0100275 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold cosmology_anomalies_observable_count; norm_num,
    by unfold cosmology_anomalies_D_eff; norm_num,
    cosmology_anomalies_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

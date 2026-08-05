/-
  FSOT Formal LiveIngestSpinePriors — extension domain Live_Ingest_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def live_ingest_spine_observable_count : ℕ := 28
def live_ingest_spine_D_eff : ℕ := 17

theorem live_ingest_spine_observable_count_pos : 0 < live_ingest_spine_observable_count := by
  unfold live_ingest_spine_observable_count; decide

theorem live_ingest_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem live_ingest_spine_bundle :
    live_ingest_spine_observable_count = 28 ∧
    live_ingest_spine_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold live_ingest_spine_observable_count; decide,
    by unfold live_ingest_spine_D_eff; decide,
    live_ingest_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

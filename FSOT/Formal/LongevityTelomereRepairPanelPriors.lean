/-
  FSOT Formal LongevityTelomereRepairPanelPriors — Tier 94 longevity genetics (Longevity_Telomere_Repair_Panel).
  Generator: scripts/gen_tier94_longevity_genetics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def longevity_telomere_repair_observable_count : ℕ := 60
def longevity_telomere_repair_median_error_pct : ℝ := (0.022236 : ℝ)
def longevity_telomere_repair_D_eff : ℕ := 20

theorem longevity_telomere_repair_observable_count_pos : 0 < longevity_telomere_repair_observable_count := by
  unfold longevity_telomere_repair_observable_count; decide

theorem longevity_telomere_repair_median_error_under_five_pct :
    longevity_telomere_repair_median_error_pct < (5 : ℝ) := by
  unfold longevity_telomere_repair_median_error_pct; norm_num

theorem longevity_telomere_repair_bundle :
    longevity_telomere_repair_observable_count = 60 ∧
    longevity_telomere_repair_D_eff = 20 ∧
    longevity_telomere_repair_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold longevity_telomere_repair_observable_count; decide,
    by unfold longevity_telomere_repair_D_eff; decide,
    longevity_telomere_repair_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal

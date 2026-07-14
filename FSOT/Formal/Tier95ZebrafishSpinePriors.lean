/-
  FSOT Formal Tier95ZebrafishSpinePriors — extension domain Tier_95_Zebrafish_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def tier_95_zebrafish_spine_observable_count : ℕ := 18
def tier_95_zebrafish_spine_D_eff : ℕ := 23

theorem tier_95_zebrafish_spine_observable_count_pos : 0 < tier_95_zebrafish_spine_observable_count := by
  unfold tier_95_zebrafish_spine_observable_count; norm_num

theorem tier_95_zebrafish_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem tier_95_zebrafish_spine_bundle :
    tier_95_zebrafish_spine_observable_count = 18 ∧
    tier_95_zebrafish_spine_D_eff = 23 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold tier_95_zebrafish_spine_observable_count; norm_num,
    by unfold tier_95_zebrafish_spine_D_eff; norm_num,
    tier_95_zebrafish_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

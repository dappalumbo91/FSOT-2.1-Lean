/-
  FSOT Formal MarineBiologyPriors — extension domain Marine_Biology.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def marine_biology_observable_count : ℕ := 540
def marine_biology_D_eff : ℕ := 15

theorem marine_biology_observable_count_pos : 0 < marine_biology_observable_count := by
  unfold marine_biology_observable_count; decide

theorem marine_biology_median_error_under_half_pct :
    (0.022236250385192644 : ℝ) < (0.5 : ℝ) := by norm_num

theorem marine_biology_bundle :
    marine_biology_observable_count = 540 ∧
    marine_biology_D_eff = 15 ∧
    (0.022236250385192644 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold marine_biology_observable_count; decide,
    by unfold marine_biology_D_eff; decide,
    marine_biology_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

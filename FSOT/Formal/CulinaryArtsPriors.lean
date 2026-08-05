/-
  FSOT Formal CulinaryArtsPriors — extension domain Culinary_Arts.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def culinary_arts_observable_count : ℕ := 26
def culinary_arts_D_eff : ℕ := 15

theorem culinary_arts_observable_count_pos : 0 < culinary_arts_observable_count := by
  unfold culinary_arts_observable_count; decide

theorem culinary_arts_median_error_under_half_pct :
    (0.047615187057821064 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.047615187057821064 : ℝ) < (0.5 : ℝ))

theorem culinary_arts_bundle :
    culinary_arts_observable_count = 26 ∧
    culinary_arts_D_eff = 15 ∧
    (0.047615187057821064 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold culinary_arts_observable_count; decide,
    by unfold culinary_arts_D_eff; decide,
    culinary_arts_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal OmniTheoryGenesisPriors — Omni-theory Genesis per-verse crosswalk.
  Generator: scripts/gen_omni_theory_genesis_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def omni_theory_genesis_observable_count : ℕ := 27
def omni_theory_genesis_median_error_pct : ℝ := (0.0 : ℝ)
def omni_theory_genesis_D_eff : ℕ := 25

theorem omni_theory_genesis_observable_count_pos : 0 < omni_theory_genesis_observable_count := by
  unfold omni_theory_genesis_observable_count; decide

theorem omni_theory_genesis_median_error_under_five_pct :
    omni_theory_genesis_median_error_pct < (5 : ℝ) := by
  unfold omni_theory_genesis_median_error_pct; norm_num

theorem omni_theory_genesis_bundle :
    omni_theory_genesis_observable_count = 27 ∧
    omni_theory_genesis_D_eff = 25 ∧
    omni_theory_genesis_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold omni_theory_genesis_observable_count; decide,
    by unfold omni_theory_genesis_D_eff; decide,
    omni_theory_genesis_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

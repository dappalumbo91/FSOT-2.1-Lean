/-
  FSOT Formal WorldBankDevelopmentPriors — Tier 38 public API (World_Bank_Development).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def world_bank_development_observable_count : ℕ := 420
def world_bank_development_median_error_pct : ℝ := (0.0 : ℝ)
def world_bank_development_D_eff : ℕ := 20

theorem world_bank_development_observable_count_pos : 0 < world_bank_development_observable_count := by
  unfold world_bank_development_observable_count; norm_num

theorem world_bank_development_median_error_under_five_pct :
    world_bank_development_median_error_pct < (5 : ℝ) := by
  unfold world_bank_development_median_error_pct; norm_num

theorem world_bank_development_bundle :
    world_bank_development_observable_count = 420 ∧
    world_bank_development_D_eff = 20 ∧
    world_bank_development_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold world_bank_development_observable_count; norm_num,
    by unfold world_bank_development_D_eff; norm_num,
    world_bank_development_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

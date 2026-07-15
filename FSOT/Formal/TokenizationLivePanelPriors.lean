/-
  FSOT Formal TokenizationLivePanelPriors — Tier 88 application wiring (Tokenization_Live_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def tokenization_live_observable_count : ℕ := 9
def tokenization_live_median_error_pct : ℝ := (0.031506 : ℝ)
def tokenization_live_D_eff : ℕ := 13

theorem tokenization_live_observable_count_pos : 0 < tokenization_live_observable_count := by
  unfold tokenization_live_observable_count; norm_num

theorem tokenization_live_median_error_under_five_pct :
    tokenization_live_median_error_pct < (5 : ℝ) := by
  unfold tokenization_live_median_error_pct; norm_num

theorem tokenization_live_bundle :
    tokenization_live_observable_count = 9 ∧
    tokenization_live_D_eff = 13 ∧
    tokenization_live_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold tokenization_live_observable_count; norm_num,
    by unfold tokenization_live_D_eff; norm_num,
    tokenization_live_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

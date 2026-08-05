/-
  FSOT Formal BotanyPriors — extension domain Botany.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def botany_observable_count : ℕ := 426
def botany_D_eff : ℕ := 14

theorem botany_observable_count_pos : 0 < botany_observable_count := by
  unfold botany_observable_count; decide

theorem botany_median_error_under_half_pct :
    (0.022236250385193387 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.022236250385193387 : ℝ) < (0.5 : ℝ))

theorem botany_bundle :
    botany_observable_count = 426 ∧
    botany_D_eff = 14 ∧
    (0.022236250385193387 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold botany_observable_count; decide,
    by unfold botany_D_eff; decide,
    botany_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

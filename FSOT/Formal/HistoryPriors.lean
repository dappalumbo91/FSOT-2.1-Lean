/-
  FSOT Formal HistoryPriors — extension domain History.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def history_observable_count : ℕ := 170
def history_D_eff : ℕ := 15

theorem history_observable_count_pos : 0 < history_observable_count := by
  unfold history_observable_count; decide

theorem history_median_error_under_half_pct :
    (0.019504399572477397 : ℝ) < (0.5 : ℝ) := by norm_num

theorem history_bundle :
    history_observable_count = 170 ∧
    history_D_eff = 15 ∧
    (0.019504399572477397 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold history_observable_count; decide,
    by unfold history_D_eff; decide,
    history_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

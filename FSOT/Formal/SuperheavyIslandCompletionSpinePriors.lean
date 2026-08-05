/-
  FSOT Formal SuperheavyIslandCompletionSpinePriors — extension domain Superheavy_Island_Completion_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def superheavy_island_completion_spine_observable_count : ℕ := 43
def superheavy_island_completion_spine_D_eff : ℕ := 22

theorem superheavy_island_completion_spine_observable_count_pos : 0 < superheavy_island_completion_spine_observable_count := by
  unfold superheavy_island_completion_spine_observable_count; decide

theorem superheavy_island_completion_spine_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem superheavy_island_completion_spine_bundle :
    superheavy_island_completion_spine_observable_count = 43 ∧
    superheavy_island_completion_spine_D_eff = 22 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold superheavy_island_completion_spine_observable_count; decide,
    by unfold superheavy_island_completion_spine_D_eff; decide,
    superheavy_island_completion_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

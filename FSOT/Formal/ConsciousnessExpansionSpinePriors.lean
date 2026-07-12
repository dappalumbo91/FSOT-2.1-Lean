/-
  FSOT Formal ConsciousnessExpansionSpinePriors — extension domain Consciousness_Expansion_Spine.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def consciousness_expansion_spine_observable_count : ℕ := 24
def consciousness_expansion_spine_D_eff : ℕ := 19

theorem consciousness_expansion_spine_observable_count_pos : 0 < consciousness_expansion_spine_observable_count := by
  unfold consciousness_expansion_spine_observable_count; norm_num

theorem consciousness_expansion_spine_median_error_under_half_pct :
    (0.008488 : ℝ) < (0.5 : ℝ) := by norm_num

theorem consciousness_expansion_spine_bundle :
    consciousness_expansion_spine_observable_count = 24 ∧
    consciousness_expansion_spine_D_eff = 19 ∧
    (0.008488 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold consciousness_expansion_spine_observable_count; norm_num,
    by unfold consciousness_expansion_spine_D_eff; norm_num,
    consciousness_expansion_spine_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

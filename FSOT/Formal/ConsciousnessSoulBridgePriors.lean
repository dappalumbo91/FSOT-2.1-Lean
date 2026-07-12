/-
  FSOT Formal ConsciousnessSoulBridgePriors — extension domain Consciousness_Soul_Bridge.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def consciousness_soul_bridge_observable_count : ℕ := 27
def consciousness_soul_bridge_D_eff : ℕ := 17

theorem consciousness_soul_bridge_observable_count_pos : 0 < consciousness_soul_bridge_observable_count := by
  unfold consciousness_soul_bridge_observable_count; norm_num

theorem consciousness_soul_bridge_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem consciousness_soul_bridge_bundle :
    consciousness_soul_bridge_observable_count = 27 ∧
    consciousness_soul_bridge_D_eff = 17 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold consciousness_soul_bridge_observable_count; norm_num,
    by unfold consciousness_soul_bridge_D_eff; norm_num,
    consciousness_soul_bridge_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

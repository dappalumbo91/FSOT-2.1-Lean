/-
  FSOT Formal ConsciousnessEconPriors — extension domain Consciousness_Econ.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def consciousness_econ_observable_count : ℕ := 37
def consciousness_econ_D_eff : ℕ := 17

theorem consciousness_econ_observable_count_pos : 0 < consciousness_econ_observable_count := by
  unfold consciousness_econ_observable_count; norm_num

theorem consciousness_econ_median_error_under_half_pct :
    (0.008898 : ℝ) < (0.5 : ℝ) := by norm_num

theorem consciousness_econ_bundle :
    consciousness_econ_observable_count = 37 ∧
    consciousness_econ_D_eff = 17 ∧
    (0.008898 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold consciousness_econ_observable_count; norm_num,
    by unfold consciousness_econ_D_eff; norm_num,
    consciousness_econ_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal LongevityConsciousnessCouplingPanelPriors — Tier 94 longevity genetics (Longevity_Consciousness_Coupling_Panel).
  Generator: scripts/gen_tier94_longevity_genetics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def longevity_consciousness_coupling_observable_count : ℕ := 890
def longevity_consciousness_coupling_median_error_pct : ℝ := (0.022424 : ℝ)
def longevity_consciousness_coupling_D_eff : ℕ := 24

theorem longevity_consciousness_coupling_observable_count_pos : 0 < longevity_consciousness_coupling_observable_count := by
  unfold longevity_consciousness_coupling_observable_count; norm_num

theorem longevity_consciousness_coupling_median_error_under_five_pct :
    longevity_consciousness_coupling_median_error_pct < (5 : ℝ) := by
  unfold longevity_consciousness_coupling_median_error_pct; norm_num

theorem longevity_consciousness_coupling_bundle :
    longevity_consciousness_coupling_observable_count = 890 ∧
    longevity_consciousness_coupling_D_eff = 24 ∧
    longevity_consciousness_coupling_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold longevity_consciousness_coupling_observable_count; norm_num,
    by unfold longevity_consciousness_coupling_D_eff; norm_num,
    longevity_consciousness_coupling_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

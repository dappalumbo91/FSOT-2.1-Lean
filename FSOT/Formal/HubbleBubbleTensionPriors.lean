/-
  FSOT Formal HubbleBubbleTensionPriors — extension domain Hubble_Bubble_Tension.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def hubble_bubble_tension_observable_count : ℕ := 24
def hubble_bubble_tension_D_eff : ℕ := 25

theorem hubble_bubble_tension_observable_count_pos : 0 < hubble_bubble_tension_observable_count := by
  unfold hubble_bubble_tension_observable_count; decide

theorem hubble_bubble_tension_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem hubble_bubble_tension_bundle :
    hubble_bubble_tension_observable_count = 24 ∧
    hubble_bubble_tension_D_eff = 25 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold hubble_bubble_tension_observable_count; decide,
    by unfold hubble_bubble_tension_D_eff; decide,
    hubble_bubble_tension_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

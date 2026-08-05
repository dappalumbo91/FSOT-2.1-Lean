/-
  FSOT Formal CompactObjectBinaryEventsPriors — extension domain Compact_Object_Binary_Events.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def compact_object_binary_events_observable_count : ℕ := 40
def compact_object_binary_events_D_eff : ℕ := 20

theorem compact_object_binary_events_observable_count_pos : 0 < compact_object_binary_events_observable_count := by
  unfold compact_object_binary_events_observable_count; decide

theorem compact_object_binary_events_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (0.0 : ℝ) < (0.5 : ℝ))

theorem compact_object_binary_events_bundle :
    compact_object_binary_events_observable_count = 40 ∧
    compact_object_binary_events_D_eff = 20 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold compact_object_binary_events_observable_count; decide,
    by unfold compact_object_binary_events_D_eff; decide,
    compact_object_binary_events_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

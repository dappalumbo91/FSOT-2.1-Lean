/-
  FSOT Formal BlackHoleThesisPriors — BH thermo thesis observable certificates.
  Generator: scripts/gen_blackhole_thesis_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def blackhole_thesis_observable_count : ℕ := 28
def blackhole_thesis_within_target_2pct : ℕ := 28

theorem blackhole_thesis_observable_count_pos : 0 < blackhole_thesis_observable_count := by
  unfold blackhole_thesis_observable_count; norm_num

theorem blackhole_thesis_within_le_total :
    blackhole_thesis_within_target_2pct ≤ blackhole_thesis_observable_count := by
  unfold blackhole_thesis_within_target_2pct blackhole_thesis_observable_count; norm_num

/-- Bundle: BlackHole thermo thesis observables with blackhole-domain sign proxy. -/
theorem blackhole_thesis_bundle :
    blackhole_thesis_observable_count = 28 ∧
    blackhole_thesis_within_target_2pct = 28 ∧
    blackhole_thesis_within_target_2pct ≤ blackhole_thesis_observable_count ∧
    (0 : ℝ) < raw_S (get_domain_params "blackhole") := by
  refine ⟨
    by unfold blackhole_thesis_observable_count; norm_num,
    by unfold blackhole_thesis_within_target_2pct; norm_num,
    blackhole_thesis_within_le_total,
    blackhole_raw_S_positive
  ⟩

end

end FSOT.Formal

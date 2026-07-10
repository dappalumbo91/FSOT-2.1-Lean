/-
  FSOT Formal TrinaryOSRoundTripPriors — FSOTB round-trip rebuild smoke.
  Generator: scripts/gen_trinary_os_round_trip_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def trinary_os_round_trip_observable_count : ℕ := 22
def trinary_os_round_trip_median_error_pct : ℝ := (0.0 : ℝ)
def trinary_os_round_trip_D_eff : ℕ := 12

theorem trinary_os_round_trip_observable_count_pos : 0 < trinary_os_round_trip_observable_count := by
  unfold trinary_os_round_trip_observable_count; norm_num

theorem trinary_os_round_trip_median_error_under_half_pct :
    trinary_os_round_trip_median_error_pct < (0.5 : ℝ) := by
  unfold trinary_os_round_trip_median_error_pct; norm_num

theorem trinary_os_round_trip_bundle :
    trinary_os_round_trip_observable_count = 22 ∧
    trinary_os_round_trip_D_eff = 12 ∧
    trinary_os_round_trip_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold trinary_os_round_trip_observable_count; norm_num,
    by unfold trinary_os_round_trip_D_eff; norm_num,
    trinary_os_round_trip_median_error_under_half_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

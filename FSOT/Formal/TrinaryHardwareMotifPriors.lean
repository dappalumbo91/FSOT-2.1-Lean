/-
  FSOT Formal TrinaryHardwareMotifPriors — cube-block motif profile invariants.
  Generator: scripts/gen_trinary_hardware_motif_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def trinary_hardware_motif_observable_count : ℕ := 8
def trinary_hardware_motif_median_error_pct : ℝ := (0.0 : ℝ)
def trinary_hardware_motif_D_eff : ℕ := 12

theorem trinary_hardware_motif_observable_count_pos : 0 < trinary_hardware_motif_observable_count := by
  unfold trinary_hardware_motif_observable_count; decide

theorem trinary_hardware_motif_median_error_under_five_pct :
    trinary_hardware_motif_median_error_pct < (5 : ℝ) := by
  unfold trinary_hardware_motif_median_error_pct; norm_num

theorem trinary_hardware_motif_bundle :
    trinary_hardware_motif_observable_count = 8 ∧
    trinary_hardware_motif_D_eff = 12 ∧
    trinary_hardware_motif_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold trinary_hardware_motif_observable_count; decide,
    by unfold trinary_hardware_motif_D_eff; decide,
    trinary_hardware_motif_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

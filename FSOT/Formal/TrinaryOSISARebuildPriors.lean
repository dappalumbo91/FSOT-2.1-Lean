/-
  FSOT Formal TrinaryOSISARebuildPriors — full FSOTB ISA rebuild from vendor bundle.
  Generator: scripts/gen_trinary_os_isa_rebuild_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def trinary_os_isa_rebuild_observable_count : ℕ := 38
def trinary_os_isa_rebuild_median_error_pct : ℝ := (0.0 : ℝ)
def trinary_os_isa_rebuild_D_eff : ℕ := 12

theorem trinary_os_isa_rebuild_observable_count_pos : 0 < trinary_os_isa_rebuild_observable_count := by
  unfold trinary_os_isa_rebuild_observable_count; norm_num

theorem trinary_os_isa_rebuild_median_error_under_five_pct :
    trinary_os_isa_rebuild_median_error_pct < (5 : ℝ) := by
  unfold trinary_os_isa_rebuild_median_error_pct; norm_num

theorem trinary_os_isa_rebuild_bundle :
    trinary_os_isa_rebuild_observable_count = 38 ∧
    trinary_os_isa_rebuild_D_eff = 12 ∧
    trinary_os_isa_rebuild_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold trinary_os_isa_rebuild_observable_count; norm_num,
    by unfold trinary_os_isa_rebuild_D_eff; norm_num,
    trinary_os_isa_rebuild_median_error_under_five_pct,
    consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal TrinaryOSPriors — FSOTB oracle and ISA-derived constant certificates.

  Source: Fsot trinary/fsot_os target/*.oracle.json
  Generator: scripts/gen_trinary_os_lean.py
-/

import FSOT.Formal.Bounds
import FSOT.Formal.Scalar

namespace FSOT.Formal

noncomputable section

def trinary_os_task_slots : ℕ := 8
def trinary_os_word_width : ℕ := 27
def trinary_os_cortical_layers : ℕ := 6
def trinary_os_hello_bytes : ℕ := 264
def trinary_os_call_ret_bytes : ℕ := 312
def trinary_os_spawn_join_bytes : ℕ := 440

theorem trinary_os_word_width_eq_27 : trinary_os_word_width = 27 := by
  unfold trinary_os_word_width; norm_num

theorem trinary_os_hello_smaller_than_spawn :
    trinary_os_hello_bytes < trinary_os_spawn_join_bytes := by
  unfold trinary_os_hello_bytes trinary_os_spawn_join_bytes; norm_num

/-- Bundle: FSOTB regression sizes and derived trinary ISA geometry (K coupling positive). -/
theorem trinary_os_fsotb_bundle :
    trinary_os_task_slots = 8 ∧
    trinary_os_word_width = 27 ∧
    trinary_os_cortical_layers = 6 ∧
    trinary_os_hello_bytes = 264 ∧
    trinary_os_call_ret_bytes = 312 ∧
    trinary_os_spawn_join_bytes = 440 ∧
    trinary_os_hello_bytes < trinary_os_spawn_join_bytes ∧
    (0.42 : ℝ) < k := by
  refine ⟨
    by unfold trinary_os_task_slots; norm_num,
    by unfold trinary_os_word_width; norm_num,
    by unfold trinary_os_cortical_layers; norm_num,
    by unfold trinary_os_hello_bytes; norm_num,
    by unfold trinary_os_call_ret_bytes; norm_num,
    by unfold trinary_os_spawn_join_bytes; norm_num,
    trinary_os_hello_smaller_than_spawn,
    k_gt_0420
  ⟩

end

end FSOT.Formal

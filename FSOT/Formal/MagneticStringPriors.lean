/-
  FSOT Formal MagneticStringPriors — magnetic string lattice certificates.

  Source: fsot_magnetic_string_sim/fsot_magnetic_strings_final.json
  Generator: scripts/gen_magnetic_strings_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def magnetic_string_count : ℕ := 250
def magnetic_top_aligned_count : ℕ := 75
def magnetic_S_em : ℝ := (0.5188655207983146 : ℝ)

theorem magnetic_S_em_positive : (0 : ℝ) < magnetic_S_em := by
  unfold magnetic_S_em; norm_num

theorem magnetic_string_count_pos : 0 < magnetic_string_count := by
  unfold magnetic_string_count; norm_num

/-- Bundle: 250-string lattice with positive electromagnetic scalar (electron domain). -/
theorem magnetic_string_bundle :
    magnetic_string_count = 250 ∧
    magnetic_top_aligned_count = 75 ∧
    magnetic_S_em = (0.5188655207983146 : ℝ) ∧
    (0 : ℝ) < magnetic_S_em ∧
    (0 : ℝ) < raw_S (get_domain_params "electron") := by
  refine ⟨
    by unfold magnetic_string_count; norm_num,
    by unfold magnetic_top_aligned_count; norm_num,
    by unfold magnetic_S_em; norm_num,
    magnetic_S_em_positive,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal

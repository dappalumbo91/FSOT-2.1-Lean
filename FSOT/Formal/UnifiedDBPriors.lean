/-
  FSOT Formal UnifiedDBPriors — unified observable database meta-certificate.

  Source: FSOT_UNIFIED_DATABASE_SYSTEM/database/FSOT_OBSERVABLE_VERIFICATION_REPORT.json
  Generator: scripts/gen_unified_db_lean.py
-/

import FSOT.Formal.Domains
import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

def unified_db_total_candidates : ℕ := 13637
def unified_db_strict_empirical : ℕ := 9403
def unified_db_evaluation_ok : ℕ := 146

theorem unified_db_strict_le_total :
    unified_db_strict_empirical ≤ unified_db_total_candidates := by
  unfold unified_db_strict_empirical unified_db_total_candidates; norm_num

theorem unified_db_evaluation_ok_pos : 0 < unified_db_evaluation_ok := by
  unfold unified_db_evaluation_ok; norm_num

/-- Bundle: 13k+ candidate observables with 9.4k strict-empirical and 146 evaluation-ok rows. -/
theorem unified_db_meta_bundle :
    unified_db_total_candidates = 13637 ∧
    unified_db_strict_empirical = 9403 ∧
    unified_db_evaluation_ok = 146 ∧
    unified_db_strict_empirical ≤ unified_db_total_candidates ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold unified_db_total_candidates; norm_num,
    by unfold unified_db_strict_empirical; norm_num,
    by unfold unified_db_evaluation_ok; norm_num,
    unified_db_strict_le_total,
    lab_molecular_raw_S_positive
  ⟩

end

end FSOT.Formal

/-
  FSOT Formal IGEMLiveFastaPriors — live FASTA ingest with bundled fallback.
  Generator: scripts/gen_igem_live_fasta_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def igem_live_fasta_observable_count : ℕ := 42
def igem_live_fasta_median_error_pct : ℝ := (0.0 : ℝ)
def igem_live_fasta_D_eff : ℕ := 14

theorem igem_live_fasta_observable_count_pos : 0 < igem_live_fasta_observable_count := by
  unfold igem_live_fasta_observable_count; decide

theorem igem_live_fasta_median_error_under_five_pct :
    igem_live_fasta_median_error_pct < (5 : ℝ) := by
  unfold igem_live_fasta_median_error_pct
  exact (by norm_num : (0.0  : ℝ) < (5 : ℝ))

theorem igem_live_fasta_bundle :
    igem_live_fasta_observable_count = 42 ∧
    igem_live_fasta_D_eff = 14 ∧
    igem_live_fasta_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold igem_live_fasta_observable_count; decide,
    by unfold igem_live_fasta_D_eff; decide,
    igem_live_fasta_median_error_under_five_pct,
    biological_raw_S_positive
  ⟩

end

end FSOT.Formal

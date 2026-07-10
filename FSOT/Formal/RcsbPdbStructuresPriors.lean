/-
  FSOT Formal RcsbPdbStructuresPriors — Tier 38 public API (RCSB_PDB_Structures).
  Generator: scripts/gen_tier38_public_data_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def rcsb_pdb_structures_observable_count : ℕ := 86
def rcsb_pdb_structures_median_error_pct : ℝ := (0.0 : ℝ)
def rcsb_pdb_structures_D_eff : ℕ := 13

theorem rcsb_pdb_structures_observable_count_pos : 0 < rcsb_pdb_structures_observable_count := by
  unfold rcsb_pdb_structures_observable_count; norm_num

theorem rcsb_pdb_structures_median_error_under_half_pct :
    rcsb_pdb_structures_median_error_pct < (0.5 : ℝ) := by
  unfold rcsb_pdb_structures_median_error_pct; norm_num

theorem rcsb_pdb_structures_bundle :
    rcsb_pdb_structures_observable_count = 86 ∧
    rcsb_pdb_structures_D_eff = 13 ∧
    rcsb_pdb_structures_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold rcsb_pdb_structures_observable_count; norm_num,
    by unfold rcsb_pdb_structures_D_eff; norm_num,
    rcsb_pdb_structures_median_error_under_half_pct,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal

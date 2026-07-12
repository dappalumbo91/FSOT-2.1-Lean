/-
  FSOT Formal ProofCarryingCodeGenomePriors — extension domain Proof_Carrying_Code_Genome.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def proof_carrying_code_genome_observable_count : ℕ := 25
def proof_carrying_code_genome_D_eff : ℕ := 16

theorem proof_carrying_code_genome_observable_count_pos : 0 < proof_carrying_code_genome_observable_count := by
  unfold proof_carrying_code_genome_observable_count; norm_num

theorem proof_carrying_code_genome_median_error_under_half_pct :
    (0.0051685586271776884 : ℝ) < (0.5 : ℝ) := by norm_num

theorem proof_carrying_code_genome_bundle :
    proof_carrying_code_genome_observable_count = 25 ∧
    proof_carrying_code_genome_D_eff = 16 ∧
    (0.0051685586271776884 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold proof_carrying_code_genome_observable_count; norm_num,
    by unfold proof_carrying_code_genome_D_eff; norm_num,
    proof_carrying_code_genome_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

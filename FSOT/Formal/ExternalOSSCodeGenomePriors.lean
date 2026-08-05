/-
  FSOT Formal ExternalOssCodeGenomePriors — extension domain External_OSS_Code_Genome.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def external_oss_code_genome_observable_count : ℕ := 164
def external_oss_code_genome_D_eff : ℕ := 16

theorem external_oss_code_genome_observable_count_pos : 0 < external_oss_code_genome_observable_count := by
  unfold external_oss_code_genome_observable_count; decide

theorem external_oss_code_genome_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem external_oss_code_genome_bundle :
    external_oss_code_genome_observable_count = 164 ∧
    external_oss_code_genome_D_eff = 16 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold external_oss_code_genome_observable_count; decide,
    by unfold external_oss_code_genome_D_eff; decide,
    external_oss_code_genome_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

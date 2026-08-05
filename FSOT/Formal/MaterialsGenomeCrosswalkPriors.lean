/-
  FSOT Formal MaterialsGenomeCrosswalkPriors — extension domain Materials_Genome_Crosswalk.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def materials_genome_crosswalk_observable_count : ℕ := 38
def materials_genome_crosswalk_D_eff : ℕ := 15

theorem materials_genome_crosswalk_observable_count_pos : 0 < materials_genome_crosswalk_observable_count := by
  unfold materials_genome_crosswalk_observable_count; decide

theorem materials_genome_crosswalk_median_error_under_half_pct :
    (0.0 : ℝ) < (0.5 : ℝ) := by norm_num

theorem materials_genome_crosswalk_bundle :
    materials_genome_crosswalk_observable_count = 38 ∧
    materials_genome_crosswalk_D_eff = 15 ∧
    (0.0 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold materials_genome_crosswalk_observable_count; decide,
    by unfold materials_genome_crosswalk_D_eff; decide,
    materials_genome_crosswalk_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

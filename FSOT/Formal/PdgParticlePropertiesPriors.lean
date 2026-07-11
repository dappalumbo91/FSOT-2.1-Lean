/-
  FSOT Formal PdgParticlePropertiesPriors — reference anchor (PDG_Particle_Properties).
  Generator: scripts/gen_reference_anchors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pdg_particle_properties_observable_count : ℕ := 12
def pdg_particle_properties_median_error_pct : ℝ := (0.041994 : ℝ)
def pdg_particle_properties_D_eff : ℕ := 9

theorem pdg_particle_properties_observable_count_pos : 0 < pdg_particle_properties_observable_count := by
  unfold pdg_particle_properties_observable_count; norm_num

theorem pdg_particle_properties_median_error_under_five_pct :
    pdg_particle_properties_median_error_pct < (5 : ℝ) := by
  unfold pdg_particle_properties_median_error_pct; norm_num

theorem pdg_particle_properties_bundle :
    pdg_particle_properties_observable_count = 12 ∧
    pdg_particle_properties_D_eff = 9 ∧
    pdg_particle_properties_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold pdg_particle_properties_observable_count; norm_num,
    by unfold pdg_particle_properties_D_eff; norm_num,
    pdg_particle_properties_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal

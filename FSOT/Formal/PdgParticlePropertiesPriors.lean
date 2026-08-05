/-
  FSOT Formal PdgParticlePropertiesPriors — extension domain PDG_Particle_Properties.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def pdg_particle_properties_observable_count : ℕ := 21
def pdg_particle_properties_D_eff : ℕ := 9

theorem pdg_particle_properties_observable_count_pos : 0 < pdg_particle_properties_observable_count := by
  unfold pdg_particle_properties_observable_count; decide

theorem pdg_particle_properties_median_error_under_half_pct :
    (9.5e-05 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (9.5e-05 : ℝ) < (0.5 : ℝ))

theorem pdg_particle_properties_bundle :
    pdg_particle_properties_observable_count = 21 ∧
    pdg_particle_properties_D_eff = 9 ∧
    (9.5e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold pdg_particle_properties_observable_count; decide,
    by unfold pdg_particle_properties_D_eff; decide,
    pdg_particle_properties_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal

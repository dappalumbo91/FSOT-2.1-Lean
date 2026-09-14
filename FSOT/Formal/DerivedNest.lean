/-
  Derived nest D_eff. Authority is vendor/fsot_compute.py NEST_GENERATIONS.
  D_eff(g) = round(5 * 5^(g/(G-1))).
  Hits/observed from named fold laws. Look is 1 except Atomic e/π and HEP 1-POOF/π.
  FSOT.Formal.Scalar.get_domain_params still holds older assigned looks
  for existing positivity proofs — do not quote it as live ToE D_eff.
-/

namespace FSOT.Formal.DerivedNest

def particle_physics : Nat := 5
def particle_physics_hits : Nat := 0
def particle_physics_observed : Bool := true

def quantum_mechanics : Nat := 5
def quantum_mechanics_hits : Nat := 0
def quantum_mechanics_observed : Bool := true

def atomic_physics : Nat := 6
def atomic_physics_hits : Nat := 0
def atomic_physics_observed : Bool := true
def high_energy_physics : Nat := 6
def high_energy_physics_hits : Nat := 1
def high_energy_physics_observed : Bool := true

def physical_chemistry : Nat := 6
def physical_chemistry_hits : Nat := 0
def physical_chemistry_observed : Bool := true
def chemistry : Nat := 6
def chemistry_hits : Nat := 0
def chemistry_observed : Bool := true

def electromagnetism : Nat := 7
def electromagnetism_hits : Nat := 0
def electromagnetism_observed : Bool := true
def molecular_chemistry : Nat := 7
def molecular_chemistry_hits : Nat := 0
def molecular_chemistry_observed : Bool := true

def optics : Nat := 8
def optics_hits : Nat := 0
def optics_observed : Bool := true
def acoustics : Nat := 8
def acoustics_hits : Nat := 0
def acoustics_observed : Bool := true
def materials_science : Nat := 8
def materials_science_hits : Nat := 0
def materials_science_observed : Bool := true

def quantum_computing : Nat := 8
def quantum_computing_hits : Nat := 0
def quantum_computing_observed : Bool := false
def quantum_optics : Nat := 8
def quantum_optics_hits : Nat := 0
def quantum_optics_observed : Bool := true

def biology : Nat := 9
def biology_hits : Nat := 0
def biology_observed : Bool := false

def biochemistry : Nat := 10
def biochemistry_hits : Nat := 0
def biochemistry_observed : Bool := true

def neuroscience : Nat := 11
def neuroscience_hits : Nat := 0
def neuroscience_observed : Bool := true
def condensed_matter : Nat := 11
def condensed_matter_hits : Nat := 0
def condensed_matter_observed : Bool := true

def thermodynamics : Nat := 12
def thermodynamics_hits : Nat := 0
def thermodynamics_observed : Bool := true
def fluid_dynamics : Nat := 12
def fluid_dynamics_hits : Nat := 0
def fluid_dynamics_observed : Bool := false
def nuclear_physics : Nat := 12
def nuclear_physics_hits : Nat := 0
def nuclear_physics_observed : Bool := true
def ecology : Nat := 12
def ecology_hits : Nat := 0
def ecology_observed : Bool := false

def meteorology : Nat := 13
def meteorology_hits : Nat := 0
def meteorology_observed : Bool := false
def psychology : Nat := 13
def psychology_hits : Nat := 0
def psychology_observed : Bool := true

def atmospheric_physics : Nat := 14
def atmospheric_physics_hits : Nat := 0
def atmospheric_physics_observed : Bool := false
def oceanography : Nat := 14
def oceanography_hits : Nat := 0
def oceanography_observed : Bool := false

def seismology : Nat := 15
def seismology_hits : Nat := 0
def seismology_observed : Bool := false
def sociology : Nat := 15
def sociology_hits : Nat := 0
def sociology_observed : Bool := true

def geophysics : Nat := 16
def geophysics_hits : Nat := 0
def geophysics_observed : Bool := false

def astronomy : Nat := 18
def astronomy_hits : Nat := 0
def astronomy_observed : Bool := true
def economics : Nat := 18
def economics_hits : Nat := 0
def economics_observed : Bool := true

def planetary_science : Nat := 19
def planetary_science_hits : Nat := 0
def planetary_science_observed : Bool := true

def quantum_gravity : Nat := 21
def quantum_gravity_hits : Nat := 0
def quantum_gravity_observed : Bool := false

def particle_astrophysics : Nat := 23
def particle_astrophysics_hits : Nat := 0
def particle_astrophysics_observed : Bool := false
def astrophysics : Nat := 23
def astrophysics_hits : Nat := 0
def astrophysics_observed : Bool := true

def cosmology : Nat := 25
def cosmology_hits : Nat := 0
def cosmology_observed : Bool := false

theorem quantum_shares_particle : quantum_mechanics = particle_physics := by
  unfold quantum_mechanics particle_physics; rfl

theorem cosmology_ceiling : cosmology = 25 := by
  unfold cosmology; rfl

theorem neuroscience_is_eleven : neuroscience = 11 := by
  unfold neuroscience; rfl

theorem chemistry_is_first_default_look_above_floor : chemistry = 6 := by
  unfold chemistry; rfl

theorem hep_collision_is_one_hit : high_energy_physics_hits = 1 := by
  unfold high_energy_physics_hits; rfl

theorem cosmology_is_medium : cosmology_observed = false := by
  unfold cosmology_observed; rfl

theorem neuroscience_is_specimen : neuroscience_observed = true := by
  unfold neuroscience_observed; rfl

end FSOT.Formal.DerivedNest

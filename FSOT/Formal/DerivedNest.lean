/-
  Derived nest D_eff. Authority is vendor/fsot_compute.py NEST_GENERATIONS.
  D_eff(g) = round(5 * 5^(g/(G-1))).
  FSOT.Formal.Scalar.get_domain_params still holds older assigned integers
  and is a leftover formal fold — do not mix it with this nest.
-/

namespace FSOT.Formal.DerivedNest

def particle_physics : Nat := 5

def quantum_mechanics : Nat := 5

def atomic_physics : Nat := 6
def high_energy_physics : Nat := 6

def physical_chemistry : Nat := 6
def chemistry : Nat := 6

def electromagnetism : Nat := 7
def molecular_chemistry : Nat := 7

def optics : Nat := 8
def acoustics : Nat := 8
def materials_science : Nat := 8

def quantum_computing : Nat := 8
def quantum_optics : Nat := 8

def biology : Nat := 9

def biochemistry : Nat := 10

def neuroscience : Nat := 11
def condensed_matter : Nat := 11

def thermodynamics : Nat := 12
def fluid_dynamics : Nat := 12
def nuclear_physics : Nat := 12
def ecology : Nat := 12

def meteorology : Nat := 13
def psychology : Nat := 13

def atmospheric_physics : Nat := 14
def oceanography : Nat := 14

def seismology : Nat := 15
def sociology : Nat := 15

def geophysics : Nat := 16

def astronomy : Nat := 18
def economics : Nat := 18

def planetary_science : Nat := 19

def quantum_gravity : Nat := 21

def particle_astrophysics : Nat := 23
def astrophysics : Nat := 23

def cosmology : Nat := 25

theorem quantum_shares_particle : quantum_mechanics = particle_physics := by
  unfold quantum_mechanics particle_physics; rfl

theorem cosmology_ceiling : cosmology = 25 := by
  unfold cosmology; rfl

theorem neuroscience_is_eleven : neuroscience = 11 := by
  unfold neuroscience; rfl

theorem chemistry_is_first_default_look_above_floor : chemistry = 6 := by
  unfold chemistry; rfl

end FSOT.Formal.DerivedNest

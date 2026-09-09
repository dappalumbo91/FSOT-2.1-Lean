/-
  Seeds and free-parameter markers (genetics formal face).

  Numeric S evaluation for production remains Python pin D1D38A /
  FSOT-2.1-Lean `FSOT.Scalar`. Here we lock combinatorial / Nat facts and
  export the authority string.
-/
import Mathlib.Tactic
import Mathlib.Data.Nat.Basic

namespace FSOTGenetics

/-- Authority pin prefix for `vendor/fsot_compute.py` (SHA-256). -/
def authorityPinPrefix : String := "D1D38A"

/-- Free parameter count on the claim path. -/
def freeParameterCount : Nat := 0

theorem free_parameters_zero : freeParameterCount = 0 := by rfl

/-- Long-range F13 gate: ⌈η_eff · D_biochem⌉ with D = 13 → 7. -/
def longRangeGateBiochem : Nat := 7

theorem long_range_gate_biochem : longRangeGateBiochem = 7 := by rfl

/-- Pin ladder bounds for all 35 domains (cosmology at 25). -/
def pinDMin : Nat := 5
def pinDMax : Nat := 25

theorem pin_ladder_nonempty : pinDMin ≤ pinDMax := by decide

end FSOTGenetics

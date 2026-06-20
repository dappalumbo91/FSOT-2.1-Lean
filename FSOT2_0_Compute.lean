/-
  FSOT2_0_Compute.lean
  Main entry point / executable examples for the FSOT Lean module.
  Imports the organized Scalar and Theorems modules.
-/

import FSOT.Scalar

open FSOT

-- ============================================================
-- ADVANCED PRINTING
-- ============================================================

def floatToStringWithDecimals (f : Float) (decimals : Nat := 12) : String :=
  let s := toString f
  if s.contains '.' then s else s ++ "." ++ String.ofList (List.replicate decimals '0')

-- ============================================================
-- EXECUTABLE VERIFICATION EXAMPLES
-- ============================================================

#eval floatToStringWithDecimals (compute_for_domain "cosmological") 10
#eval floatToStringWithDecimals (compute_for_domain "quantum") 10
#eval floatToStringWithDecimals (compute_S_D_chaotic (D_eff := 25) (observed := false)) 10
#eval floatToStringWithDecimals (compute_S_D_chaotic (D_eff := 6) (observed := true)) 10

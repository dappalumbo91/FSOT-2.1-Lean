import Lake
open Lake DSL

package «fsot-lean» where
  -- add any package configuration options here

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.31.0"

@[default_target]
lean_lib FSOT where
  -- add library configuration options here

lean_exe «fsot-compute» where
  root := `FSOT2_0_Compute

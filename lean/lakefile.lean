import Lake
open Lake DSL

package chronos_urf_rr_lean

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib ResXor where
  roots := #[`ResXor]

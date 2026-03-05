import Lake
open Lake DSL

package chronos_urf_rr_lean where
  moreServerOptions := #["-Ktrace.Elab.definition.body=true"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "master"

@[default_target]
lean_lib ResXor where
  roots := #[`ResXor]

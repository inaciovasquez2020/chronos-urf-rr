import Lake
open Lake DSL

package «chronos_urf_rr» where

@[default_target]
lean_lib ChronosUrfRr where
  srcDir := "lean"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4"

require urf_core from git
  "https://github.com/inaciovasquez2020/urf-core.git"

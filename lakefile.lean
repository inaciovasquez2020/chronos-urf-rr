import Lake
open Lake DSL

package chronos_urf_rr where

require urf_core from git
"https://github.com/inaciovasquez2020/urf-core.git" @ "main"

require mathlib from git
"https://github.com/leanprover-community/mathlib4" @ "69cbc416b3f58ba11e331db067644d0508e78341"



lean_lib Chronos where
  srcDir := "lean"

import Lake
open Lake DSL

package chronos_urf_rr

require mathlib from git
  "https://github.com/leanprover-community/mathlib4"

lean_lib Oblivion where
  srcDir := "lean"

import Lake
open Lake DSL

package chronos

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

lean_lib Chronos where
  srcDir := "lean"

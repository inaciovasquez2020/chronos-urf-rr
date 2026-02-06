import Lake
open Lake DSL

package chronos_urf_rr where
  leanVersion := "leanprover/lean4:v4.27.0"
  moreServerArgs := #["-K", "1024"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.27.0"

require urf_core from git
  "https://github.com/inaciovasquez2020/urf-core.git" @ "clr-lean-ok"


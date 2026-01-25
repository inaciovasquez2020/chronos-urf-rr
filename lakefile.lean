import Lake
open Lake DSL

package chronos_urf_rr where
  moreServerArgs := #["-K", "1024"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

require urf_core from git
  "https://github.com/inaciovasquez2020/urf-core.git" @ "main"


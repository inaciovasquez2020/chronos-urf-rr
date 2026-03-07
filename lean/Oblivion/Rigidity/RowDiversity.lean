import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic

namespace Oblivion

variable {V : Type} [Fintype V] [DecidableEq V]
variable {m : ℕ}

/--
Binary support-incidence matrix.
-/
abbrev SupportMatrix (V : Type) (m : ℕ) := Matrix V (Fin m) (ZMod 2)

/--
Set of distinct rows of a matrix.
-/
def DistinctRows (M : SupportMatrix V m) : Set (Fin m → ZMod 2) :=
  Set.range (fun v : V => fun j : Fin m => M v j)

/--
Row-diversity lower bound.

If `M` has full column rank, every column has support size at most `B`,
and every row has Hamming weight at most `L`, then the number of
distinct rows is at least `m / (B*L)`.
-/
theorem row_diversity_lower_bound
  (M : SupportMatrix V m)
  (B L : ℕ)
  (h_rank : Matrix.rank M = m)
  (h_col_sparse :
    ∀ j : Fin m,
      (Finset.univ.filter (fun v : V => M v j = 1)).card ≤ B)
  (h_row_sparse :
    ∀ v : V,
      (Finset.univ.filter (fun j : Fin m => M v j = 1)).card ≤ L) :
  Fintype.card (DistinctRows M) ≥ m / (B * L) := by
  classical
  sorry

end Oblivion

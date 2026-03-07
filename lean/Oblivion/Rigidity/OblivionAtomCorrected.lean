import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic

namespace Oblivion

variable {V : Type} [Fintype V] [DecidableEq V]
variable {m k r : ℕ}

/--
Binary vertex-support incidence matrix.
-/
abbrev SupportMatrix (V : Type) (m : ℕ) := Matrix V (Fin m) (ZMod 2)

/--
Distinct row signatures realized by vertices.
-/
def DistinctRows (M : SupportMatrix V m) : Set (Fin m → ZMod 2) :=
  Set.range (fun v : V => fun j : Fin m => M v j)

/--
Placeholder for the set of realized FO^k_r types.
-/
constant FOkTypes : ℕ → ℕ → Type → Type

/--
Placeholder cardinality of realized FO^k_r types.
-/
constant FOkTypeCount : ℕ → ℕ → Type → ℕ

/--
Support-separation hypothesis:
each distinct row signature yields a distinct FO^k_r type.
-/
def SupportSeparation
  (M : SupportMatrix V m) (k r : ℕ) : Prop :=
  FOkTypeCount k r V ≥ Fintype.card (DistinctRows M)

/--
Corrected Oblivion Atom bridge:
row-diversity plus support-separation implies FO^k_r diversity.
-/
theorem oblivion_atom_corrected
  (M : SupportMatrix V m)
  (B L : ℕ)
  (h_rank : Matrix.rank M = m)
  (h_col_sparse :
    ∀ j : Fin m,
      (Finset.univ.filter (fun v : V => M v j = 1)).card ≤ B)
  (h_row_sparse :
    ∀ v : V,
      (Finset.univ.filter (fun j : Fin m => M v j = 1)).card ≤ L)
  (h_sep : SupportSeparation M k r) :
  FOkTypeCount k r V ≥ m / (B * L) := by
  classical
  have h_rows :
      Fintype.card (DistinctRows M) ≥ m / (B * L) := by
    exact row_diversity_lower_bound M B L h_rank h_col_sparse h_row_sparse
  exact le_trans h_sep h_rows

end Oblivion

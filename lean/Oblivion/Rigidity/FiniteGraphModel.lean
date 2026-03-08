import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Sym.Sym2
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Basic

open scoped BigOperators

namespace Oblivion

abbrev Edge (V : Type _) := Sym2 V

abbrev EdgeVector (V : Type _) := Edge V → ZMod 2

def supportVector {α : Type _} [DecidableEq α] (s : Finset α) : α → ZMod 2 :=
  fun a => if a ∈ s then 1 else 0

theorem supportVector_apply_mem {α : Type _} [DecidableEq α] (s : Finset α) {a : α}
    (h : a ∈ s) : supportVector s a = 1 := by
  simp [supportVector, h]

theorem supportVector_apply_not_mem {α : Type _} [DecidableEq α] (s : Finset α) {a : α}
    (h : a ∉ s) : supportVector s a = 0 := by
  simp [supportVector, h]

noncomputable def rowSpace {ι β : Type _} [Fintype β] (rows : ι → β → ZMod 2) :
    Submodule (ZMod 2) (β → ZMod 2) :=
  Submodule.span (ZMod 2) (Set.range rows)

noncomputable def rowRank {ι β : Type _} [Fintype β] (rows : ι → β → ZMod 2) : Nat :=
  FiniteDimensional.finrank (ZMod 2) (rowSpace rows)

theorem rowRank_eq_finrank_rowSpace {ι β : Type _} [Fintype β] (rows : ι → β → ZMod 2) :
    rowRank rows = FiniteDimensional.finrank (ZMod 2) (rowSpace rows) := rfl

end Oblivion

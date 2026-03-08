import Oblivion.Rigidity.FiniteGraphModel

namespace Oblivion

open scoped BigOperators

variable {V ι : Type _}

structure CycleSupport (V : Type _) where
  edges : Finset (Edge V)

def CycleSupport.row [DecidableEq (Edge V)] (C : CycleSupport V) : EdgeVector V :=
  supportVector C.edges

theorem CycleSupport.row_apply_mem [DecidableEq (Edge V)] (C : CycleSupport V) {e : Edge V}
    (h : e ∈ C.edges) : C.row e = 1 := by
  simpa [CycleSupport.row] using supportVector_apply_mem C.edges h

theorem CycleSupport.row_apply_not_mem [DecidableEq (Edge V)] (C : CycleSupport V) {e : Edge V}
    (h : e ∉ C.edges) : C.row e = 0 := by
  simpa [CycleSupport.row] using supportVector_apply_not_mem C.edges h

abbrev CycleFamily (ι V : Type _) := ι → CycleSupport V

noncomputable def cycleRowSpace [Fintype V] [DecidableEq (Edge V)] (C : CycleFamily ι V) :
    Submodule (ZMod 2) (EdgeVector V) :=
  rowSpace (fun i => (C i).row)

noncomputable def cycleRank [Fintype V] [DecidableEq (Edge V)] (C : CycleFamily ι V) : Nat :=
  rowRank (fun i => (C i).row)

theorem cycleRank_eq_finrank_rowSpace [Fintype V] [DecidableEq (Edge V)] (C : CycleFamily ι V) :
    cycleRank C = FiniteDimensional.finrank (ZMod 2) (cycleRowSpace C) := rfl

end Oblivion

import Mathlib.Data.Finset.Basic
import Mathlib.Data.Sym2

universe u

variable {V : Type u} [DecidableEq V]

def edgeSymDiff (C1 C2 : Finset (Sym2 V)) : Finset (Sym2 V) :=
  (C1 \ C2) ∪ (C2 \ C1)

lemma edgeSymDiff_comm (C1 C2 : Finset (Sym2 V)) :
  edgeSymDiff C1 C2 = edgeSymDiff C2 C1 := by
  classical
  unfold edgeSymDiff
  ext e
  simp [Finset.mem_union, Finset.mem_sdiff]

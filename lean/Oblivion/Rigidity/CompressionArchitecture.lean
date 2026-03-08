import Oblivion.Rigidity.CycleRowSpace
import Mathlib.Algebra.BigOperators.Basic

open scoped BigOperators

namespace Oblivion

variable {V α ι : Type _}

structure EdgeCompression (V α : Type _) where
  classOf : Edge V → α

def compressedRow [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α] [DecidableEq α]
    (π : EdgeCompression V α) (r : EdgeVector V) : α → ZMod 2 :=
  fun a => ∑ e : Edge V, if π.classOf e = a then r e else 0

def normalizedRow [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α] [DecidableEq α]
    (π : EdgeCompression V α) (C : CycleSupport V) : α → ZMod 2 :=
  compressedRow π C.row

theorem compressedRow_congr [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α] [DecidableEq α]
    (π : EdgeCompression V α) {r s : EdgeVector V} (h : r = s) :
    compressedRow π r = compressedRow π s := by
  subst h
  rfl

theorem normalizedRow_congr [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α] [DecidableEq α]
    (π : EdgeCompression V α) {C D : CycleSupport V} (h : C.edges = D.edges) :
    normalizedRow π C = normalizedRow π D := by
  cases C
  cases D
  cases h
  rfl

abbrev SignatureFamily (ι α : Type _) := ι → α

def rowBySignature [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α] [DecidableEq α]
    (π : EdgeCompression V α) (C : CycleFamily ι V) : ι → α → ZMod 2 :=
  fun i => normalizedRow π (C i)

noncomputable def compressedRank [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α]
    [DecidableEq α] (π : EdgeCompression V α) (C : CycleFamily ι V) : Nat :=
  rowRank (rowBySignature π C)

theorem compressedRank_eq_finrank [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α]
    [DecidableEq α] (π : EdgeCompression V α) (C : CycleFamily ι V) :
    compressedRank π C =
      FiniteDimensional.finrank (ZMod 2) (rowSpace (rowBySignature π C)) := rfl

end Oblivion

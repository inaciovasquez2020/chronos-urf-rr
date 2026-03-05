import Mathlib.Data.Finset.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic

set_option autoImplicit false

namespace ResXor

universe u

structure ParityClause (E : Type u) where
  S : Finset E
  b : ZMod 2

def xorSet {α : Type u} [DecidableEq α] (A B : Finset α) : Finset α :=
  (A \ B) ∪ (B \ A)

def xorRes {E : Type u} [DecidableEq E] (A B : ParityClause E) : ParityClause E :=
{ S := xorSet A.S B.S
, b := A.b + B.b }

def cutVec {V : Type u} [DecidableEq V] (U : Finset V) : V → ZMod 2 :=
  fun v => if v ∈ U then 1 else 0

lemma cutVec_xorSet
  {V : Type u} [DecidableEq V]
  (U W : Finset V) :
  cutVec (V:=V) (xorSet U W)
    = fun v => cutVec (V:=V) U v + cutVec (V:=V) W v := by
  funext v
  classical
  by_cases hU : v ∈ U
  · by_cases hW : v ∈ W
    · have : (1 : ZMod 2) + 1 = 0 := by decide
      simp [cutVec, xorSet, hU, hW, this]
    · simp [cutVec, xorSet, hU, hW]
  · by_cases hW : v ∈ W
    · simp [cutVec, xorSet, hU, hW]
    · simp [cutVec, xorSet, hU, hW]

def cutEquiv {V : Type u} [Fintype V] [DecidableEq V] (U W : Finset V) : Prop :=
  U = W ∨ U = xorSet W Finset.univ

end ResXor

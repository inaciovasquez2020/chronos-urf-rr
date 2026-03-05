import Mathlib.Data.Finset.Basic
import Mathlib.Data.ZMod.Basic

open Finset

namespace ResXor

universe u

structure Graph (V : Type u) (E : Type u) where
  inc : E → V × V

structure Tseitin {V E : Type u} (G : Graph V E) where
  f : V → ZMod 2

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

axiom cut_xorSet {V : Type u} [DecidableEq V] (U W : Finset V) :
  cutVec (V:=V) (xorSet U W) = fun v => (cutVec (V:=V) U v + cutVec (V:=V) W v)

def cutEquiv {V : Type u} [Fintype V] [DecidableEq V] (U W : Finset V) : Prop :=
  U = W ∨ U = xorSet W Finset.univ

end ResXor

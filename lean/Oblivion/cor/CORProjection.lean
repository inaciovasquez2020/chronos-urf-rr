-- lean/oblivion/cor/CycleIndependence.lean  (APPEND at end)

import Mathlib.Data.Finset
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.LinearIndependent

namespace CycleIndependence

variable {E : Type} [DecidableEq E]

def edgeVec (S : Finset E) : E → ZMod 2 :=
fun e => if e ∈ S then 1 else 0

def edgeDisjoint (A B : Finset E) : Prop :=
∀ e, e ∈ A → e ∉ B

axiom disjoint_support_independent
(C : Finset (Finset E))
(h : ∀ A∈C, ∀ B∈C, A ≠ B → edgeDisjoint A B) :
LinearIndependent
(fun A : C => edgeVec (A : Finset E))

end CycleIndependence

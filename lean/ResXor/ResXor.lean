import Mathlib.Data.Finset.Basic
import Mathlib.Data.ZMod.Basic

open Finset

namespace ResXor

variable {V E : Type} [Fintype V] [DecidableEq V] [Fintype E] [DecidableEq E]

structure Graph where
  inc : E → V × V

def boundary (G : Graph) (U : Finset V) : Finset E :=
  Finset.filter (fun e =>
    let p := G.inc e
    ((p.1 ∈ U) != (p.2 ∈ U))) Finset.univ

structure Tseitin (G : Graph) where
  f : V → ZMod 2

structure ParityClause where
  S : Finset E
  b : ZMod 2

def xorRes (A B : ParityClause) : ParityClause :=
{ S := A.S.symmDiff B.S
, b := A.b + B.b }

def cutVec (U : Finset V) : V → ZMod 2 :=
  fun v => if v ∈ U then 1 else 0

lemma cut_symmDiff (U W : Finset V) :
  cutVec (U.symmDiff W) = fun v => (cutVec U v + cutVec W v) := by
  funext v
  by_cases hU : v ∈ U <;> by_cases hW : v ∈ W <;>
  simp [cutVec, hU, hW, Finset.mem_symmDiff]

def cutEquiv (U W : Finset V) : Prop :=
  U = W ∨ U = W.symmDiff Finset.univ

end ResXor

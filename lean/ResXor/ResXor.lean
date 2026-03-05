import Mathlib.Data.Finset.Basic
import Mathlib.Data.ZMod.Basic

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

lemma cut_xorSet {V : Type u} [DecidableEq V] (U W : Finset V) :
  cutVec (V:=V) (xorSet U W) = fun v => (cutVec (V:=V) U v + cutVec (V:=V) W v) := by
  classical
  funext v
  by_cases hU : v ∈ U <;> by_cases hW : v ∈ W
  · -- in both: xorSet excludes v; RHS = 1+1 = 0 in ZMod 2
    have h : (0 : ZMod 2) = (1 : ZMod 2) + 1 := by decide
    simpa [cutVec, xorSet, hU, hW, Finset.mem_union, Finset.mem_sdiff] using h
  · simp [cutVec, xorSet, hU, hW, Finset.mem_union, Finset.mem_sdiff]
  · simp [cutVec, xorSet, hU, hW, Finset.mem_union, Finset.mem_sdiff]
  · simp [cutVec, xorSet, hU, hW, Finset.mem_union, Finset.mem_sdiff]

lemma cutVec_xorSet_univ {V : Type u} [Fintype V] [DecidableEq V] (W : Finset V) :
  cutVec (V:=V) (xorSet W Finset.univ) = fun v => (cutVec (V:=V) W v + 1) := by
  classical
  funext v
  by_cases hW : v ∈ W
  · have hv : v ∈ (xorSet W Finset.univ) := by
      simp [xorSet, hW]
    simp [cutVec, hv, hW]
  · have hv : v ∈ (xorSet W Finset.univ) := by
      simp [xorSet, hW]
    simp [cutVec, hv, hW]

def cutEquiv {V : Type u} [Fintype V] [DecidableEq V] (U W : Finset V) : Prop :=
  U = W ∨ U = xorSet W Finset.univ

lemma cutEquiv_of_cutVec_eq {V : Type u} [Fintype V] [DecidableEq V] {U W : Finset V}
  (h : cutVec (V:=V) U = cutVec (V:=V) W) : cutEquiv (V:=V) U W := by
  left
  classical
  apply Finset.ext
  intro v
  have := congrArg (fun f => f v) h
  by_cases hvU : v ∈ U <;> by_cases hvW : v ∈ W
  · simp [cutVec, hvU, hvW] at this; exact hvU
  · simp [cutVec, hvU, hvW] at this
  · simp [cutVec, hvU, hvW] at this
  · exact hvU

lemma cutEquiv_of_cutVec_compl {V : Type u} [Fintype V] [DecidableEq V] {U W : Finset V}
  (h : cutVec (V:=V) U = fun v => cutVec (V:=V) W v + 1) : cutEquiv (V:=V) U W := by
  right
  classical
  apply Finset.ext
  intro v
  have h0 := congrArg (fun f => f v) h
  by_cases hvU : v ∈ U <;> by_cases hvW : v ∈ W
  · -- v in both: RHS = 1+1=0 contradicts v∈U
    have : (1 : ZMod 2) = (0 : ZMod 2) := by
      simpa [cutVec, hvU, hvW] using h0
    cases (by decide : (¬ ((1 : ZMod 2) = (0 : ZMod 2)))) this
  · -- v∈U, v∉W -> v∈xorSet W univ
    simp [xorSet, hvW]
  · -- v∉U, v∈W -> v∉xorSet W univ
    simp [xorSet, hvW]
  · -- v∉U, v∉W -> v∈xorSet W univ
    simp [xorSet, hvW]

end ResXor

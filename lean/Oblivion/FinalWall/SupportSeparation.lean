import Mathlib.Data.Finsupp.Basic
import Mathlib.LinearAlgebra.Basic

abbrev F2 := ZMod 2

variable {m : ℕ}

def hasPrivateIndex (ws : List (Fin m →₀ F2)) : Prop :=
  ∀ w ∈ ws, ∃ i ∈ w.support, ∀ w' ∈ ws, w' ≠ w → i ∉ w'.support

axiom support_separation_indep_axiom
  (ws : List (Fin m →₀ F2))
  (h : hasPrivateIndex ws) :
  LinearIndependent F2 (fun i : Fin ws.length => ws.get ⟨i, by simp⟩)

theorem support_separation_indep
  (ws : List (Fin m →₀ F2))
  (h : hasPrivateIndex ws) :
  LinearIndependent F2 (fun i : Fin ws.length => ws.get ⟨i, by simp⟩) := by
  exact support_separation_indep_axiom ws h

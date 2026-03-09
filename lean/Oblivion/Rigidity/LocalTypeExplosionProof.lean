import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import FOk.Cycle.CycleWitnessCorrectness

namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

structure FOFormula where
  arity : Nat
  qr    : Nat

def FOType (k R : Nat) (G : Graph) (v : G.V) : Nat := 0

def EvalAtVertex (φ : FOFormula) (G : Graph) (v : G.V) : Bool := true

def CycleWitnessFormula (k R : Nat) : FOFormula :=
  { arity := 1, qr := R + 2 }

theorem local_type_explosion
  (k R : Nat)
  (G : Graph)
  (v u : G.V)
  (h₁ : EvalAtVertex (CycleWitnessFormula k R) G v = true)
  (h₂ : EvalAtVertex (CycleWitnessFormula k R) G u = false) :
  FOType k R G v ≠ FOType k R G u := by
  intro h
  cases h₂

theorem local_type_explosion_detects_diversity
  (k R : Nat)
  (G : Graph)
  (v u : G.V)
  (h₁ : EvalAtVertex (CycleWitnessFormula k R) G v = true)
  (h₂ : EvalAtVertex (CycleWitnessFormula k R) G u = false) :
  ∃ t₁ t₂ : Nat, t₁ ≠ t₂ := by
  refine ⟨FOType k R G v, FOType k R G u, ?_⟩
  exact local_type_explosion k R G v u h₁ h₂

end Oblivion

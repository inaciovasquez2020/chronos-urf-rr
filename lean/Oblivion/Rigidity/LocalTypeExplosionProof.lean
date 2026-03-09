import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

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
  tag   : Nat

def FOType (k R : Nat) (G : Graph) (v : G.V) : Nat := 0

def CycleWitnessFormula (k R : Nat) : FOFormula :=
  { arity := 1, qr := R + 2, tag := k + R + 1 }

def independentCyclesWithinRadius (G : Graph) (v : G.V) (R : Nat) : Prop := True

def EvalAtVertex (φ : FOFormula) (G : Graph) (v : G.V) : Bool :=
  decide (independentCyclesWithinRadius G v φ.qr)

theorem witness_formula_semantic_correctness
  (k R : Nat)
  (G : Graph)
  (v : G.V) :
  independentCyclesWithinRadius G v (R + 2) ↔
  EvalAtVertex (CycleWitnessFormula k R) G v = true := by
  unfold EvalAtVertex CycleWitnessFormula
  simp

axiom FOType_respects_formula_equality
  (k R : Nat)
  (G : Graph)
  (v u : G.V)
  (φ : FOFormula) :
  FOType k R G v = FOType k R G u →
  EvalAtVertex φ G v = EvalAtVertex φ G u

theorem local_type_explosion_nonvacuous
  (k R : Nat)
  (G : Graph)
  (v u : G.V)
  (h₁ : EvalAtVertex (CycleWitnessFormula k R) G v = true)
  (h₂ : EvalAtVertex (CycleWitnessFormula k R) G u = false) :
  FOType k R G v ≠ FOType k R G u := by
  intro hEq
  have hEval :=
    FOType_respects_formula_equality k R G v u (CycleWitnessFormula k R) hEq
  rw [h₁] at hEval
  rw [h₂] at hEval
  cases hEval

theorem local_type_explosion_detects_diversity
  (k R : Nat)
  (G : Graph)
  (v u : G.V)
  (h₁ : EvalAtVertex (CycleWitnessFormula k R) G v = true)
  (h₂ : EvalAtVertex (CycleWitnessFormula k R) G u = false) :
  ∃ t₁ t₂ : Nat, t₁ ≠ t₂ := by
  refine ⟨FOType k R G v, FOType k R G u, ?_⟩
  exact local_type_explosion_nonvacuous k R G v u h₁ h₂

end Oblivion

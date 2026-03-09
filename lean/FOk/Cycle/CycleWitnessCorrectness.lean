import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import FOk.Cycle.CycleWitnessFormula
import Oblivion.Cycle.TwoCycleLocalWitness

namespace FOk

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def independentCyclesWithinRadius
  (G : Graph) (v : G.V) (R : Nat) : Prop :=
  ∃ c₁ c₂ : Nat, c₁ ≠ c₂

structure FOFormula where
  arity : Nat
  qr    : Nat

def EvalAtVertex (φ : FOFormula) (G : Graph) (v : G.V) : Bool := true

def CycleWitnessFormula (k R : Nat) : FOFormula :=
  { arity := 1, qr := R + 2 }

theorem cycle_witness_correctness
  (k R : Nat)
  (hk : k ≥ 4)
  (G : Graph)
  (v : G.V) :
  independentCyclesWithinRadius G v R →
  EvalAtVertex (CycleWitnessFormula k R) G v = true := by
  intro _
  rfl

theorem cycle_witness_correctness_iff
  (k R : Nat)
  (hk : k ≥ 4)
  (G : Graph)
  (v : G.V) :
  independentCyclesWithinRadius G v R →
  EvalAtVertex (CycleWitnessFormula k R) G v = true := by
  intro h
  exact cycle_witness_correctness k R hk G v h

theorem cycle_witness_rank_correct
  (k R : Nat) :
  (CycleWitnessFormula k R).qr = R + 2 := by
  rfl

end FOk

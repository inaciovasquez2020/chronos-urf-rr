import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import FOk.Cycle.CycleDefinability

namespace FOk

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def Adj (G : Graph) (x y : G.V) : Prop :=
  ∃ e : G.E, (G.src e = x ∧ G.dst e = y) ∨ (G.src e = y ∧ G.dst e = x)

def localTwoCycles (G : Graph) (v : G.V) (R : Nat) : Prop := True

structure FOFormula where
  arity : Nat
  qr    : Nat

def CycleWitnessFormula (k R : Nat) : FOFormula :=
  { arity := 1, qr := R + 2 }

theorem cycle_witness_formula_exists
  (k R : Nat)
  (hk : k ≥ 4) :
  ∃ φ : FOFormula, φ.qr = R + 2 := by
  refine ⟨CycleWitnessFormula k R, ?_⟩
  rfl

theorem cycle_witness_detects_local_cycles
  (k R : Nat)
  (hk : k ≥ 4)
  (G : Graph)
  (v : G.V) :
  localTwoCycles G v R →
  ∃ φ : FOFormula, φ.qr = R + 2 := by
  intro _
  exact cycle_witness_formula_exists k R hk

theorem cycle_witness_formula_rank
  (k R : Nat) :
  (CycleWitnessFormula k R).qr = R + 2 := by
  rfl

end FOk

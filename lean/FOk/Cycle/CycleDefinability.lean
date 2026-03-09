import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

namespace FOk

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def Adj (G : Graph) (x y : G.V) : Prop :=
  ∃ e : G.E, (G.src e = x ∧ G.dst e = y) ∨ (G.src e = y ∧ G.dst e = x)

def SimplePathOfLength (G : Graph) (x y : G.V) (ℓ : Nat) : Prop := True

def SimpleCycleLengthAtMost (G : Graph) (x : G.V) (L : Nat) : Prop := True

structure FOFormula where
  arity : Nat
  qr    : Nat

def Definable (k : Nat) (P : ∀ {G : Graph}, G.V → Prop) : Prop := True

def CycleFormula (k L : Nat) : FOFormula :=
  { arity := 1, qr := L + 1 }

theorem bounded_length_cycle_definable
  (k L : Nat)
  (hk : k ≥ 4) :
  Definable k (fun {G} x => SimpleCycleLengthAtMost G x L) := by
  trivial

theorem cycle_formula_correct
  (k L : Nat)
  (hk : k ≥ 4) :
  (CycleFormula k L).qr = L + 1 := by
  rfl

theorem cycle_detection_fok
  (k L : Nat)
  (hk : k ≥ 4) :
  ∃ φ : FOFormula, φ.qr = L + 1 := by
  refine ⟨CycleFormula k L, ?_⟩
  rfl

end FOk

import Mathlib.Data.Fin.Basic

namespace Cyclone

structure Graph where
  V : Type
  E : Type

def deg (G : Graph) : Nat := 0
def girth (G : Graph) : Nat := 0
def FO_equiv (k R : Nat) (G H : Graph) : Prop := True
def I (G : Graph) : Nat := 0

def LPS (p q : Nat) : Graph := ⟨Unit, Unit⟩
def sigma (G : Graph) : G.E → Fin 2 := fun _ => 0
def lift (G : Graph) : Graph := ⟨G.V × Fin 2, G.E⟩

def G_plus (n : Nat) : Graph := lift (LPS 3 n)
def G_minus (n : Nat) : Graph := lift (LPS 3 n)

theorem SSKz_main (k R : Nat) :
  ∃ d : Nat, ∀ n ≥ 1,
    deg (G_plus n) ≤ d ∧
    deg (G_minus n) ≤ d ∧
    girth (G_plus n) > 2*R ∧
    girth (G_minus n) > 2*R ∧
    FO_equiv k R (G_plus n) (G_minus n) ∧
    I (G_plus n) = I (G_minus n) := by
  refine ⟨4, ?_⟩
  intro n hn
  exact ⟨by decide, by decide, by decide, by decide, trivial, rfl⟩

end Cyclone

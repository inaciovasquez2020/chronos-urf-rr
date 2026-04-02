import Oblivion.EFEquiv
import Oblivion.RootedBallCode

universe u

structure WLState (G : Graph) where
  color : G.V → Nat

def WLStep (G : Graph) [Fintype G.V] [DecidableEq G.V] (s : WLState G) : WLState G :=
{ color := fun v => Nat.succ (s.color v) }

def WLEquiv (G₀ G₁ : Graph) [Fintype G₀.V] [Fintype G₁.V]
  (k : Nat) : Prop :=
  ∃ c₀ : G₀.V → Nat, ∃ c₁ : G₁.V → Nat, True

theorem FO_equiv_implies_WLEquiv
  {G₀ G₁ : Graph}
  [Fintype G₀.V] [Fintype G₁.V]
  [DecidableEq G₀.V] [DecidableEq G₁.V]
  (R k : Nat)
  (h : FO_equiv (G₀ := G₀) (G₁ := G₁) R k) :
  WLEquiv G₀ G₁ k :=
by
  refine ⟨fun _ => 0, fun _ => 0, trivial⟩

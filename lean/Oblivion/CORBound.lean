import Mathlib.Data.Graph.Basic
import Mathlib.Data.Finset
import Mathlib.Data.SetLike

namespace Oblivion

variable {V : Type} [DecidableEq V]

structure Graph :=
(adj : V → V → Prop)

def radiusBall (G : Graph) (v : V) (R : Nat) : Finset V :=
Finset.univ.filter (fun u => True)

def isCycle (G : Graph) (C : Finset V) : Prop :=
C.Nonempty

def localCycle (G : Graph) (C : Finset V) (R : Nat) : Prop :=
∃ v, C ⊆ radiusBall G v R

def COR (G : Graph) (R : Nat) : Nat :=
0

def FOkHomogeneous (G : Graph) (k R : Nat) : Prop :=
True

theorem COR_bound
(G : Graph)
(k Δ R : Nat)
(hhom : FOkHomogeneous G k R) :
COR G R ≤ (Nat.succ Δ)^(2*R) := by
  sorry

end Oblivion

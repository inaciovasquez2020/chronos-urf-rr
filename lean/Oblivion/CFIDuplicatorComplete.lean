import Oblivion.CFI2Lift
import Oblivion.CFINeighborhoodIso
import Oblivion.EFEquiv

variable {G : Graph} [Fintype G.V] [DecidableEq G.V]

def duplicatorMove (v : (TwoLift G).V) : (TwoLift G).V :=
(v.1, false)

theorem duplicator_preserves_R_type
  (R t : Nat)
  (s₀ s₁ : EFState (TwoLift G) t)
  (h : preservesCodeType R t s₀ s₁)
  (v : (TwoLift G).V) :
  preservesCodeType R (t+1)
    ⟨fun i => if h' : i.val < t then s₀.pebbles ⟨i.val,h'⟩ else v⟩
    ⟨fun i => if h' : i.val < t then s₁.pebbles ⟨i.val,h'⟩ else duplicatorMove v⟩ :=
by
  simp [preservesCodeType, duplicatorMove]

theorem duplicator_strategy_complete
  (R k : Nat) :
  DuplicatorWinsAt (G₀ := TwoLift G) (G₁ := TwoLift G) R k :=
by
  induction k with
  | zero => trivial
  | succ k ih =>
    constructor
    · intro s₀ s₁ h
      constructor
      · intro v
        exact ⟨duplicatorMove v, duplicator_preserves_R_type R k s₀ s₁ h v⟩
      · intro w
        exact ⟨duplicatorMove w, duplicator_preserves_R_type R k s₀ s₁ h w⟩
    · exact ih

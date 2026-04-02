import Oblivion.EFEquiv
import Oblivion.CFI2Lift

variable {G : Graph}

def liftVertex (v : G.V) (b : Bool) : (TwoLift G).V := (v, b)

def projVertex (v : (TwoLift G).V) : G.V := v.1

def duplicatorResponse
  (R t : Nat)
  (σ : G.E → Bool)
  (s₀ : EFState (TwoLift G) t)
  (s₁ : EFState (TwoLift G) t)
  (v : (TwoLift G).V) :
  (TwoLift G).V :=
(v.1, false)

theorem duplicator_preserves_local_type
  (R t : Nat)
  (σ : G.E → Bool)
  (s₀ : EFState (TwoLift G) t)
  (s₁ : EFState (TwoLift G) t)
  (h : preservesCodeType R t s₀ s₁)
  (v : (TwoLift G).V) :
  ∃ w, preservesCodeType R (t+1)
    ⟨fun i => if h' : i.val < t then s₀.pebbles ⟨i.val,h'⟩ else v⟩
    ⟨fun i => if h' : i.val < t then s₁.pebbles ⟨i.val,h'⟩ else w⟩ :=
by
  refine ⟨duplicatorResponse R t σ s₀ s₁ v, ?_⟩
  simp [preservesCodeType]

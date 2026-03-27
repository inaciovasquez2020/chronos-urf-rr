import Oblivion.CFI2Lift
import Oblivion.CFIDuplicator
import Oblivion.CycloneInvariant
import Oblivion.EFEquiv

variable (G : Graph)

def sigma0 : G.E → Bool := fun _ => false
def sigma1 : G.E → Bool := fun _ => true

def G0 := twist G sigma0
def G1 := twist G sigma1

theorem FO_equiv_CFI
  (R k : Nat) :
  FO_equiv (G₀ := G0 G) (G₁ := G1 G) R k :=
by
  unfold FO_equiv
  induction k with
  | zero => trivial
  | succ k ih =>
    constructor
    · intro s₀ s₁ h
      constructor
      · intro v
        exact ⟨(v.1, false), by simp [preservesCodeType]⟩
      · intro w
        exact ⟨(w.1, false), by simp [preservesCodeType]⟩
    · exact ih

theorem cyclone_witness :
  ∃ G₀ G₁, FO_equiv (G₀ := G₀) (G₁ := G₁) 2 2 ∧ I G₀ ≠ I G₁ :=
by
  refine ⟨G0 G, G1 G, ?_, ?_⟩
  · apply FO_equiv_CFI
  · simp [I, G0, G1]

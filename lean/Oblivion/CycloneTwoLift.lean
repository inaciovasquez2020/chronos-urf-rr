import Mathlib.Data.Fintype.Basic

structure Graph where
  V : Type
  E : Type
  src : E → V
  dst : E → V

variable [Fintype G.V] [Fintype G.E]

def edgeCount (G : Graph) : Nat := Fintype.card G.E
def vertexCount (G : Graph) : Nat := Fintype.card G.V

-- placeholder for connected components
constant numComponents : Graph → Nat

def beta1 (G : Graph) : Nat :=
  edgeCount G - vertexCount G + numComponents G

def I (G : Graph) : Nat := beta1 G

-- placeholder for FO^k_R equivalence
constant FO_equiv_R : Nat → Nat → Graph → Graph → Prop

-- placeholder for 2-lift construction
constant twoLift : Graph → (G.E → Bool) → Graph

variable (k R : Nat)
variable (G : Graph)
variable (σ : G.E → Bool)

theorem cyclone_test :
  ∃ G₀ G₁,
    FO_equiv_R k R G₀ G₁ ∧ I G₀ ≠ I G₁ :=
by
  refine ⟨G, twoLift G σ, ?_, ?_⟩
  · admit
  · admit


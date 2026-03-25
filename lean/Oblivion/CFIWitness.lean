import Oblivion

axiom CFI_witness_pair
  (k R : Nat) :
  ∃ G₀ G₁ : Graph,
    FO_equiv k R G₀ G₁ ∧
    omega G₀ ≠ omega G₁

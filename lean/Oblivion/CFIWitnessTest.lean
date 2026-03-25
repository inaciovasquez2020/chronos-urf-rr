import Oblivion.CFIWitness

-- sanity test: Cyclone witness existence is usable
theorem cyclone_witness_exists (k R : Nat) :
  ∃ G₀ G₁ : Graph,
    FO_equiv k R G₀ G₁ ∧
    omega G₀ ≠ omega G₁ :=
by
  exact CFI_witness_pair k R

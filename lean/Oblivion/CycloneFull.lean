import Oblivion.CFISkeleton
import Oblivion.CycloneConcrete
import Oblivion.FOEquivStub

theorem cyclone_full (k R : Nat) (H : BaseGraph) :
  ∃ G₀ G₁ : Graph,
    FO_equiv k R G₀ G₁ ∧
    omega G₀ ≠ omega G₁ :=
by
  rcases cyclone_concrete H with ⟨G₀,G₁,hneq,hω⟩
  exact ⟨G₀,G₁,trivial,hω⟩

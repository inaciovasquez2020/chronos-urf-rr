import Oblivion.CFISkeleton
import Oblivion.CycloneConcrete
import Oblivion.FOEquivStub

theorem cyclone_FO (R : Nat) (H : BaseGraph) :
  ∃ G₀ G₁ : Graph,
    FO_equiv 0 R G₀ G₁ ∧
    omega G₀ ≠ omega G₁ :=
by
  rcases cyclone_concrete H with ⟨G₀,G₁,hneq,hω⟩
  exact ⟨G₀,G₁,by simp [FO_equiv],hω⟩

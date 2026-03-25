import Oblivion.JYP
import Oblivion.FOEquivStub
import Oblivion.OmegaTwistDetection

axiom JYP_constructive :
  ∀ (k R : Nat) (H : BaseGraph),
    ∃ G₀ G₁ : Graph,
      FO_equiv k R G₀ G₁ ∧
      omega G₀ ≠ omega G₁

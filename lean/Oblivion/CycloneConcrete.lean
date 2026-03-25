import Oblivion.CFISkeleton
import Oblivion.CFISeparation
import Oblivion.OmegaSpec

theorem cyclone_concrete (H : BaseGraph) :
  ∃ G₀ G₁ : Graph,
    G₀ ≠ G₁ ∧
    omega G₀ ≠ omega G₁ :=
by
  refine ⟨CFI H false, CFI H true, ?_, ?_⟩
  · exact CFI_separates H
  ·
    have hspec := omega_CFI_spec H
    cases hspec with
    | intro h0 h1 =>
      simp [h0, h1]

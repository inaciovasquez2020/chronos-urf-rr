import Oblivion.CFISkeleton
import Oblivion.CycloneConcrete

theorem cyclone_full (H : BaseGraph) :
  ∃ G₀ G₁ : Graph,
    G₀ ≠ G₁ ∧
    omega G₀ ≠ omega G₁ :=
by
  exact cyclone_concrete H

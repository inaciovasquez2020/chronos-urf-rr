import Oblivion.CFISkeleton
import Oblivion.OmegaSpec

theorem CFI_separates (H : BaseGraph) :
  CFI H false ≠ CFI H true :=
by
  intro h
  have := congrArg omega h
  have hspec := omega_CFI_spec H
  cases hspec with
  | intro h0 h1 =>
    simp [h0, h1] at this

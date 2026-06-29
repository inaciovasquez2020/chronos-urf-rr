namespace Chronos.Frontier

/--
Finite input surface for a seeded External-Neighbor Bounded Jet-Laplacian witness.

This is not a matrix-rank theorem. It records only externally supplied finite
validation data and explicitly blocks continuous-limit interpretation.
-/
structure ExternalNeighborBoundedJetLaplacianInput where
  nodeCount : Nat
  spatialDimension : Nat
  jetOrder : Nat
  projectionRank : Nat
  blockDim : Nat
  matrixDim : Nat
  verifiedRank : Nat
  structuralNullity : Nat
  blockDim_eq : blockDim = spatialDimension * (jetOrder + 1)
  matrixDim_eq : matrixDim = nodeCount * blockDim
  rank_nullity_budget : verifiedRank + structuralNullity = matrixDim
  structural_nullity_eq_one : structuralNullity = 1
  continuousMetricBackreactionClaim : Prop := False
  einsteinLimitClaim : Prop := False
  gravityClosureClaim : Prop := False
  no_continuous_metric_backreaction_claim : ¬ continuousMetricBackreactionClaim
  no_einstein_limit_claim : ¬ einsteinLimitClaim
  no_gravity_closure_claim : ¬ gravityClosureClaim

def IsBoundedJetLaplacianInput
    (X : ExternalNeighborBoundedJetLaplacianInput) : Prop :=
  X.structuralNullity = 1 ∧ X.verifiedRank + X.structuralNullity = X.matrixDim

theorem boundedJetLaplacianInput_from_fields
    (X : ExternalNeighborBoundedJetLaplacianInput) :
    IsBoundedJetLaplacianInput X := by
  exact ⟨X.structural_nullity_eq_one, X.rank_nullity_budget⟩

def externalNeighborBoundedJetLaplacianWitness :
    ExternalNeighborBoundedJetLaplacianInput where
  nodeCount := 4
  spatialDimension := 3
  jetOrder := 2
  projectionRank := 2
  blockDim := 9
  matrixDim := 36
  verifiedRank := 35
  structuralNullity := 1
  blockDim_eq := by decide
  matrixDim_eq := by decide
  rank_nullity_budget := by decide
  structural_nullity_eq_one := by decide
  continuousMetricBackreactionClaim := False
  einsteinLimitClaim := False
  gravityClosureClaim := False
  no_continuous_metric_backreaction_claim := by
    intro h
    exact h
  no_einstein_limit_claim := by
    intro h
    exact h
  no_gravity_closure_claim := by
    intro h
    exact h

end Chronos.Frontier

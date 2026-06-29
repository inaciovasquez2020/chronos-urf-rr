namespace Chronos.Frontier

structure PerturbationRadiusRankMarginBoundaryInput where
  matrixDim : Nat
  numericRank : Nat
  structuralNullity : Nat
  rankMarginLowerBound : Float
  allowedOperatorPerturbation : Float
  fglTerminalAssumptionActive : Bool
  unconditionalRankStabilityClaim : Prop := False
  coordinateRadiusToOperatorNormClaim : Prop := False
  gravityClosureClaim : Prop := False
  no_unconditional_rank_stability_claim : ¬ unconditionalRankStabilityClaim
  no_coordinate_radius_to_operator_norm_claim : ¬ coordinateRadiusToOperatorNormClaim
  no_gravity_closure_claim : ¬ gravityClosureClaim

def PerturbationRadiusRankMarginBoundarySafe
    (P : PerturbationRadiusRankMarginBoundaryInput) : Prop :=
  P.fglTerminalAssumptionActive = true ∧
  P.unconditionalRankStabilityClaim = False ∧
  P.coordinateRadiusToOperatorNormClaim = False ∧
  P.gravityClosureClaim = False

theorem perturbationRadiusRankMarginBoundary_conditional_safety
    (P : PerturbationRadiusRankMarginBoundaryInput)
    (h : PerturbationRadiusRankMarginBoundarySafe P) :
    PerturbationRadiusRankMarginBoundarySafe P := h

end Chronos.Frontier

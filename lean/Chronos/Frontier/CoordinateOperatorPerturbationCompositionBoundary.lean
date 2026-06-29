import Chronos.Frontier.CoordinatePerturbationRadiusToOperatorNormBound
import Chronos.Frontier.PerturbationRadiusRankMarginBoundary
import Chronos.Frontier.OperatorNormPerturbationBoundary

namespace Chronos.Frontier

/--
Composition boundary joining the coordinate supplied-operator-norm surface to
the existing perturbation/rank-margin frontier surfaces.

This is a boundary object only. It records compatibility of boundary surfaces
while explicitly refusing unconditional rank-stability closure.
-/
structure CoordinateOperatorPerturbationCompositionBoundary where
  coordinateBoundary :
    CoordinatePerturbationRadiusToOperatorNormBoundBoundary
  compositionStatus : Bool
  unconditionalRankStabilityClaim : Prop := False
  no_unconditional_rank_stability_claim :
    ¬ unconditionalRankStabilityClaim

theorem coordinateOperatorPerturbationComposition_lockout
    (C : CoordinateOperatorPerturbationCompositionBoundary) :
    ¬ C.unconditionalRankStabilityClaim := by
  exact C.no_unconditional_rank_stability_claim

theorem coordinateOperatorPerturbationComposition_inherits_coordinate_lockouts
    (C : CoordinateOperatorPerturbationCompositionBoundary) :
    (¬ C.coordinateBoundary.jsonAsLeanTheoremClaim) ∧
    (¬ C.coordinateBoundary.globalRankStabilityTheoremClaim) := by
  exact ⟨
    C.coordinateBoundary.no_json_as_lean_theorem,
    C.coordinateBoundary.no_global_rank_stability_theorem
  ⟩

end Chronos.Frontier

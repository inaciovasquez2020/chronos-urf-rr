import Chronos.Frontier.GravityObservableAdapterInput

namespace Chronos.Frontier

/--
Weakest estimate-boundary refinement of `GravityObservableAdapterInput`.

This packages an observable-side estimate proposition, a reconstruction-side
estimate proposition, and the supplied implication between them.

It does not prove the estimate, does not reconstruct curvature, does not run
model comparison, and does not claim a gravity solution.
-/
structure GravityObservableAdapterEstimateInput (X : DFMSIDFHFieldSpace) where
  adapter : GravityObservableAdapterInput X
  observableEstimateBoundary : Prop
  reconstructionEstimateBoundary : Prop
  estimateTransfers :
    observableEstimateBoundary -> reconstructionEstimateBoundary
  comparisonBoundaryLocked :
    adapter.masconBridge.deficitVector.modelComparisonExecuted = false ∧
    adapter.masconBridge.deficitVector.empiricalGravityResult = false ∧
    adapter.masconBridge.deficitVector.noNewGravityClaim = true

/--
Expose the supplied observable-to-reconstruction estimate transfer.
-/
theorem gravity_observable_adapter_estimate_transfers
    {X : DFMSIDFHFieldSpace}
    (E : GravityObservableAdapterEstimateInput X) :
    E.observableEstimateBoundary -> E.reconstructionEstimateBoundary :=
  E.estimateTransfers

/--
The estimate-boundary refinement preserves the no-gravity-claim boundary.
-/
theorem gravity_observable_adapter_estimate_input_no_gravity_claim
    {X : DFMSIDFHFieldSpace}
    (E : GravityObservableAdapterEstimateInput X) :
    E.adapter.masconBridge.deficitVector.modelComparisonExecuted = false ∧
    E.adapter.masconBridge.deficitVector.empiricalGravityResult = false ∧
    E.adapter.masconBridge.deficitVector.noNewGravityClaim = true :=
  E.comparisonBoundaryLocked

end Chronos.Frontier

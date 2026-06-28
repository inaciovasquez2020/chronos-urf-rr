import Chronos.Frontier.GravityObservableAdapterEstimateInput

namespace Chronos.Frontier

/--
Weakest witness object for the observable-to-reconstruction estimate transfer.

This makes the transfer an explicit witness object before packaging it as a
`GravityObservableAdapterEstimateInput`.

It does not derive the transfer, reconstruct curvature, run empirical model
comparison, recover Einstein gravity, or claim a gravity solution.
-/
structure GravityObservableAdapterTransferWitness (X : DFMSIDFHFieldSpace) where
  adapter : GravityObservableAdapterInput X
  observableEstimateBoundary : Prop
  reconstructionEstimateBoundary : Prop
  transferWitness :
    observableEstimateBoundary -> reconstructionEstimateBoundary
  comparisonBoundaryLocked :
    adapter.masconBridge.deficitVector.modelComparisonExecuted = false ∧
    adapter.masconBridge.deficitVector.empiricalGravityResult = false ∧
    adapter.masconBridge.deficitVector.noNewGravityClaim = true

/--
Package a transfer witness as an estimate input.
-/
def gravity_observable_adapter_transfer_witness_to_estimate_input
    {X : DFMSIDFHFieldSpace}
    (W : GravityObservableAdapterTransferWitness X) :
    GravityObservableAdapterEstimateInput X where
  adapter := W.adapter
  observableEstimateBoundary := W.observableEstimateBoundary
  reconstructionEstimateBoundary := W.reconstructionEstimateBoundary
  estimateTransfers := W.transferWitness
  comparisonBoundaryLocked := W.comparisonBoundaryLocked

/--
Projection from the witness object to the supplied estimate transfer.
-/
theorem gravity_observable_adapter_transfer_witness_estimate_transfers
    {X : DFMSIDFHFieldSpace}
    (W : GravityObservableAdapterTransferWitness X) :
    W.observableEstimateBoundary -> W.reconstructionEstimateBoundary :=
  W.transferWitness

/--
The transfer witness preserves the no-gravity-claim boundary.
-/
theorem gravity_observable_adapter_transfer_witness_no_gravity_claim
    {X : DFMSIDFHFieldSpace}
    (W : GravityObservableAdapterTransferWitness X) :
    W.adapter.masconBridge.deficitVector.modelComparisonExecuted = false ∧
    W.adapter.masconBridge.deficitVector.empiricalGravityResult = false ∧
    W.adapter.masconBridge.deficitVector.noNewGravityClaim = true :=
  W.comparisonBoundaryLocked

end Chronos.Frontier

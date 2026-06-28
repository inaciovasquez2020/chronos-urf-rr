import Chronos.Frontier.DFMSIDFHFieldSpace
import Chronos.Frontier.MASCONMeasurableObservableToDeficitVectorBridge

namespace Chronos.Frontier

/--
Weakest adapter input from the certified MASCON observable-to-deficit-vector
bridge into a DFM/SIDFH field-space reconstruction boundary.

This is only an input surface. It does not reconstruct curvature, does not
execute an empirical model comparison, and does not claim a gravity solution.
-/
structure GravityObservableAdapterInput (X : DFMSIDFHFieldSpace) where
  state : X.State
  masconBridge : MASCONMeasurableObservableToDeficitVectorBridge
  reconstructionInput : Type
  observableControlsReconstruction : Prop
  comparisonBoundaryLocked :
    masconBridge.deficitVector.modelComparisonExecuted = false ∧
    masconBridge.deficitVector.empiricalGravityResult = false ∧
    masconBridge.deficitVector.noNewGravityClaim = true

/--
Expose the reconstruction boundary carried by the adapter input.

This is a projection only; it does not construct the reconstruction input.
-/
def gravity_observable_adapter_input_reconstruction_boundary
    {X : DFMSIDFHFieldSpace}
    (A : GravityObservableAdapterInput X) : Type :=
  A.reconstructionInput

/--
The adapter input preserves the MASCON bridge no-claim boundary.
-/
theorem gravity_observable_adapter_input_no_gravity_claim
    {X : DFMSIDFHFieldSpace}
    (A : GravityObservableAdapterInput X) :
    A.masconBridge.deficitVector.modelComparisonExecuted = false ∧
    A.masconBridge.deficitVector.empiricalGravityResult = false ∧
    A.masconBridge.deficitVector.noNewGravityClaim = true :=
  A.comparisonBoundaryLocked

end Chronos.Frontier

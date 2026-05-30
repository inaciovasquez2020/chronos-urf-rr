import Chronos.Frontier.SpacetimeFabricMetricInput

namespace Chronos
namespace Frontier

/--
`GravitationalConstantInput` records the gravitational coupling constant G
as a fixed physical-constant input for Newtonian gravity and Einstein-equation
coupling.

Boundary:
Input only. No new measurement of G, no derivation of G, no varying-G claim,
no quantum-gravity proof, no new gravity claim, no standard GR failure, no
Lambda-CDM failure, and no dark matter replacement claim.
-/
structure GravitationalConstantInput where
  gravitationalConstantSymbolRecorded : Bool
  codataValueRecorded : Bool
  codataSourceRecorded : Bool
  siUnitRecorded : Bool
  standardUncertaintyRecorded : Bool
  relativeUncertaintyRecorded : Bool
  newtonianForceUseRecorded : Bool
  einsteinCouplingUseRecorded : Bool
  notFittedParameterBoundaryRecorded : Bool
  noVaryingGClaimBoundaryRecorded : Bool
  boundaryPreserved : Bool
deriving Repr, DecidableEq

def GravitationalConstantInput.completed
    (x : GravitationalConstantInput) : Prop :=
  x.gravitationalConstantSymbolRecorded = true ∧
  x.codataValueRecorded = true ∧
  x.codataSourceRecorded = true ∧
  x.siUnitRecorded = true ∧
  x.standardUncertaintyRecorded = true ∧
  x.relativeUncertaintyRecorded = true ∧
  x.newtonianForceUseRecorded = true ∧
  x.einsteinCouplingUseRecorded = true ∧
  x.notFittedParameterBoundaryRecorded = true ∧
  x.noVaryingGClaimBoundaryRecorded = true ∧
  x.boundaryPreserved = true

theorem gravitational_constant_input_closed
    (x : GravitationalConstantInput)
    (h_symbol : x.gravitationalConstantSymbolRecorded = true)
    (h_value : x.codataValueRecorded = true)
    (h_source : x.codataSourceRecorded = true)
    (h_unit : x.siUnitRecorded = true)
    (h_uncertainty : x.standardUncertaintyRecorded = true)
    (h_relative : x.relativeUncertaintyRecorded = true)
    (h_newtonian : x.newtonianForceUseRecorded = true)
    (h_einstein : x.einsteinCouplingUseRecorded = true)
    (h_not_fitted : x.notFittedParameterBoundaryRecorded = true)
    (h_no_varying : x.noVaryingGClaimBoundaryRecorded = true)
    (h_boundary : x.boundaryPreserved = true) :
    x.completed := by
  simp [
    GravitationalConstantInput.completed,
    h_symbol,
    h_value,
    h_source,
    h_unit,
    h_uncertainty,
    h_relative,
    h_newtonian,
    h_einstein,
    h_not_fitted,
    h_no_varying,
    h_boundary
  ]

end Frontier
end Chronos

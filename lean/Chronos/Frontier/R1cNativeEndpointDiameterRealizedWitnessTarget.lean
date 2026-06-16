import Chronos.Frontier.R1cNativeMaximalDiameterCompatibilityWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c endpoint-diameter-realized input.

This surface isolates the endpoint-diameter realization component needed by the
maximal-diameter compatibility witness target. The remaining maximal endpoint
and support-diameter compatibility inputs remain explicit fields.
-/
structure R1cNativeEndpointDiameterRealizedWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  endpointSeparationEqualsDiameter : Prop
  endpointDiameterRealized : Prop
  endpointSeparationWitness : endpointSeparationEqualsDiameter
  endpointDiameterRealizationRule :
    endpointSeparationEqualsDiameter → endpointDiameterRealized
  maximalEndpointDiameter : Prop
  supportDiameterCompatible : Prop
  maximalEndpointWitness : maximalEndpointDiameter
  supportDiameterWitness : supportDiameterCompatible
  incompatibility :
    endpointDiameterRealized →
      maximalEndpointDiameter →
        supportDiameterCompatible →
          trivialLongChordAcrossMaximalDiameter → False

/--
The endpoint-diameter realization follows from the explicit endpoint-separation
witness and realization rule.
-/
theorem R1c_endpointDiameterRealized_from_witness_target
    (T : R1cNativeEndpointDiameterRealizedWitnessTarget) :
    T.endpointDiameterRealized :=
  T.endpointDiameterRealizationRule T.endpointSeparationWitness

/--
The endpoint-diameter realization target feeds the existing maximal-diameter
compatibility witness target.
-/
def r1c_maximal_diameter_compatibility_witness_target_from_endpoint_diameter_realized
    (T : R1cNativeEndpointDiameterRealizedWitnessTarget) :
    R1cNativeMaximalDiameterCompatibilityWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  endpointDiameterRealized :=
    T.endpointDiameterRealized
  maximalEndpointDiameter :=
    T.maximalEndpointDiameter
  supportDiameterCompatible :=
    T.supportDiameterCompatible
  endpointDiameterWitness :=
    R1c_endpointDiameterRealized_from_witness_target T
  maximalEndpointWitness :=
    T.maximalEndpointWitness
  supportDiameterWitness :=
    T.supportDiameterWitness
  incompatibility :=
    T.incompatibility

end Frontier
end Chronos

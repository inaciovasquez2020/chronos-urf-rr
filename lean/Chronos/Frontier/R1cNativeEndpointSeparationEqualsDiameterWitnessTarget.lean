import Chronos.Frontier.R1cNativeEndpointDiameterRealizedWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c endpoint-separation-equals-diameter input.

This surface isolates the endpoint-separation equality component needed by the
endpoint-diameter-realized witness target. The measurement witnesses and the
rule converting them into endpoint-separation-equals-diameter remain explicit.
-/
structure R1cNativeEndpointSeparationEqualsDiameterWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  endpointSeparationMeasurement : Prop
  diameterMeasurement : Prop
  endpointSeparationEqualsDiameter : Prop
  endpointSeparationMeasurementWitness : endpointSeparationMeasurement
  diameterMeasurementWitness : diameterMeasurement
  endpointSeparationEqualsDiameterRule :
    endpointSeparationMeasurement →
      diameterMeasurement →
        endpointSeparationEqualsDiameter
  endpointDiameterRealized : Prop
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
The endpoint-separation-equals-diameter witness follows from explicit endpoint
separation and diameter measurement witnesses.
-/
theorem R1c_endpointSeparationEqualsDiameter_from_witness_target
    (T : R1cNativeEndpointSeparationEqualsDiameterWitnessTarget) :
    T.endpointSeparationEqualsDiameter :=
  T.endpointSeparationEqualsDiameterRule
    T.endpointSeparationMeasurementWitness
    T.diameterMeasurementWitness

/--
The endpoint-separation-equals-diameter witness target feeds the existing
endpoint-diameter-realized witness target.
-/
def r1c_endpoint_diameter_realized_witness_target_from_endpoint_separation_equals_diameter
    (T : R1cNativeEndpointSeparationEqualsDiameterWitnessTarget) :
    R1cNativeEndpointDiameterRealizedWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  endpointSeparationEqualsDiameter :=
    T.endpointSeparationEqualsDiameter
  endpointDiameterRealized :=
    T.endpointDiameterRealized
  endpointSeparationWitness :=
    R1c_endpointSeparationEqualsDiameter_from_witness_target T
  endpointDiameterRealizationRule :=
    T.endpointDiameterRealizationRule
  maximalEndpointDiameter :=
    T.maximalEndpointDiameter
  supportDiameterCompatible :=
    T.supportDiameterCompatible
  maximalEndpointWitness :=
    T.maximalEndpointWitness
  supportDiameterWitness :=
    T.supportDiameterWitness
  incompatibility :=
    T.incompatibility

end Frontier
end Chronos

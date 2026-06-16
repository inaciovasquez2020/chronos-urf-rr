import Chronos.Frontier.R1cNativeEndpointSeparationEqualsDiameterWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c endpoint-separation-measurement input.

This surface isolates the endpoint-separation measurement component needed by
the endpoint-separation-equals-diameter witness target. The native endpoint
input and the rule extracting the endpoint-separation measurement from it remain
explicit proof fields.
-/
structure R1cNativeEndpointSeparationMeasurementWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  nativeEndpointInput : Prop
  endpointSeparationMeasurement : Prop
  nativeEndpointInputWitness : nativeEndpointInput
  endpointSeparationMeasurementRule :
    nativeEndpointInput → endpointSeparationMeasurement
  diameterMeasurement : Prop
  endpointSeparationEqualsDiameter : Prop
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
The endpoint-separation measurement follows from the explicit native endpoint
input witness and measurement rule.
-/
theorem R1c_endpointSeparationMeasurement_from_witness_target
    (T : R1cNativeEndpointSeparationMeasurementWitnessTarget) :
    T.endpointSeparationMeasurement :=
  T.endpointSeparationMeasurementRule T.nativeEndpointInputWitness

/--
The endpoint-separation-measurement witness target feeds the existing
endpoint-separation-equals-diameter witness target.
-/
def r1c_endpoint_separation_equals_diameter_witness_target_from_endpoint_separation_measurement
    (T : R1cNativeEndpointSeparationMeasurementWitnessTarget) :
    R1cNativeEndpointSeparationEqualsDiameterWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  endpointSeparationMeasurement :=
    T.endpointSeparationMeasurement
  diameterMeasurement :=
    T.diameterMeasurement
  endpointSeparationEqualsDiameter :=
    T.endpointSeparationEqualsDiameter
  endpointSeparationMeasurementWitness :=
    R1c_endpointSeparationMeasurement_from_witness_target T
  diameterMeasurementWitness :=
    T.diameterMeasurementWitness
  endpointSeparationEqualsDiameterRule :=
    T.endpointSeparationEqualsDiameterRule
  endpointDiameterRealized :=
    T.endpointDiameterRealized
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

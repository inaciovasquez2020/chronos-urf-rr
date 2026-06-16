import Chronos.Frontier.R1cNativeEndpointSeparationMeasurementWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c native-endpoint-input component.

This surface isolates the native endpoint input needed by the
endpoint-separation-measurement witness target. The native endpoint
configuration, admissibility witness, and input extraction rule remain explicit.
-/
structure R1cNativeEndpointInputWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  nativeEndpointConfiguration : Prop
  nativeEndpointAdmissible : Prop
  nativeEndpointInput : Prop
  nativeEndpointConfigurationWitness : nativeEndpointConfiguration
  nativeEndpointAdmissibleWitness : nativeEndpointAdmissible
  nativeEndpointInputRule :
    nativeEndpointConfiguration →
      nativeEndpointAdmissible →
        nativeEndpointInput
  endpointSeparationMeasurement : Prop
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
The native endpoint input follows from the explicit native endpoint
configuration and admissibility witnesses.
-/
theorem R1c_nativeEndpointInput_from_witness_target
    (T : R1cNativeEndpointInputWitnessTarget) :
    T.nativeEndpointInput :=
  T.nativeEndpointInputRule
    T.nativeEndpointConfigurationWitness
    T.nativeEndpointAdmissibleWitness

/--
The native-endpoint-input witness target feeds the existing
endpoint-separation-measurement witness target.
-/
def r1c_endpoint_separation_measurement_witness_target_from_native_endpoint_input
    (T : R1cNativeEndpointInputWitnessTarget) :
    R1cNativeEndpointSeparationMeasurementWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  nativeEndpointInput :=
    T.nativeEndpointInput
  endpointSeparationMeasurement :=
    T.endpointSeparationMeasurement
  nativeEndpointInputWitness :=
    R1c_nativeEndpointInput_from_witness_target T
  endpointSeparationMeasurementRule :=
    T.endpointSeparationMeasurementRule
  diameterMeasurement :=
    T.diameterMeasurement
  endpointSeparationEqualsDiameter :=
    T.endpointSeparationEqualsDiameter
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

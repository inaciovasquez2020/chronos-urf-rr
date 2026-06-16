import Chronos.Frontier.R1cNativeEndpointInputWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c native-endpoint-configuration component.

This surface isolates the native endpoint configuration needed by the native
endpoint input witness target. The raw endpoint configuration source, geometry
anchor, and extraction rule remain explicit proof fields.
-/
structure R1cNativeEndpointConfigurationWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  nativeEndpointConfigurationSource : Prop
  nativeGeometryAnchor : Prop
  nativeEndpointConfiguration : Prop
  nativeEndpointConfigurationSourceWitness :
    nativeEndpointConfigurationSource
  nativeGeometryAnchorWitness :
    nativeGeometryAnchor
  nativeEndpointConfigurationRule :
    nativeEndpointConfigurationSource →
      nativeGeometryAnchor →
        nativeEndpointConfiguration
  nativeEndpointAdmissible : Prop
  nativeEndpointInput : Prop
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
The native endpoint configuration follows from the explicit source and geometry
anchor witnesses.
-/
theorem R1c_nativeEndpointConfiguration_from_witness_target
    (T : R1cNativeEndpointConfigurationWitnessTarget) :
    T.nativeEndpointConfiguration :=
  T.nativeEndpointConfigurationRule
    T.nativeEndpointConfigurationSourceWitness
    T.nativeGeometryAnchorWitness

/--
The native-endpoint-configuration witness target feeds the existing
native-endpoint-input witness target.
-/
def r1c_native_endpoint_input_witness_target_from_native_endpoint_configuration
    (T : R1cNativeEndpointConfigurationWitnessTarget) :
    R1cNativeEndpointInputWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  nativeEndpointConfiguration :=
    T.nativeEndpointConfiguration
  nativeEndpointAdmissible :=
    T.nativeEndpointAdmissible
  nativeEndpointInput :=
    T.nativeEndpointInput
  nativeEndpointConfigurationWitness :=
    R1c_nativeEndpointConfiguration_from_witness_target T
  nativeEndpointAdmissibleWitness :=
    T.nativeEndpointAdmissibleWitness
  nativeEndpointInputRule :=
    T.nativeEndpointInputRule
  endpointSeparationMeasurement :=
    T.endpointSeparationMeasurement
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

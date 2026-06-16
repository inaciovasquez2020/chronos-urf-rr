import Chronos.Frontier.R1cNativeEndpointConfigurationWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c native-endpoint-configuration-source
component.

This surface isolates the configuration source needed by the native endpoint
configuration witness target. The raw source witness and the rule extracting
the endpoint configuration source from it remain explicit proof fields.
-/
structure R1cNativeEndpointConfigurationSourceWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  rawEndpointConfigurationSource : Prop
  nativeEndpointConfigurationSource : Prop
  rawEndpointConfigurationSourceWitness :
    rawEndpointConfigurationSource
  nativeEndpointConfigurationSourceRule :
    rawEndpointConfigurationSource →
      nativeEndpointConfigurationSource
  nativeGeometryAnchor : Prop
  nativeEndpointConfiguration : Prop
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
The native endpoint configuration source follows from the explicit raw source
witness and source-extraction rule.
-/
theorem R1c_nativeEndpointConfigurationSource_from_witness_target
    (T : R1cNativeEndpointConfigurationSourceWitnessTarget) :
    T.nativeEndpointConfigurationSource :=
  T.nativeEndpointConfigurationSourceRule
    T.rawEndpointConfigurationSourceWitness

/--
The native-endpoint-configuration-source witness target feeds the existing
native-endpoint-configuration witness target.
-/
def r1c_native_endpoint_configuration_witness_target_from_configuration_source
    (T : R1cNativeEndpointConfigurationSourceWitnessTarget) :
    R1cNativeEndpointConfigurationWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  nativeEndpointConfigurationSource :=
    T.nativeEndpointConfigurationSource
  nativeGeometryAnchor :=
    T.nativeGeometryAnchor
  nativeEndpointConfiguration :=
    T.nativeEndpointConfiguration
  nativeEndpointConfigurationSourceWitness :=
    R1c_nativeEndpointConfigurationSource_from_witness_target T
  nativeGeometryAnchorWitness :=
    T.nativeGeometryAnchorWitness
  nativeEndpointConfigurationRule :=
    T.nativeEndpointConfigurationRule
  nativeEndpointAdmissible :=
    T.nativeEndpointAdmissible
  nativeEndpointInput :=
    T.nativeEndpointInput
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

import Chronos.Frontier.R1cNativeEndpointConfigurationSourceWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c raw-endpoint-configuration-source component.

This surface isolates the raw endpoint configuration source needed by the
native endpoint configuration source witness target. The base source witness
and extraction rule remain explicit proof fields.
-/
structure R1cNativeRawEndpointConfigurationSourceWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  rawEndpointConfigurationSourceBase : Prop
  rawEndpointConfigurationSource : Prop
  rawEndpointConfigurationSourceBaseWitness :
    rawEndpointConfigurationSourceBase
  rawEndpointConfigurationSourceRule :
    rawEndpointConfigurationSourceBase →
      rawEndpointConfigurationSource
  nativeEndpointConfigurationSource : Prop
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
The raw endpoint configuration source follows from the explicit base source
witness and extraction rule.
-/
theorem R1c_rawEndpointConfigurationSource_from_witness_target
    (T : R1cNativeRawEndpointConfigurationSourceWitnessTarget) :
    T.rawEndpointConfigurationSource :=
  T.rawEndpointConfigurationSourceRule
    T.rawEndpointConfigurationSourceBaseWitness

/--
The raw-endpoint-configuration-source witness target feeds the existing native
endpoint-configuration-source witness target.
-/
def r1c_native_endpoint_configuration_source_witness_target_from_raw_source
    (T : R1cNativeRawEndpointConfigurationSourceWitnessTarget) :
    R1cNativeEndpointConfigurationSourceWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  rawEndpointConfigurationSource :=
    T.rawEndpointConfigurationSource
  nativeEndpointConfigurationSource :=
    T.nativeEndpointConfigurationSource
  rawEndpointConfigurationSourceWitness :=
    R1c_rawEndpointConfigurationSource_from_witness_target T
  nativeEndpointConfigurationSourceRule :=
    T.nativeEndpointConfigurationSourceRule
  nativeGeometryAnchor :=
    T.nativeGeometryAnchor
  nativeEndpointConfiguration :=
    T.nativeEndpointConfiguration
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

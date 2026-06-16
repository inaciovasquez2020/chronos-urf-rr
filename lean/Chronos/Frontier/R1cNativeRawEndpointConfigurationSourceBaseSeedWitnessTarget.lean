import Chronos.Frontier.R1cNativeRawEndpointConfigurationSourceBaseWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c raw-endpoint-configuration-source-base-seed
component.

This surface isolates the seed witness needed by the raw endpoint configuration
source base witness target. The seed carrier and the rule extracting the base
seed from it remain explicit proof fields.
-/
structure R1cNativeRawEndpointConfigurationSourceBaseSeedWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  rawEndpointConfigurationSourceBaseSeedCarrier : Prop
  rawEndpointConfigurationSourceBaseSeed : Prop
  rawEndpointConfigurationSourceBaseSeedCarrierWitness :
    rawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeedRule :
    rawEndpointConfigurationSourceBaseSeedCarrier →
      rawEndpointConfigurationSourceBaseSeed
  rawEndpointConfigurationSourceBase : Prop
  rawEndpointConfigurationSourceBaseRule :
    rawEndpointConfigurationSourceBaseSeed →
      rawEndpointConfigurationSourceBase
  rawEndpointConfigurationSource : Prop
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
The raw endpoint configuration source base seed follows from the explicit seed
carrier witness and seed-extraction rule.
-/
theorem R1c_rawEndpointConfigurationSourceBaseSeed_from_witness_target
    (T : R1cNativeRawEndpointConfigurationSourceBaseSeedWitnessTarget) :
    T.rawEndpointConfigurationSourceBaseSeed :=
  T.rawEndpointConfigurationSourceBaseSeedRule
    T.rawEndpointConfigurationSourceBaseSeedCarrierWitness

/--
The raw-endpoint-configuration-source-base-seed witness target feeds the
existing raw-endpoint-configuration-source-base witness target.
-/
def r1c_raw_endpoint_configuration_source_base_witness_target_from_seed
    (T : R1cNativeRawEndpointConfigurationSourceBaseSeedWitnessTarget) :
    R1cNativeRawEndpointConfigurationSourceBaseWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  rawEndpointConfigurationSourceBaseSeed :=
    T.rawEndpointConfigurationSourceBaseSeed
  rawEndpointConfigurationSourceBase :=
    T.rawEndpointConfigurationSourceBase
  rawEndpointConfigurationSourceBaseSeedWitness :=
    R1c_rawEndpointConfigurationSourceBaseSeed_from_witness_target T
  rawEndpointConfigurationSourceBaseRule :=
    T.rawEndpointConfigurationSourceBaseRule
  rawEndpointConfigurationSource :=
    T.rawEndpointConfigurationSource
  rawEndpointConfigurationSourceRule :=
    T.rawEndpointConfigurationSourceRule
  nativeEndpointConfigurationSource :=
    T.nativeEndpointConfigurationSource
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

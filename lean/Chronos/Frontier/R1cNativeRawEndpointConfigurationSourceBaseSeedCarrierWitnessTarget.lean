import Chronos.Frontier.R1cNativeRawEndpointConfigurationSourceBaseSeedWitnessTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the concrete R1c
raw-endpoint-configuration-source-base-seed-carrier component.

This surface isolates the concrete seed-carrier witness needed by the
raw-endpoint-configuration-source-base-seed witness target. The concrete
carrier and the rule extracting the raw seed carrier from it remain explicit
proof fields.
-/
structure R1cNativeRawEndpointConfigurationSourceBaseSeedCarrierWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrier : Prop
  rawEndpointConfigurationSourceBaseSeedCarrier : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierWitness :
    concreteRawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeedCarrierRule :
    concreteRawEndpointConfigurationSourceBaseSeedCarrier →
      rawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeed : Prop
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
  nativeGeometryAnchorWitness : nativeGeometryAnchor
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
    nativeEndpointInput →
      endpointSeparationMeasurement
  diameterMeasurement : Prop
  endpointSeparationEqualsDiameter : Prop
  diameterMeasurementWitness : diameterMeasurement
  endpointSeparationEqualsDiameterRule :
    endpointSeparationMeasurement →
      diameterMeasurement →
        endpointSeparationEqualsDiameter
  endpointDiameterRealized : Prop
  endpointDiameterRealizationRule :
    endpointSeparationEqualsDiameter →
      endpointDiameterRealized
  maximalEndpointDiameter : Prop
  supportDiameterCompatible : Prop
  maximalEndpointWitness : maximalEndpointDiameter
  supportDiameterWitness : supportDiameterCompatible
  incompatibility :
    endpointDiameterRealized →
      maximalEndpointDiameter →
        supportDiameterCompatible →
          trivialLongChordAcrossMaximalDiameter →
            False

/--
The raw endpoint configuration source base seed carrier follows from the
explicit concrete carrier witness and carrier-extraction rule.
-/
theorem R1c_rawEndpointConfigurationSourceBaseSeedCarrier_from_witness_target
    (T : R1cNativeRawEndpointConfigurationSourceBaseSeedCarrierWitnessTarget) :
    T.rawEndpointConfigurationSourceBaseSeedCarrier :=
  T.rawEndpointConfigurationSourceBaseSeedCarrierRule
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierWitness

/--
The concrete raw-endpoint-configuration-source-base-seed-carrier witness target
feeds the existing raw-endpoint-configuration-source-base-seed witness target.
-/
def r1c_raw_endpoint_configuration_source_base_seed_witness_target_from_carrier
    (T : R1cNativeRawEndpointConfigurationSourceBaseSeedCarrierWitnessTarget) :
    R1cNativeRawEndpointConfigurationSourceBaseSeedWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  rawEndpointConfigurationSourceBaseSeedCarrier :=
    T.rawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeed :=
    T.rawEndpointConfigurationSourceBaseSeed
  rawEndpointConfigurationSourceBaseSeedCarrierWitness :=
    R1c_rawEndpointConfigurationSourceBaseSeedCarrier_from_witness_target T
  rawEndpointConfigurationSourceBaseSeedRule :=
    T.rawEndpointConfigurationSourceBaseSeedRule
  rawEndpointConfigurationSourceBase :=
    T.rawEndpointConfigurationSourceBase
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

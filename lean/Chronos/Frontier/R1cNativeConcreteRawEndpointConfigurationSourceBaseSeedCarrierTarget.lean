import Chronos.Frontier.R1cNativeRawEndpointConfigurationSourceBaseSeedCarrierWitnessTarget

namespace Chronos
namespace Frontier

/--
Native carrier target for the concrete R1c
raw-endpoint-configuration-source-base-seed-carrier component.

This surface isolates the concrete carrier needed by the
raw-endpoint-configuration-source-base-seed-carrier witness target. The
carrier source witness and the rule extracting the concrete carrier remain
explicit proof fields.
-/
structure R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSource : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrier : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceWitness :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSource
  concreteRawEndpointConfigurationSourceBaseSeedCarrierRule :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSource →
      concreteRawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeedCarrier : Prop
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
The concrete raw endpoint configuration source base seed carrier follows from
the explicit carrier source witness and carrier-extraction rule.
-/
theorem R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrier_from_target
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierTarget) :
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrier :=
  T.concreteRawEndpointConfigurationSourceBaseSeedCarrierRule
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceWitness

/--
The concrete raw-endpoint-configuration-source-base-seed-carrier target feeds
the existing seed-carrier witness target.
-/
def r1c_raw_endpoint_configuration_source_base_seed_carrier_witness_target_from_concrete_carrier
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierTarget) :
    R1cNativeRawEndpointConfigurationSourceBaseSeedCarrierWitnessTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  concreteRawEndpointConfigurationSourceBaseSeedCarrier :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeedCarrier :=
    T.rawEndpointConfigurationSourceBaseSeedCarrier
  concreteRawEndpointConfigurationSourceBaseSeedCarrierWitness :=
    R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrier_from_target T
  rawEndpointConfigurationSourceBaseSeedRule :=
    T.rawEndpointConfigurationSourceBaseSeedRule
  rawEndpointConfigurationSourceBaseSeed :=
    T.rawEndpointConfigurationSourceBaseSeed
  rawEndpointConfigurationSourceBaseSeedCarrierRule :=
    T.rawEndpointConfigurationSourceBaseSeedCarrierRule
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

import Chronos.Frontier.R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputTarget

namespace Chronos
namespace Frontier

structure R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceSeed : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceSeedWitness :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceSeed
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceRule :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceSeed →
      concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputRule :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource →
      concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSource : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceRule :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput →
      concreteRawEndpointConfigurationSourceBaseSeedCarrierSource
  concreteRawEndpointConfigurationSourceBaseSeedCarrier : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierRule :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSource →
      concreteRawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeedCarrier : Prop
  rawEndpointConfigurationSourceBaseSeedCarrierRule :
    concreteRawEndpointConfigurationSourceBaseSeedCarrier →
      rawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeed : Prop
  rawEndpointConfigurationSourceBaseSeedCarrierRule :
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

theorem R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource_from_target
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget) :
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource :=
  T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceRule
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceSeedWitness

def r1c_concrete_raw_endpoint_configuration_source_base_seed_carrier_source_input_target_from_source
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceTarget) :
    R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceWitness :=
    R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource_from_target T
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputRule :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputRule
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSource :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSource
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceRule :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceRule
  concreteRawEndpointConfigurationSourceBaseSeedCarrier :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrier
  concreteRawEndpointConfigurationSourceBaseSeedCarrierRule :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierRule
  rawEndpointConfigurationSourceBaseSeedCarrier :=
    T.rawEndpointConfigurationSourceBaseSeedCarrier
  rawEndpointConfigurationSourceBaseSeedCarrierRule :=
    T.rawEndpointConfigurationSourceBaseSeedCarrierRule
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

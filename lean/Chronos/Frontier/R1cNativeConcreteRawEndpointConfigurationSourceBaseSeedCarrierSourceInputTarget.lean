import Chronos.Frontier.R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceTarget

namespace Chronos
namespace Frontier

/--
Native input target for the concrete R1c
raw-endpoint-configuration-source-base-seed-carrier-source-input component.

This surface isolates the concrete source input needed by the concrete
raw-endpoint-configuration-source-base-seed-carrier-source target. The input
source witness and the rule extracting the concrete source input remain
explicit proof fields.
-/
structure R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceWitness :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSource
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
The concrete raw endpoint configuration source base seed carrier source input
follows from the explicit input source witness and input-extraction rule.
-/
theorem R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput_from_target
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputTarget) :
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput :=
  T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputRule
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputSourceWitness

/--
The concrete raw-endpoint-configuration-source-base-seed-carrier-source-input
target feeds the existing concrete carrier source target.
-/
def r1c_concrete_raw_endpoint_configuration_source_base_seed_carrier_source_target_from_input
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputTarget) :
    R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSource :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSource
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputWitness :=
    R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput_from_target T
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceRule :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceRule
  concreteRawEndpointConfigurationSourceBaseSeedCarrier :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrier
  concreteRawEndpointConfigurationSourceBaseSeedCarrierRule :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierRule
  rawEndpointConfigurationSourceBaseSeedCarrier :=
    T.rawEndpointConfigurationSourceBaseSeedCarrier
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

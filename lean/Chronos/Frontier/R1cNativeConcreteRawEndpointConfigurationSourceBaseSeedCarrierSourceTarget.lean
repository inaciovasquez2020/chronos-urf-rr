import Chronos.Frontier.R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierTarget

namespace Chronos
namespace Frontier

/--
Native source target for the concrete R1c
raw-endpoint-configuration-source-base-seed-carrier-source component.

This surface isolates the concrete carrier source needed by the
concrete raw-endpoint-configuration-source-base-seed-carrier target. The
source input witness and the rule extracting the concrete source remain
explicit proof fields.
-/
structure R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSource : Prop
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputWitness :
    concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInput
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

/--
The concrete raw endpoint configuration source base seed carrier source follows
from the explicit source input witness and source-extraction rule.
-/
theorem R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrierSource_from_target
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceTarget) :
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSource :=
  T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceRule
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceInputWitness

/--
The concrete raw-endpoint-configuration-source-base-seed-carrier-source target
feeds the existing concrete carrier target.
-/
def r1c_concrete_raw_endpoint_configuration_source_base_seed_carrier_target_from_source
    (T : R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierSourceTarget) :
    R1cNativeConcreteRawEndpointConfigurationSourceBaseSeedCarrierTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSource :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrierSource
  concreteRawEndpointConfigurationSourceBaseSeedCarrier :=
    T.concreteRawEndpointConfigurationSourceBaseSeedCarrier
  concreteRawEndpointConfigurationSourceBaseSeedCarrierSourceWitness :=
    R1c_concreteRawEndpointConfigurationSourceBaseSeedCarrierSource_from_target T
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

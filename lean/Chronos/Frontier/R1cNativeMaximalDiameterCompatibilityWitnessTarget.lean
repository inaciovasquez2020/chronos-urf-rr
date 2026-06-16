import Chronos.Frontier.R1cNativeTrivialLongChordIncompatibilityTarget

namespace Chronos
namespace Frontier

/--
Native witness target for the R1c maximal-diameter compatibility input.

This surface does not prove the geometric incompatibility itself. It isolates
the compatibility witness that the incompatibility target needs: endpoint
diameter realization, maximal endpoint diameter, and support-diameter
compatibility are bundled as explicit proof fields.
-/
structure R1cNativeMaximalDiameterCompatibilityWitnessTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  endpointDiameterRealized : Prop
  maximalEndpointDiameter : Prop
  supportDiameterCompatible : Prop
  endpointDiameterWitness : endpointDiameterRealized
  maximalEndpointWitness : maximalEndpointDiameter
  supportDiameterWitness : supportDiameterCompatible
  incompatibility :
    endpointDiameterRealized →
      maximalEndpointDiameter →
        supportDiameterCompatible →
          trivialLongChordAcrossMaximalDiameter → False

/--
The bundled native witnesses produce the compatibility proposition needed by
the previous incompatibility target.
-/
def R1c_maximalDiameterCompatibility_from_witness_target
    (T : R1cNativeMaximalDiameterCompatibilityWitnessTarget) : Prop :=
  T.endpointDiameterRealized ∧
    T.maximalEndpointDiameter ∧
      T.supportDiameterCompatible

/--
The compatibility witness is explicit: all three components are fields of the
target object.
-/
theorem R1c_maximalDiameterCompatibility_witness
    (T : R1cNativeMaximalDiameterCompatibilityWitnessTarget) :
    R1c_maximalDiameterCompatibility_from_witness_target T :=
  ⟨T.endpointDiameterWitness,
    T.maximalEndpointWitness,
    T.supportDiameterWitness⟩

/--
A compatibility witness target feeds the existing R1c incompatibility target.
-/
def r1c_trivial_long_chord_incompatibility_target_from_compatibility_witness
    (T : R1cNativeMaximalDiameterCompatibilityWitnessTarget) :
    R1cNativeTrivialLongChordIncompatibilityTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  maximalDiameterCompatibility :=
    R1c_maximalDiameterCompatibility_from_witness_target T
  compatibility :=
    R1c_maximalDiameterCompatibility_witness T
  incompatibility := by
    intro hCompatibility hTrivial
    exact T.incompatibility
      hCompatibility.1
      hCompatibility.2.1
      hCompatibility.2.2
      hTrivial

end Frontier
end Chronos

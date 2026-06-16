import Chronos.Frontier.R1cNativeMaximalSeparationExclusionTarget

namespace Chronos
namespace Frontier

/--
Native no-trivial-long-chord target for the final explicit R1c input.

This is an interface surface only.  It isolates the remaining native ingredient:
a verified exclusion of a trivial long chord across the maximal diameter.
-/
structure R1cNativeNoTrivialLongChordAcrossMaximalDiameterTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  noTrivialLongChordAcrossMaximalDiameter : Prop
  excludesTrivialLongChordAcrossMaximalDiameter :
    (trivialLongChordAcrossMaximalDiameter → False) →
      noTrivialLongChordAcrossMaximalDiameter

/--
The final no-trivial-long-chord input is supplied once the native target proves
that a trivial long chord across the maximal diameter is impossible.
-/
theorem R1c_noTrivialLongChordAcrossMaximalDiameter_from_native_target
    (T : R1cNativeNoTrivialLongChordAcrossMaximalDiameterTarget)
    (hExcluded : T.trivialLongChordAcrossMaximalDiameter → False) :
    T.noTrivialLongChordAcrossMaximalDiameter :=
  T.excludesTrivialLongChordAcrossMaximalDiameter hExcluded

/--
The no-trivial-long-chord target feeds the existing maximal-separation
final-exclusion target while keeping the actual contradiction proof explicit.
-/
def r1c_maximal_separation_exclusion_target_from_no_trivial_long_chord_target
    (T : R1cNativeNoTrivialLongChordAcrossMaximalDiameterTarget)
    (endpointSeparationEqualsDiameter : Prop)
    (maximalEndpointSeparation : Prop)
    (supportDiameterBridge : Prop)
    (finalR1cExclusion :
      endpointSeparationEqualsDiameter →
        maximalEndpointSeparation →
          supportDiameterBridge →
            T.noTrivialLongChordAcrossMaximalDiameter →
              R1ConcreteNewsteinFGLGeometrySourceObject.R1c_maximalSeparationForbidsTrivialLongChord) :
    R1cNativeMaximalSeparationExclusionTarget where
  endpointSeparationEqualsDiameter :=
    endpointSeparationEqualsDiameter
  maximalEndpointSeparation :=
    maximalEndpointSeparation
  supportDiameterBridge :=
    supportDiameterBridge
  noTrivialLongChordAcrossMaximalDiameter :=
    T.noTrivialLongChordAcrossMaximalDiameter
  finalR1cExclusion :=
    finalR1cExclusion

end Frontier
end Chronos

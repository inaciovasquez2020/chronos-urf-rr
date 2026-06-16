import Chronos.Frontier.R1cNativeSupportDiameterBridgeTarget

namespace Chronos
namespace Frontier

/--
Native maximal-separation and final-exclusion target for the remaining R1c
interface input.

This is an interface surface only.  It isolates the final native ingredient
after the support-diameter bridge target: maximal endpoint separation, together
with endpoint-diameter equality and the support-diameter bridge, excludes a
trivial long chord across the maximal diameter.
-/
structure R1cNativeMaximalSeparationExclusionTarget where
  endpointSeparationEqualsDiameter : Prop
  maximalEndpointSeparation : Prop
  supportDiameterBridge : Prop
  noTrivialLongChordAcrossMaximalDiameter : Prop
  finalR1cExclusion :
    endpointSeparationEqualsDiameter →
      maximalEndpointSeparation →
        supportDiameterBridge →
          noTrivialLongChordAcrossMaximalDiameter →
            R1ConcreteNewsteinFGLGeometrySourceObject.R1c_maximalSeparationForbidsTrivialLongChord

/--
The final R1c exclusion is supplied once the maximal-separation target receives
endpoint-diameter equality, maximal endpoint separation, the support-diameter
bridge, and the explicit no-trivial-long-chord exclusion input.
-/
theorem R1c_final_exclusion_from_native_maximal_separation_target
    (T : R1cNativeMaximalSeparationExclusionTarget)
    (hEndpoint : T.endpointSeparationEqualsDiameter)
    (hMaximal : T.maximalEndpointSeparation)
    (hSupportDiameter : T.supportDiameterBridge)
    (hNoTrivial : T.noTrivialLongChordAcrossMaximalDiameter) :
    R1ConcreteNewsteinFGLGeometrySourceObject.R1c_maximalSeparationForbidsTrivialLongChord :=
  T.finalR1cExclusion hEndpoint hMaximal hSupportDiameter hNoTrivial

/--
A maximal-separation final-exclusion target feeds the existing R1c native
Newstein/FGL interface target while keeping the no-trivial-long-chord exclusion
input explicit.
-/
def r1c_native_interface_from_maximal_separation_exclusion_target
    (T : R1cNativeMaximalSeparationExclusionTarget)
    (hNoTrivial : T.noTrivialLongChordAcrossMaximalDiameter) :
    R1cNativeNewsteinFGLInterfaceTarget where
  endpointSeparationEqualsDiameter :=
    T.endpointSeparationEqualsDiameter
  maximalEndpointSeparation :=
    T.maximalEndpointSeparation
  supportDiameterBridge :=
    T.supportDiameterBridge
  maximalSeparationExcludesTrivialLongChord := by
    intro hEndpoint hMaximal hSupportDiameter
    exact T.finalR1cExclusion
      hEndpoint hMaximal hSupportDiameter hNoTrivial

end Frontier
end Chronos

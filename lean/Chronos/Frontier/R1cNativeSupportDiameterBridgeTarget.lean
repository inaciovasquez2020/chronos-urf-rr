import Chronos.Frontier.R1cNativeNewsteinFGLInterfaceTarget

namespace Chronos
namespace Frontier

/--
Native support-diameter bridge target for the remaining R1c interface input.

This is an interface surface only.  It isolates the next missing native
ingredient: a proof that containing the distinguished endpoint forces the
relevant support diameter obstruction needed by the R1c native interface.
-/
structure R1cNativeSupportDiameterBridgeTarget where
  endpointContainedInSupport : Prop
  supportDiameterAtLeastEndpointSeparation : Prop
  endpointSeparationEqualsDiameter : Prop
  supportDiameterBridge : Prop
  supportDiameterBridge_from_native_support :
    endpointContainedInSupport →
      supportDiameterAtLeastEndpointSeparation →
        endpointSeparationEqualsDiameter →
          supportDiameterBridge

/--
The support-diameter bridge is supplied once the native containment,
support-diameter lower bound, and endpoint-diameter equality inputs are supplied.
-/
theorem R1c_supportDiameterBridge_from_native_support_target
    (B : R1cNativeSupportDiameterBridgeTarget)
    (hContained : B.endpointContainedInSupport)
    (hSupportLower : B.supportDiameterAtLeastEndpointSeparation)
    (hEndpointDiameter : B.endpointSeparationEqualsDiameter) :
    B.supportDiameterBridge :=
  B.supportDiameterBridge_from_native_support
    hContained hSupportLower hEndpointDiameter

/--
A support-diameter bridge target can feed the existing R1c native Newstein/FGL
interface target while keeping maximal separation and the final exclusion rule
explicit.
-/
def r1c_native_interface_from_support_diameter_bridge_target
    (B : R1cNativeSupportDiameterBridgeTarget)
    (maximalEndpointSeparation : Prop)
    (maximalSeparationExcludesTrivialLongChord :
      {sourceObject : R1ConcreteNewsteinFGLGeometrySourceObject} →
        B.endpointSeparationEqualsDiameter →
          maximalEndpointSeparation →
            B.supportDiameterBridge →
              R1ConcreteNewsteinFGLGeometrySourceObject.R1c_maximalSeparationForbidsTrivialLongChord sourceObject) :
    R1cNativeNewsteinFGLInterfaceTarget where
  endpointSeparationEqualsDiameter :=
    B.endpointSeparationEqualsDiameter
  maximalEndpointSeparation :=
    maximalEndpointSeparation
  supportDiameterBridge :=
    B.supportDiameterBridge
  maximalSeparationExcludesTrivialLongChord :=
    maximalSeparationExcludesTrivialLongChord

end Frontier
end Chronos

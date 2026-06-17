import Chronos.Frontier.R1ConcreteNewsteinFGLGeometrySourceObject

namespace Chronos
namespace Frontier

/--
Verified native Newstein/FGL interface target for the remaining R1c source
field.

This is an interface surface only.  It records the weakest repository-native
ingredients identified by the existing R1c reduction scan: endpoint separation
equals the diameter, endpoint separation is maximal, and a support-diameter
bridge converts containment of the distinguished endpoint into the relevant
diameter obstruction.
-/
structure R1cNativeNewsteinFGLInterfaceTarget where
  endpointSeparationEqualsDiameter : Prop
  maximalEndpointSeparation : Prop
  supportDiameterBridge : Prop
  maximalSeparationExcludesTrivialLongChord :
    endpointSeparationEqualsDiameter →
      maximalEndpointSeparation →
        supportDiameterBridge →
          R1ConcreteNewsteinFGLGeometrySourceObject.R1c_maximalSeparationForbidsTrivialLongChord sourceObject

/--
The R1c source field is supplied once the verified native Newstein/FGL interface
target supplies the endpoint-separation, maximality, and support-diameter
bridge ingredients.
-/
theorem R1c_maximalSeparationForbidsTrivialLongChord_from_native_interface
    (sourceObject : R1ConcreteNewsteinFGLGeometrySourceObject)
    (I : R1cNativeNewsteinFGLInterfaceTarget)
    (hEndpoint : I.endpointSeparationEqualsDiameter)
    (hMaximal : I.maximalEndpointSeparation)
    (hSupportDiameter : I.supportDiameterBridge) :
    R1ConcreteNewsteinFGLGeometrySourceObject.R1c_maximalSeparationForbidsTrivialLongChord sourceObject :=
  I.maximalSeparationExcludesTrivialLongChord hEndpoint hMaximal hSupportDiameter

/--
A concrete source object can be assembled from the remaining verified R1c native
interface target.  R1a and R1b are already discharged by the concrete safe
semantic data.
-/
def r1_concrete_newstein_fgl_source_object_from_r1c_native_interface
    (I : R1cNativeNewsteinFGLInterfaceTarget)
    (hEndpoint : I.endpointSeparationEqualsDiameter)
    (_hMaximal : I.maximalEndpointSeparation)
    (_hSupportDiameter : I.supportDiameterBridge) :
    R1ConcreteNewsteinFGLGeometrySourceObject where
  R1c_maximalSeparationForbidsTrivialLongChord :=
    I.endpointSeparationEqualsDiameter
  R1c_supplied :=
    hEndpoint

end Frontier
end Chronos

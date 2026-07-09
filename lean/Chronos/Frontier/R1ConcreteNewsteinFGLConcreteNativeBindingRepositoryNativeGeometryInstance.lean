import Chronos.Frontier.R1ConcreteNewsteinFGLConcreteNativeBindingToRepositoryNativeGeometryTarget
import Chronos.Frontier.R1cNativeNewsteinFGLInterfaceTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput where
  interface : R1cNativeNewsteinFGLInterfaceTarget
  endpoint : interface.endpointSeparationEqualsDiameter
  maximal : interface.maximalEndpointSeparation
  supportDiameter : interface.supportDiameterBridge

def R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput.source
    (x : R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput) :
    R1ConcreteNewsteinFGLGeometrySourceObject :=
  r1_concrete_newstein_fgl_source_object_from_r1c_native_interface
    x.interface
    x.endpoint
    x.maximal
    x.supportDiameter

def R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput.toTarget
    (x : R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput) :
    R1ConcreteNewsteinFGLConcreteNativeBindingToRepositoryNativeGeometryTarget
      concreteNativeR1SemanticData where
  source := x.source
  binding := concreteNativeBindingSpec
  binding_supplied := concrete_native_binding_supplied
  binding_r1_data_matches := rfl

def R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput.toRepositoryNativeGeometry
    (x : R1ConcreteNewsteinFGLConcreteNativeBindingRepositoryNativeGeometryInstanceInput) :
    R1ConcreteNewsteinFGLRepositoryNativeGeometry concreteNativeR1SemanticData :=
  x.toTarget.toRepositoryNativeGeometry

def r1_concrete_newstein_fgl_concrete_native_binding_repository_native_geometry_instance_boundary : String :=
  "NO_CONCRETE_NATIVE_BINDING_REPOSITORY_NATIVE_GEOMETRY_INSTANCE_INPUT"

end Frontier
end Chronos

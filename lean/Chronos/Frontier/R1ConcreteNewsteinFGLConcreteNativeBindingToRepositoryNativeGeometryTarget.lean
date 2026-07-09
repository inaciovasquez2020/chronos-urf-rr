import Chronos.Frontier.ConcreteNativeBindingSpec
import Chronos.Frontier.R1ConcreteNewsteinFGLRepositoryNativeGeometryToNativeNonAliasDataTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLConcreteNativeBindingToRepositoryNativeGeometryTarget
    (D : R1SemanticData) : Sort _ where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  binding : NewsteinR1R2R3NativeBindingSpec
  binding_supplied : NewsteinR1R2R3NativeBindingSupplied binding
  binding_r1_data_matches : binding.nativeR1Data = D

def R1ConcreteNewsteinFGLConcreteNativeBindingToRepositoryNativeGeometryTarget.toRepositoryNativeGeometry
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLConcreteNativeBindingToRepositoryNativeGeometryTarget D) :
    R1ConcreteNewsteinFGLRepositoryNativeGeometry D where
  source := x.source
  repository_native_geometry_evidence :=
    NewsteinR1R2R3NativeBindingSupplied x.binding ∧ x.binding.nativeR1Data = D
  repository_native_geometry_supplied :=
    ⟨x.binding_supplied, x.binding_r1_data_matches⟩

def r1_concrete_newstein_fgl_concrete_native_binding_to_repository_native_geometry_boundary : String :=
  "NO_CONCRETE_NATIVE_BINDING_TO_REPOSITORY_NATIVE_GEOMETRY_INSTANCE"

end Frontier
end Chronos

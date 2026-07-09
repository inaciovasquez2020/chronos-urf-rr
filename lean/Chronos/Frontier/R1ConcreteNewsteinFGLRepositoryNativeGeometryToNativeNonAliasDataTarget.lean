import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataR1LongChordTheoremRouteTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLRepositoryNativeGeometry
    (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  repository_native_geometry_evidence : Prop
  repository_native_geometry_supplied : repository_native_geometry_evidence

structure R1ConcreteNewsteinFGLRepositoryNativeGeometryToNativeNonAliasDataTarget
    (D : R1SemanticData) : Type where
  geometry : R1ConcreteNewsteinFGLRepositoryNativeGeometry D
  native_non_alias_evidence : Prop
  native_non_alias_supplied : native_non_alias_evidence

def R1ConcreteNewsteinFGLRepositoryNativeGeometryToNativeNonAliasDataTarget.toNativeNonAliasData
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLRepositoryNativeGeometryToNativeNonAliasDataTarget D) :
    R1ConcreteNewsteinFGLNativeNonAliasData D where
  source := x.geometry.source
  native_non_alias_evidence := x.native_non_alias_evidence
  native_non_alias_supplied := x.native_non_alias_supplied

def r1_concrete_newstein_fgl_repository_native_geometry_to_native_non_alias_data_boundary : String :=
  "NO_REPOSITORY_NATIVE_GEOMETRY_TO_NATIVE_NON_ALIAS_DATA_INSTANCE"

end Frontier
end Chronos

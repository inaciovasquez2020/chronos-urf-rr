import Chronos.Frontier.R1ConcreteNewsteinFGLRepositoryNativeGeometryR1TheoremRouteTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget
    (D : R1SemanticData) : Type where
  repository_route :
    R1ConcreteNewsteinFGLRepositoryNativeGeometryToNativeNonAliasDataTarget D
  r1a :
    R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget D
  r1b :
    R1ConcreteNewsteinFGLNativeNonAliasDataToR1bInputFieldTarget D
  r1c :
    R1ConcreteNewsteinFGLNativeNonAliasDataToR1cInputFieldTarget D

def R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget.toRepositoryNativeGeometryR1Route
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget D) :
    R1ConcreteNewsteinFGLRepositoryNativeGeometryR1TheoremRouteTarget D where
  repository_to_native_non_alias := x.repository_route
  native_non_alias_r1_route := {
    r1a := x.r1a
    r1b := x.r1b
    r1c := x.r1c
  }

def r1_concrete_newstein_fgl_repository_native_geometry_full_input_contract_boundary : String :=
  "NO_REPOSITORY_NATIVE_GEOMETRY_FULL_R1_INPUT_CONTRACT_INSTANCE"

end Frontier
end Chronos

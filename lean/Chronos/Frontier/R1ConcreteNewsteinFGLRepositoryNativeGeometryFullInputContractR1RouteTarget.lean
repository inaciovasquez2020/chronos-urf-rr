import Chronos.Frontier.R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget

namespace Chronos
namespace Frontier

theorem R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget.toR1LongChordExclusionTheorem
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLRepositoryNativeGeometryFullInputContractTarget D) :
    R1LongChordExclusionTheorem D :=
  x.toRepositoryNativeGeometryR1Route.toR1LongChordExclusionTheorem

def r1_concrete_newstein_fgl_repository_native_geometry_full_input_contract_r1_route_boundary : String :=
  "NO_REPOSITORY_NATIVE_GEOMETRY_FULL_R1_INPUT_CONTRACT_ROUTE_INSTANCE"

end Frontier
end Chronos

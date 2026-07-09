import Chronos.Frontier.R1ConcreteNewsteinFGLRepositoryNativeGeometryToNativeNonAliasDataTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataR1LongChordTheoremRouteTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLRepositoryNativeGeometryR1TheoremRouteTarget
    (D : R1SemanticData) : Type where
  repository_to_native_non_alias :
    R1ConcreteNewsteinFGLRepositoryNativeGeometryToNativeNonAliasDataTarget D
  native_non_alias_r1_route :
    R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget D

theorem R1ConcreteNewsteinFGLRepositoryNativeGeometryR1TheoremRouteTarget.toR1LongChordExclusionTheorem
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLRepositoryNativeGeometryR1TheoremRouteTarget D) :
    R1LongChordExclusionTheorem D :=
  x.native_non_alias_r1_route.toR1LongChordExclusionTheorem

def r1_concrete_newstein_fgl_repository_native_geometry_r1_theorem_route_boundary : String :=
  "NO_REPOSITORY_NATIVE_GEOMETRY_R1_THEOREM_ROUTE_INSTANCE"

end Frontier
end Chronos

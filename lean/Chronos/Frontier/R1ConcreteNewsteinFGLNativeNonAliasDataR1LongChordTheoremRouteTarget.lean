import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1LongChordTheoremRouteTarget

namespace Chronos
namespace Frontier

theorem R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget.toR1LongChordExclusionTheorem
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget D) :
    R1LongChordExclusionTheorem D :=
  x.toNativeMapAssembly.toR1LongChordExclusionTheorem

def r1_concrete_newstein_fgl_native_non_alias_data_r1_long_chord_theorem_route_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_DATA_R1_LONG_CHORD_THEOREM_ROUTE_INSTANCE"

end Frontier
end Chronos

import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget

namespace Chronos
namespace Frontier

theorem R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget.toR1LongChordExclusionTheorem
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget D) :
    R1LongChordExclusionTheorem D :=
  R1_LongChordExclusion_from_semantic_inputs D x.toR1TheoremProofInputs

def r1_concrete_newstein_fgl_to_native_map_r1_long_chord_theorem_route_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_R1_LONG_CHORD_THEOREM_ROUTE_INSTANCE"

end Frontier
end Chronos

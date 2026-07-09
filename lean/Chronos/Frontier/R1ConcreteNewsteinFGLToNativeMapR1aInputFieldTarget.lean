import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLToNativeMapR1aInputFieldTarget
    (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  R1a_trivialFaceBoundariesAvoidLongChords :
    ∀ face, D.TrivFace face →
      ¬ D.FaceBoundarySupport face D.e1 ∧
      ¬ D.FaceBoundarySupport face D.e2

def r1_concrete_newstein_fgl_to_native_map_r1a_input_field_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_R1A_INPUT_FIELD"

end Frontier
end Chronos

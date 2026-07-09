import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLToNativeMapR1bInputFieldTarget
    (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  R1b_trivialWordSupportComesFromTrivialFaces :
    ∀ word edge, D.TrivWord word → D.WordSupport word edge →
      ∃ face, D.TrivFace face ∧ D.FaceBoundarySupport face edge

def r1_concrete_newstein_fgl_to_native_map_r1b_input_field_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_R1B_INPUT_FIELD"

end Frontier
end Chronos

import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1bInputFieldTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLNativeNonAliasDataToR1bInputFieldTarget
    (D : R1SemanticData) : Type where
  data : R1ConcreteNewsteinFGLNativeNonAliasData D
  R1b_trivialWordSupportComesFromTrivialFaces :
    ∀ word edge, D.TrivWord word → D.WordSupport word edge →
      ∃ face, D.TrivFace face ∧ D.FaceBoundarySupport face edge

def R1ConcreteNewsteinFGLNativeNonAliasDataToR1bInputFieldTarget.toR1bInputField
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLNativeNonAliasDataToR1bInputFieldTarget D) :
    R1ConcreteNewsteinFGLToNativeMapR1bInputFieldTarget D where
  source := x.data.source
  R1b_trivialWordSupportComesFromTrivialFaces :=
    x.R1b_trivialWordSupportComesFromTrivialFaces

def r1_concrete_newstein_fgl_native_non_alias_data_to_r1b_input_field_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_DATA_TO_R1B_INPUT_FIELD_INSTANCE"

end Frontier
end Chronos

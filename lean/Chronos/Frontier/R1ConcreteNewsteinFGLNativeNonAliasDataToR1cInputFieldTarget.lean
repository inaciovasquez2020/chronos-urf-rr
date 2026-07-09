import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1cInputFieldTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLNativeNonAliasDataToR1cInputFieldTarget
    (D : R1SemanticData) : Type where
  data : R1ConcreteNewsteinFGLNativeNonAliasData D
  R1c_maximalSeparationForbidsTrivialLongChord : Prop
  R1c_supplied : R1c_maximalSeparationForbidsTrivialLongChord

def R1ConcreteNewsteinFGLNativeNonAliasDataToR1cInputFieldTarget.toR1cInputField
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLNativeNonAliasDataToR1cInputFieldTarget D) :
    R1ConcreteNewsteinFGLToNativeMapR1cInputFieldTarget D where
  source := x.data.source
  R1c_maximalSeparationForbidsTrivialLongChord :=
    x.R1c_maximalSeparationForbidsTrivialLongChord
  R1c_supplied := x.R1c_supplied

def r1_concrete_newstein_fgl_native_non_alias_data_to_r1c_input_field_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_DATA_TO_R1C_INPUT_FIELD_INSTANCE"

end Frontier
end Chronos

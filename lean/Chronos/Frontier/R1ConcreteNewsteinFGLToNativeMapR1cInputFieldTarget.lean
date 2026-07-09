import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLToNativeMapR1cInputFieldTarget
    (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  R1c_maximalSeparationForbidsTrivialLongChord : Prop
  R1c_supplied : R1c_maximalSeparationForbidsTrivialLongChord

def r1_concrete_newstein_fgl_to_native_map_r1c_input_field_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_R1C_INPUT_FIELD"

end Frontier
end Chronos

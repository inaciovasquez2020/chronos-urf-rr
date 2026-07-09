import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1aInputFieldTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLNativeNonAliasData
    (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  native_non_alias_evidence : Prop
  native_non_alias_supplied : native_non_alias_evidence

structure R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget
    (D : R1SemanticData) : Type where
  data : R1ConcreteNewsteinFGLNativeNonAliasData D
  R1a_trivialFaceBoundariesAvoidLongChords :
    ∀ face, D.TrivFace face →
      ¬ D.FaceBoundarySupport face D.e1 ∧
      ¬ D.FaceBoundarySupport face D.e2

def R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget.toR1aInputField
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget D) :
    R1ConcreteNewsteinFGLToNativeMapR1aInputFieldTarget D where
  source := x.data.source
  R1a_trivialFaceBoundariesAvoidLongChords :=
    x.R1a_trivialFaceBoundariesAvoidLongChords

def r1_concrete_newstein_fgl_native_non_alias_data_to_r1a_input_field_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_DATA_TO_R1A_INPUT_FIELD_INSTANCE"

end Frontier
end Chronos

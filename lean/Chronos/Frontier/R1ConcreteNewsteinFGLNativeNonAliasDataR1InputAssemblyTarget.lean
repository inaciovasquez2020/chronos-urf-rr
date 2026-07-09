import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataToR1bInputFieldTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLNativeNonAliasDataToR1cInputFieldTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget
    (D : R1SemanticData) : Type where
  r1a : R1ConcreteNewsteinFGLNativeNonAliasDataToR1aInputFieldTarget D
  r1b : R1ConcreteNewsteinFGLNativeNonAliasDataToR1bInputFieldTarget D
  r1c : R1ConcreteNewsteinFGLNativeNonAliasDataToR1cInputFieldTarget D

def R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget.toNativeMapAssembly
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLNativeNonAliasDataR1InputAssemblyTarget D) :
    R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget D where
  source := x.r1a.data.source
  r1a := x.r1a.toR1aInputField
  r1b := x.r1b.toR1bInputField
  r1c := x.r1c.toR1cInputField

def r1_concrete_newstein_fgl_native_non_alias_data_r1_input_assembly_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_DATA_R1_INPUT_ASSEMBLY_INSTANCE"

end Frontier
end Chronos

import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1aInputFieldTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1bInputFieldTarget
import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1cInputFieldTarget

namespace Chronos
namespace Frontier

structure R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget
    (D : R1SemanticData) : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1a : R1ConcreteNewsteinFGLToNativeMapR1aInputFieldTarget D
  r1b : R1ConcreteNewsteinFGLToNativeMapR1bInputFieldTarget D
  r1c : R1ConcreteNewsteinFGLToNativeMapR1cInputFieldTarget D

def R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget.toR1TheoremProofInputs
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget D) :
    R1TheoremProofInputs D where
  R1a_trivialFaceBoundariesAvoidLongChords :=
    x.r1a.R1a_trivialFaceBoundariesAvoidLongChords
  R1b_trivialWordSupportComesFromTrivialFaces :=
    x.r1b.R1b_trivialWordSupportComesFromTrivialFaces
  R1c_maximalSeparationForbidsTrivialLongChord :=
    x.r1c.R1c_maximalSeparationForbidsTrivialLongChord
  R1c_supplied := x.r1c.R1c_supplied

def r1_concrete_newstein_fgl_to_native_map_r1_input_assembly_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_R1_INPUT_ASSEMBLY_INSTANCE"

end Frontier
end Chronos

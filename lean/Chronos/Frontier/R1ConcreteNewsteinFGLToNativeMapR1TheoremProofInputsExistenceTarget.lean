import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget

namespace Chronos
namespace Frontier

theorem R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget.toR1TheoremProofInputsExists
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLToNativeMapR1InputAssemblyTarget D) :
    Nonempty (R1TheoremProofInputs D) :=
  ⟨x.toR1TheoremProofInputs⟩

def r1_concrete_newstein_fgl_to_native_map_r1_theorem_proof_inputs_existence_boundary : String :=
  "NO_NATIVE_NON_ALIAS_NEWSTEIN_FGL_R1_THEOREM_PROOF_INPUTS_EXISTENCE_INSTANCE"

end Frontier
end Chronos

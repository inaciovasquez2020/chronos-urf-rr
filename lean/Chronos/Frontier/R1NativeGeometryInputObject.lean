import Chronos.Frontier.R1NativeInputBridge

namespace Chronos
namespace Frontier

/--
Boundary marker for the next missing native R1 geometry input object.

This is only an alias surface for the already existing `R1TheoremProofInputs`
input package. It does not construct such inputs from concrete Newstein/FGL
geometry.
-/
abbrev R1NativeGeometryInputObject (D : R1SemanticData) := R1TheoremProofInputs D

/--
The native geometry input object surface feeds the existing R1 theorem proof
input package.
-/
def r1_native_geometry_input_object_to_r1_theorem_proof_inputs
    {D : R1SemanticData}
    (x : R1NativeGeometryInputObject D) : R1TheoremProofInputs D :=
  x

/--
The existing R1 theorem proof input package is the current native geometry input
object surface.
-/
def r1_theorem_proof_inputs_to_r1_native_geometry_input_object
    {D : R1SemanticData}
    (x : R1TheoremProofInputs D) : R1NativeGeometryInputObject D :=
  x

end Frontier
end Chronos

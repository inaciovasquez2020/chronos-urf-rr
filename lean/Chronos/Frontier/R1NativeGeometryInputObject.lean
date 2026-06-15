import Chronos.Frontier.R1NativeInputBridge

/--
Boundary marker for the next missing native R1 geometry input object.

This is only an alias surface for the already existing `R1TheoremProofInputs`
input package. It does not construct such inputs from concrete Newstein/FGL
geometry.
-/
abbrev R1NativeGeometryInputObject := R1TheoremProofInputs

/--
The native geometry input object surface feeds the existing R1 theorem proof
input package.
-/
theorem r1_native_geometry_input_object_to_r1_theorem_proof_inputs
    (x : R1NativeGeometryInputObject) : R1TheoremProofInputs :=
  x

/--
The existing R1 theorem proof input package is the current native geometry input
object surface.
-/
theorem r1_theorem_proof_inputs_to_r1_native_geometry_input_object
    (x : R1TheoremProofInputs) : R1NativeGeometryInputObject :=
  x

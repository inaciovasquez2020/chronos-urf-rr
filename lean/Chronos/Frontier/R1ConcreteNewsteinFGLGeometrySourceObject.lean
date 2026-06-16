import Chronos.Frontier.R1NativeGeometryInputObject
import Chronos.Frontier.R1ConcreteSemanticDataInstance

namespace Chronos
namespace Frontier

/--
Concrete Newstein/FGL source object for the restricted safe R1 semantic data.

This source object no longer aliases the full native geometry input package.
It carries only the remaining source assumptions needed after the concrete safe
R1b bridge has been supplied by `R1ConcreteNativeSafeSemanticData_R1b`.
-/
structure R1ConcreteNewsteinFGLGeometrySourceObject where
  R1c_maximalSeparationForbidsTrivialLongChord : Prop
  R1c_supplied : R1c_maximalSeparationForbidsTrivialLongChord

/--
The concrete safe Newstein/FGL source object feeds the native R1 geometry input
object for `R1ConcreteNativeSafeSemanticData`.

The R1b input is discharged by `R1ConcreteNativeSafeSemanticData_R1b`; R1c is
kept as an explicit source field and is not solved here.
-/
def r1_concrete_newstein_fgl_geometry_source_object_to_native_geometry_input_object
    (x : R1ConcreteNewsteinFGLGeometrySourceObject) :
    R1NativeGeometryInputObject R1ConcreteNativeSafeSemanticData where
  R1a_trivialFaceBoundariesAvoidLongChords :=
    R1ConcreteNativeSafeSemanticData_R1a
  R1b_trivialWordSupportComesFromTrivialFaces :=
    R1ConcreteNativeSafeSemanticData_R1b
  R1c_maximalSeparationForbidsTrivialLongChord :=
    x.R1c_maximalSeparationForbidsTrivialLongChord
  R1c_supplied :=
    x.R1c_supplied

/--
The native safe R1 geometry input object restricts back to the concrete
Newstein/FGL source-object surface by forgetting the already-discharged R1b
field.
-/
def r1_native_geometry_input_object_to_concrete_newstein_fgl_geometry_source_object
    (x : R1NativeGeometryInputObject R1ConcreteNativeSafeSemanticData) :
    R1ConcreteNewsteinFGLGeometrySourceObject where
  R1c_maximalSeparationForbidsTrivialLongChord :=
    x.R1c_maximalSeparationForbidsTrivialLongChord
  R1c_supplied :=
    x.R1c_supplied

end Frontier
end Chronos

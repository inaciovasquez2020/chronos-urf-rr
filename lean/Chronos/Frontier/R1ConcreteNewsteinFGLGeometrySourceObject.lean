import Chronos.Frontier.R1NativeGeometryInputObject

namespace Chronos
namespace Frontier

/--
Boundary marker for the first concrete Newstein/FGL geometry source object.

This is only a source-object surface over the existing
`R1NativeGeometryInputObject` target. It does not construct that target from
concrete Newstein/FGL geometry.
-/
abbrev R1ConcreteNewsteinFGLGeometrySourceObject (D : R1SemanticData) :=
  R1NativeGeometryInputObject D

/--
The current concrete Newstein/FGL geometry source-object surface feeds the
existing native R1 geometry input object.
-/
def r1_concrete_newstein_fgl_geometry_source_object_to_native_geometry_input_object
    {D : R1SemanticData}
    (x : R1ConcreteNewsteinFGLGeometrySourceObject D) :
    R1NativeGeometryInputObject D :=
  x

/--
The existing native R1 geometry input object is the current repository-local
source-object surface for the concrete Newstein/FGL geometry target.
-/
def r1_native_geometry_input_object_to_concrete_newstein_fgl_geometry_source_object
    {D : R1SemanticData}
    (x : R1NativeGeometryInputObject D) :
    R1ConcreteNewsteinFGLGeometrySourceObject D :=
  x

end Frontier
end Chronos

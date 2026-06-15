import Chronos.Frontier.R1NativeGeometryInputObject

/--
Boundary marker for the first concrete Newstein/FGL geometry source object.

This is only a source-object surface over the existing
`R1NativeGeometryInputObject` target. It does not construct that target from
concrete Newstein/FGL geometry.
-/
abbrev R1ConcreteNewsteinFGLGeometrySourceObject := R1NativeGeometryInputObject

/--
The current concrete Newstein/FGL geometry source-object surface feeds the
existing native R1 geometry input object.
-/
theorem r1_concrete_newstein_fgl_geometry_source_object_to_native_geometry_input_object
    (x : R1ConcreteNewsteinFGLGeometrySourceObject) : R1NativeGeometryInputObject :=
  x

/--
The existing native R1 geometry input object is the current repository-local
source-object surface for the concrete Newstein/FGL geometry target.
-/
theorem r1_native_geometry_input_object_to_concrete_newstein_fgl_geometry_source_object
    (x : R1NativeGeometryInputObject) : R1ConcreteNewsteinFGLGeometrySourceObject :=
  x

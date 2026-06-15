import Chronos.Frontier.R1ConcreteNewsteinFGLGeometrySourceObject

/--
Boundary marker for the missing native construction map from the concrete
Newstein/FGL source object to the native R1 geometry input object.

This structure intentionally contains no function field. It records the target
of a future construction without constructing `R1NativeGeometryInputObject` from
`R1ConcreteNewsteinFGLGeometrySourceObject`.
-/
structure R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget : Type where
  marker : Unit := ()

/--
The map target is present as a boundary object.
-/
theorem r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target_exists :
    Nonempty R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget :=
  ⟨{}⟩

/--
The active boundary for this target is that no native construction map has been
provided.
-/
def r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target_boundary : String :=
  "NO_NATIVE_CONSTRUCTION_MAP_FROM_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT_TO_R1_NATIVE_GEOMETRY_INPUT_OBJECT"

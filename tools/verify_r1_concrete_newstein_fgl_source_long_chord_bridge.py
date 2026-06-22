from pathlib import Path

lean = Path("lean/Chronos/Frontier/R1ConcreteNewsteinFGLGeometrySourceObject.lean").read_text()

required = [
    "theorem r1_concrete_native_safe_long_chord_exclusion_from_concrete_newstein_fgl_source",
    "R1LongChordExclusionTheorem R1ConcreteNativeSafeSemanticData",
    "R1_LongChordExclusion_from_semantic_inputs",
    "r1_concrete_newstein_fgl_geometry_source_object_to_native_geometry_input_object x",
]

missing = [token for token in required if token not in lean]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

print("R1_CONCRETE_NEWSTEIN_FGL_SOURCE_LONG_CHORD_BRIDGE_OK")

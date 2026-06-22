from pathlib import Path

lean = Path("lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContract.lean").read_text()

required = [
    "structure R1ConcreteNewsteinFGLToNativeMapLongChordInputField",
    "def r1_concrete_newstein_fgl_to_native_map_input_contract_long_chord_field",
    "R1ConcreteNewsteinFGLToNativeMapInputContract D",
    "R1ConcreteNewsteinFGLToNativeMapLongChordInputField D",
    "longChordExclusionEvidence := x.longChordExclusionEvidence",
]

missing = [token for token in required if token not in lean]
if missing:
    raise SystemExit("MISSING_OBJECT := " + missing[0])

print("R1_CONCRETE_NEWSTEIN_FGL_TO_NATIVE_MAP_LONG_CHORD_INPUT_FIELD_OK")

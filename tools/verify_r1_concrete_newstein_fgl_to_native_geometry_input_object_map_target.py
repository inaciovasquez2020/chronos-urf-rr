#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target_2026_06_15.json"
SOURCE_FILE = ROOT / "lean/Chronos/Frontier/R1ConcreteNewsteinFGLGeometrySourceObject.lean"
TARGET_FILE = ROOT / "lean/Chronos/Frontier/R1NativeGeometryInputObject.lean"
LEAN_SURFACE = ROOT / "lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget.lean"
IMPORT_ROOT = ROOT / "lean/Chronos.lean"

EXPECTED = {
    "artifact": "R1_CONCRETE_NEWSTEIN_FGL_TO_NATIVE_GEOMETRY_INPUT_OBJECT_MAP_TARGET",
    "date": "2026-06-15",
    "repository": "chronos-urf-rr",
    "status": "boundary_map_target",
    "source_declaration": "R1ConcreteNewsteinFGLGeometrySourceObject",
    "target_declaration": "R1NativeGeometryInputObject",
    "source_declaration_file": "lean/Chronos/Frontier/R1ConcreteNewsteinFGLGeometrySourceObject.lean",
    "target_declaration_file": "lean/Chronos/Frontier/R1NativeGeometryInputObject.lean",
    "lean_surface": "lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget.lean",
    "next_missing_object": "native construction map from R1ConcreteNewsteinFGLGeometrySourceObject to R1NativeGeometryInputObject",
    "boundary": "NO_NATIVE_CONSTRUCTION_MAP_FROM_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT_TO_R1_NATIVE_GEOMETRY_INPUT_OBJECT",
    "verifier": "tools/verify_r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target.py",
    "test": "tests/test_r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target.py",
}

REQUIRED_EXISTING_DECLARATIONS = [
    "R1ConcreteNewsteinFGLGeometrySourceObject",
    "R1NativeGeometryInputObject",
]

REQUIRED_LEAN_DECLARATIONS = [
    "R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget",
    "r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target_exists",
    "r1_concrete_newstein_fgl_to_native_geometry_input_object_map_target_boundary",
]

REQUIRED_NON_CLAIMS = [
    "does not define a function from R1ConcreteNewsteinFGLGeometrySourceObject to R1NativeGeometryInputObject",
    "does not construct R1NativeGeometryInputObject from concrete Newstein/FGL geometry",
    "does not prove Newstein/FGL geometry satisfies R1TheoremProofInputs",
    "does not close R1",
]

FORBIDDEN_LEAN_FRAGMENTS = [
    "def r1_concrete_newstein_fgl_to_native_geometry_input_object\n",
    "theorem r1_concrete_newstein_fgl_to_native_geometry_input_object\n",
    ": R1NativeGeometryInputObject :=",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(ARTIFACT.exists(), f"missing artifact: {ARTIFACT}")
    require(SOURCE_FILE.exists(), f"missing source declaration file: {SOURCE_FILE}")
    require(TARGET_FILE.exists(), f"missing target declaration file: {TARGET_FILE}")
    require(LEAN_SURFACE.exists(), f"missing Lean surface: {LEAN_SURFACE}")
    require(IMPORT_ROOT.exists(), f"missing import root: {IMPORT_ROOT}")

    data = json.loads(ARTIFACT.read_text())

    for key, expected in EXPECTED.items():
        require(data.get(key) == expected, f"{key} mismatch")

    require(
        data.get("required_existing_declarations") == REQUIRED_EXISTING_DECLARATIONS,
        "required_existing_declarations mismatch",
    )
    require(
        data.get("required_lean_declarations") == REQUIRED_LEAN_DECLARATIONS,
        "required_lean_declarations mismatch",
    )
    require(data.get("non_claims") == REQUIRED_NON_CLAIMS, "non_claims mismatch")
    require(data.get("forbidden_lean_fragments") == FORBIDDEN_LEAN_FRAGMENTS, "forbidden_lean_fragments mismatch")

    source_text = SOURCE_FILE.read_text()
    target_text = TARGET_FILE.read_text()
    require("R1ConcreteNewsteinFGLGeometrySourceObject" in source_text, "missing source declaration")
    require("R1NativeGeometryInputObject" in target_text, "missing target declaration")

    lean_text = LEAN_SURFACE.read_text()
    require(
        "import Chronos.Frontier.R1ConcreteNewsteinFGLGeometrySourceObject" in lean_text,
        "missing source object import",
    )
    for declaration in REQUIRED_LEAN_DECLARATIONS:
        require(declaration in lean_text, f"missing Lean declaration: {declaration}")

    for forbidden in FORBIDDEN_LEAN_FRAGMENTS:
        require(forbidden not in lean_text, f"forbidden real-construction fragment present: {forbidden!r}")

    import_text = IMPORT_ROOT.read_text()
    require(
        "import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget" in import_text,
        "missing Chronos root import",
    )

    print("R1_CONCRETE_NEWSTEIN_FGL_TO_NATIVE_GEOMETRY_INPUT_OBJECT_MAP_TARGET_OK")


if __name__ == "__main__":
    main()

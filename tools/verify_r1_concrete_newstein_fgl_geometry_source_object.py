#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/r1_concrete_newstein_fgl_geometry_source_object_2026_06_15.json"
EXISTING_SOURCE = ROOT / "lean/Chronos/Frontier/R1NativeGeometryInputObject.lean"
LEAN_SURFACE = ROOT / "lean/Chronos/Frontier/R1ConcreteNewsteinFGLGeometrySourceObject.lean"
IMPORT_ROOT = ROOT / "lean/Chronos.lean"

EXPECTED = {
    "artifact": "R1_CONCRETE_NEWSTEIN_FGL_GEOMETRY_SOURCE_OBJECT_TARGET",
    "date": "2026-06-15",
    "repository": "chronos-urf-rr",
    "status": "boundary_source_object",
    "first_concrete_source_object": "R1ConcreteNewsteinFGLGeometrySourceObject",
    "feeds_existing_declaration": "R1NativeGeometryInputObject",
    "existing_declaration_source": "lean/Chronos/Frontier/R1NativeGeometryInputObject.lean",
    "lean_surface": "lean/Chronos/Frontier/R1ConcreteNewsteinFGLGeometrySourceObject.lean",
    "next_missing_object": "native construction map from concrete Newstein/FGL geometry source object to R1NativeGeometryInputObject",
    "boundary": "NO_CONCRETE_NEWSTEIN_FGL_GEOMETRY_TO_R1_NATIVE_GEOMETRY_INPUT_OBJECT_MAP",
    "verifier": "tools/verify_r1_concrete_newstein_fgl_geometry_source_object.py",
    "test": "tests/test_r1_concrete_newstein_fgl_geometry_source_object.py",
}

REQUIRED_EXISTING_DECLARATIONS = [
    "R1NativeGeometryInputObject",
]

REQUIRED_LEAN_DECLARATIONS = [
    "R1ConcreteNewsteinFGLGeometrySourceObject",
    "r1_concrete_newstein_fgl_geometry_source_object_to_native_geometry_input_object",
    "r1_native_geometry_input_object_to_concrete_newstein_fgl_geometry_source_object",
]

REQUIRED_NON_CLAIMS = [
    "does not construct R1NativeGeometryInputObject from Newstein/FGL geometry",
    "does not prove Newstein/FGL geometry satisfies R1TheoremProofInputs",
    "does not close R1",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(ARTIFACT.exists(), f"missing artifact: {ARTIFACT}")
    require(EXISTING_SOURCE.exists(), f"missing existing declaration source: {EXISTING_SOURCE}")
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

    existing_text = EXISTING_SOURCE.read_text()
    for declaration in REQUIRED_EXISTING_DECLARATIONS:
        require(declaration in existing_text, f"missing existing declaration: {declaration}")

    lean_text = LEAN_SURFACE.read_text()
    require(
        "import Chronos.Frontier.R1NativeGeometryInputObject" in lean_text,
        "missing native geometry input object import",
    )
    for declaration in REQUIRED_LEAN_DECLARATIONS:
        require(declaration in lean_text, f"missing Lean declaration: {declaration}")

    import_text = IMPORT_ROOT.read_text()
    require(
        "import Chronos.Frontier.R1ConcreteNewsteinFGLGeometrySourceObject" in import_text,
        "missing Chronos root import",
    )

    print("R1_CONCRETE_NEWSTEIN_FGL_GEOMETRY_SOURCE_OBJECT_OK")


if __name__ == "__main__":
    main()

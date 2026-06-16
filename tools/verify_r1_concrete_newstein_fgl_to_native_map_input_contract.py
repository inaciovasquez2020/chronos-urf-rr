#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/r1_concrete_newstein_fgl_to_native_map_input_contract_2026_06_15.json"
SOURCE_FILE = ROOT / "lean/Chronos/Frontier/R1ConcreteNewsteinFGLGeometrySourceObject.lean"
MAP_TARGET_FILE = ROOT / "lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget.lean"
LEAN_SURFACE = ROOT / "lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContract.lean"
IMPORT_ROOT = ROOT / "lean/Chronos.lean"

EXPECTED = {
    "artifact": "R1_CONCRETE_NEWSTEIN_FGL_TO_NATIVE_MAP_INPUT_CONTRACT",
    "date": "2026-06-15",
    "repository": "chronos-urf-rr",
    "status": "input_contract",
    "contract_declaration": "R1ConcreteNewsteinFGLToNativeMapInputContract",
    "source_declaration": "R1ConcreteNewsteinFGLGeometrySourceObject",
    "map_target_declaration": "R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget",
    "lean_surface": "lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContract.lean",
    "next_missing_object": "non-vacuous discharge of the input contract fields for concrete Newstein/FGL geometry",
    "boundary": "NO_DISCHARGED_INPUT_CONTRACT_FOR_NATIVE_CONSTRUCTION_MAP",
    "verifier": "tools/verify_r1_concrete_newstein_fgl_to_native_map_input_contract.py",
    "test": "tests/test_r1_concrete_newstein_fgl_to_native_map_input_contract.py",
}

REQUIRED_EXISTING_DECLARATIONS = [
    "R1ConcreteNewsteinFGLGeometrySourceObject",
    "R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget",
]

REQUIRED_CONTRACT_FIELDS = [
    "source",
    "r1LongChordExclusion",
    "r1DiameterSeparationFillingObstruction",
    "r1UniformLocalTypeCapacity",
    "r1SourceToNativeCompatibility",
    "longChordExclusionEvidence",
    "diameterSeparationFillingObstructionEvidence",
    "uniformLocalTypeCapacityEvidence",
    "sourceToNativeCompatibilityEvidence",
]

REQUIRED_LEAN_DECLARATIONS = [
    "R1ConcreteNewsteinFGLToNativeMapInputContract",
    "r1_concrete_newstein_fgl_to_native_map_input_contract_boundary",
]

REQUIRED_NON_CLAIMS = [
    "does not define the construction map",
    "does not construct R1NativeGeometryInputObject from concrete Newstein/FGL geometry",
    "does not discharge the contract fields",
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
    require(MAP_TARGET_FILE.exists(), f"missing map target file: {MAP_TARGET_FILE}")
    require(LEAN_SURFACE.exists(), f"missing Lean surface: {LEAN_SURFACE}")
    require(IMPORT_ROOT.exists(), f"missing import root: {IMPORT_ROOT}")

    data = json.loads(ARTIFACT.read_text())

    for key, expected in EXPECTED.items():
        require(data.get(key) == expected, f"{key} mismatch")

    require(data.get("required_existing_declarations") == REQUIRED_EXISTING_DECLARATIONS, "required_existing_declarations mismatch")
    require(data.get("required_contract_fields") == REQUIRED_CONTRACT_FIELDS, "required_contract_fields mismatch")
    require(data.get("required_lean_declarations") == REQUIRED_LEAN_DECLARATIONS, "required_lean_declarations mismatch")
    require(data.get("non_claims") == REQUIRED_NON_CLAIMS, "non_claims mismatch")
    require(data.get("forbidden_lean_fragments") == FORBIDDEN_LEAN_FRAGMENTS, "forbidden_lean_fragments mismatch")

    source_text = SOURCE_FILE.read_text()
    map_target_text = MAP_TARGET_FILE.read_text()
    require("R1ConcreteNewsteinFGLGeometrySourceObject" in source_text, "missing source declaration")
    require("R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget" in map_target_text, "missing map target declaration")

    lean_text = LEAN_SURFACE.read_text()
    require(
        "import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeGeometryInputObjectMapTarget" in lean_text,
        "missing map target import",
    )

    for declaration in REQUIRED_LEAN_DECLARATIONS:
        require(declaration in lean_text, f"missing Lean declaration: {declaration}")

    for field in REQUIRED_CONTRACT_FIELDS:
        require(field in lean_text, f"missing contract field: {field}")

    for forbidden in FORBIDDEN_LEAN_FRAGMENTS:
        require(forbidden not in lean_text, f"forbidden construction fragment present: {forbidden!r}")

    import_text = IMPORT_ROOT.read_text()
    require(
        "import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract" in import_text,
        "missing Chronos root import",
    )

    print("R1_CONCRETE_NEWSTEIN_FGL_TO_NATIVE_MAP_INPUT_CONTRACT_OK")


if __name__ == "__main__":
    main()

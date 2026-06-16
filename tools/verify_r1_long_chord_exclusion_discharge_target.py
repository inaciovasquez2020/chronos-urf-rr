#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/r1_long_chord_exclusion_discharge_target_2026_06_15.json"
CONTRACT_FILE = ROOT / "lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContract.lean"
LEAN_SURFACE = ROOT / "lean/Chronos/Frontier/R1LongChordExclusionDischargeTarget.lean"
IMPORT_ROOT = ROOT / "lean/Chronos.lean"

EXPECTED = {
    "artifact": "R1_LONG_CHORD_EXCLUSION_DISCHARGE_TARGET",
    "date": "2026-06-15",
    "repository": "chronos-urf-rr",
    "status": "field_discharge_target",
    "target_field": "r1LongChordExclusion",
    "parent_contract": "R1ConcreteNewsteinFGLToNativeMapInputContract",
    "parent_contract_file": "lean/Chronos/Frontier/R1ConcreteNewsteinFGLToNativeMapInputContract.lean",
    "lean_surface": "lean/Chronos/Frontier/R1LongChordExclusionDischargeTarget.lean",
    "next_missing_object": "non-vacuous proof of long-chord exclusion for the concrete Newstein/FGL source object",
    "boundary": "NO_DISCHARGED_R1_LONG_CHORD_EXCLUSION_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT",
    "verifier": "tools/verify_r1_long_chord_exclusion_discharge_target.py",
    "test": "tests/test_r1_long_chord_exclusion_discharge_target.py",
}

REQUIRED_EXISTING_DECLARATIONS = [
    "R1ConcreteNewsteinFGLToNativeMapInputContract",
    "r1LongChordExclusion",
]

REQUIRED_LEAN_DECLARATIONS = [
    "R1LongChordExclusionDischargeTarget",
    "r1_long_chord_exclusion_discharge_target_boundary",
]

REQUIRED_CONTRACT_FIELDS = [
    "source",
    "r1LongChordExclusion",
    "longChordExclusionEvidence",
]

REQUIRED_NON_CLAIMS = [
    "does not discharge r1LongChordExclusion",
    "does not define the native construction map",
    "does not construct R1NativeGeometryInputObject from concrete Newstein/FGL geometry",
    "does not close R1",
]

FORBIDDEN_LEAN_FRAGMENTS = [
    "theorem r1_long_chord_exclusion_discharge",
    "def r1_concrete_newstein_fgl_to_native_geometry_input_object",
    ": R1NativeGeometryInputObject :=",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(ARTIFACT.exists(), f"missing artifact: {ARTIFACT}")
    require(CONTRACT_FILE.exists(), f"missing contract file: {CONTRACT_FILE}")
    require(LEAN_SURFACE.exists(), f"missing Lean surface: {LEAN_SURFACE}")
    require(IMPORT_ROOT.exists(), f"missing import root: {IMPORT_ROOT}")

    data = json.loads(ARTIFACT.read_text())

    for key, expected in EXPECTED.items():
        require(data.get(key) == expected, f"{key} mismatch")

    require(data.get("required_existing_declarations") == REQUIRED_EXISTING_DECLARATIONS, "required_existing_declarations mismatch")
    require(data.get("required_lean_declarations") == REQUIRED_LEAN_DECLARATIONS, "required_lean_declarations mismatch")
    require(data.get("required_contract_fields") == REQUIRED_CONTRACT_FIELDS, "required_contract_fields mismatch")
    require(data.get("non_claims") == REQUIRED_NON_CLAIMS, "non_claims mismatch")
    require(data.get("forbidden_lean_fragments") == FORBIDDEN_LEAN_FRAGMENTS, "forbidden_lean_fragments mismatch")

    contract_text = CONTRACT_FILE.read_text()
    for declaration in REQUIRED_EXISTING_DECLARATIONS:
        require(declaration in contract_text, f"missing existing declaration or field: {declaration}")

    lean_text = LEAN_SURFACE.read_text()
    require(
        "import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract" in lean_text,
        "missing input contract import",
    )

    for declaration in REQUIRED_LEAN_DECLARATIONS:
        require(declaration in lean_text, f"missing Lean declaration: {declaration}")

    for field in REQUIRED_CONTRACT_FIELDS:
        require(field in lean_text, f"missing discharge target field: {field}")

    for forbidden in FORBIDDEN_LEAN_FRAGMENTS:
        require(forbidden not in lean_text, f"forbidden Lean fragment present: {forbidden!r}")

    import_text = IMPORT_ROOT.read_text()
    require(
        "import Chronos.Frontier.R1LongChordExclusionDischargeTarget" in import_text,
        "missing Chronos root import",
    )

    print("R1_LONG_CHORD_EXCLUSION_DISCHARGE_TARGET_OK")


if __name__ == "__main__":
    main()

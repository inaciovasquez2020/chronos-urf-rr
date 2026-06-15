#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/r1_native_geometry_input_object_2026_06_15.json"
SOURCE_BRIDGE = ROOT / "lean/Chronos/Frontier/R1NativeInputBridge.lean"

EXPECTED = {
    "artifact": "R1_NATIVE_GEOMETRY_INPUT_OBJECT_TARGET",
    "date": "2026-06-15",
    "repository": "chronos-urf-rr",
    "status": "boundary_target",
    "source_bridge": "lean/Chronos/Frontier/R1NativeInputBridge.lean",
    "requires_existing_declaration": "R1TheoremProofInputs",
    "next_missing_object": "native construction of R1TheoremProofInputs from concrete Newstein/FGL geometry",
    "boundary": "NO_NATIVE_CONCRETE_NEWSTEIN_FGL_TO_R1_PROOF_INPUTS_CONSTRUCTION",
    "verifier": "tools/verify_r1_native_geometry_input_object.py",
    "test": "tests/test_r1_native_geometry_input_object.py",
}

REQUIRED_NON_CLAIMS = [
    "does not construct R1TheoremProofInputs",
    "does not prove Newstein/FGL geometry satisfies R1TheoremProofInputs",
    "does not close R1",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(ARTIFACT.exists(), f"missing artifact: {ARTIFACT}")
    require(SOURCE_BRIDGE.exists(), f"missing source bridge: {SOURCE_BRIDGE}")

    data = json.loads(ARTIFACT.read_text())

    for key, expected in EXPECTED.items():
        require(data.get(key) == expected, f"{key} mismatch")

    require(data.get("non_claims") == REQUIRED_NON_CLAIMS, "non_claims mismatch")

    source_text = SOURCE_BRIDGE.read_text()
    require(
        "R1TheoremProofInputs" in source_text,
        "missing existing declaration surface: R1TheoremProofInputs",
    )

    print("R1_NATIVE_GEOMETRY_INPUT_OBJECT_OK")


if __name__ == "__main__":
    main()

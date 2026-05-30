#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/shape_compatible_authentic_external_gravity_model_vector_source_2026_05_29.json")
DOC = Path("docs/status/SHAPE_COMPATIBLE_AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/ShapeCompatibleAuthenticExternalGravityModelVectorSource.lean")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "SOURCE_CONTRACT_ONLY_AUTHENTIC_EXTERNAL_VECTOR_SOURCE_NOT_SUPPLIED"
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]
    assert artifact["authentic_external_source_supplied"] is False
    assert artifact["shape_compatible_vector_supplied"] is False
    assert artifact["external_model_comparison_executable"] is False
    assert artifact["weakest_missing_object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_FILE_AND_PROVENANCE_CERTIFICATE"

    contract = artifact["required_source_contract"]
    assert all(contract.values())

    assert len(artifact["accepted_source_classes"]) == 5
    assert len(artifact["candidate_local_paths"]) == 2
    assert artifact["empirical_gravity_result"] is False
    assert artifact["external_gravity_model_validation"] is False
    assert all(artifact["boundary"].values())
    assert artifact["next_admissible_object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_FILE_AND_PROVENANCE_CERTIFICATE"

    print("SHAPE_COMPATIBLE_AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OK")

if __name__ == "__main__":
    main()

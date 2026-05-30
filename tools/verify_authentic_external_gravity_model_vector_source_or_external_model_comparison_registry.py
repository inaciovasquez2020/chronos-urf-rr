#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_external_model_comparison_registry_2026_05_29.json")
DOC = Path("docs/status/AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_EXTERNAL_MODEL_COMPARISON_REGISTRY_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorSourceOrExternalModelComparisonRegistry.lean")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "EXTERNAL_MODEL_COMPARISON_REGISTRY_ONLY_VECTOR_SOURCE_NOT_SUPPLIED"
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]
    assert artifact["external_gravity_model_vector_source_supplied"] is False
    assert artifact["external_model_comparison_executable"] is False
    assert len(artifact["candidate_external_sources"]) == 5
    assert artifact["weakest_missing_object"] == "SHAPE_COMPATIBLE_AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE"
    assert artifact["empirical_gravity_result"] is False
    assert artifact["external_gravity_model_validation"] is False
    assert all(artifact["boundary"].values())
    assert artifact["next_admissible_object"] == "SHAPE_COMPATIBLE_AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE"

    print("AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_EXTERNAL_MODEL_COMPARISON_REGISTRY_OK")

if __name__ == "__main__":
    main()

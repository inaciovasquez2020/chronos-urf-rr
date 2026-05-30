#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_file_and_provenance_certificate_2026_05_30.json")
DOC = Path("docs/status/AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_FILE_AND_PROVENANCE_CERTIFICATE_2026_05_30.md")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorFileAndProvenanceCertificate.lean")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "REQUIRED_AUTHENTIC_EXTERNAL_VECTOR_FILE_AND_PROVENANCE_CERTIFICATE_NOT_SUPPLIED"
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]
    assert len(artifact["candidate_local_paths"]) == 2
    assert all(artifact["required_provenance_certificate_fields"].values())
    assert artifact["authentic_external_vector_file_supplied"] is False
    assert artifact["provenance_certificate_supplied"] is False
    assert artifact["shape_compatible"] is False
    assert artifact["external_model_comparison_executable"] is False
    assert artifact["weakest_missing_object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_FILE_WITH_SOURCE_URL_EXTRACTION_SCRIPT_AND_SHA256"
    assert artifact["empirical_gravity_result"] is False
    assert artifact["external_gravity_model_validation"] is False
    assert all(artifact["boundary"].values())
    assert artifact["next_admissible_object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_FILE_WITH_SOURCE_URL_EXTRACTION_SCRIPT_AND_SHA256"

    print("AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_FILE_AND_PROVENANCE_CERTIFICATE_OK")

if __name__ == "__main__":
    main()

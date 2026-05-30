#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/gravity/shape_compatible_independent_nonzero_baseline_vector_file_2026_05_29.json")
DOC = Path("docs/status/SHAPE_COMPATIBLE_INDEPENDENT_NONZERO_BASELINE_VECTOR_FILE_2026_05_29.md")

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "SHAPE_COMPATIBLE_INDEPENDENT_NONZERO_BASELINE_VECTOR_FILE_PRESENT_DISTINCT_FROM_DEFICIT_VECTOR"
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]
    assert artifact["baseline_path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["baseline_shape"] == [255, 360, 720]
    assert artifact["baseline_size"] == 66096000
    assert artifact["baseline_nonzero"] is True
    assert artifact["distinct_from_deficit_vector"] is True
    assert artifact["mean_absolute_delta_from_deficit_vector"] > 0.0
    assert len(artifact["baseline_sha256"]) == 64
    assert artifact["external_gravity_model_status"] == "not_supplied"
    assert all(artifact["boundary"].values())

    print("SHAPE_COMPATIBLE_INDEPENDENT_NONZERO_BASELINE_VECTOR_FILE_OK")

if __name__ == "__main__":
    main()

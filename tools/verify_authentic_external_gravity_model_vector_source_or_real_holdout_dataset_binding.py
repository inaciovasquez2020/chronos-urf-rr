#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_real_holdout_dataset_binding_2026_05_29.json")
DOC = Path("docs/status/AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_REAL_HOLDOUT_DATASET_BINDING_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorSourceOrRealHoldoutDatasetBinding.lean")

def finite_number(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "REAL_HOLDOUT_DATASET_BINDING_SUPPLIED_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_NOT_SUPPLIED"
    assert artifact["branch_selected"] == "real_holdout_dataset_binding"
    assert artifact["authentic_external_gravity_model_vector_source_supplied"] is False
    assert artifact["real_holdout_dataset_binding_supplied"] is True
    assert artifact["empirical_gravity_result"] is False
    assert artifact["external_gravity_model_validation"] is False

    assert len(artifact["authenticated_binding_artifacts"]) >= 1
    for item in artifact["authenticated_binding_artifacts"]:
        assert Path(item["path"]).exists()
        assert len(item["sha256"]) == 64

    holdout = artifact["holdout_binding"]
    assert holdout["rule"] == "time_index_mod_5_eq_0"
    assert holdout["time_count"] == 51
    assert holdout["spatial_slice_length"] == 259200
    assert holdout["holdout_vector_length"] == 13219200
    assert holdout["required_vector_length"] == 66096000
    assert holdout["required_shape"] == [255, 360, 720]

    metrics = artifact["inherited_holdout_metrics"]
    assert metrics["holdout_vector_length"] == 13219200
    assert finite_number(metrics["mean_absolute_delta"])
    assert finite_number(metrics["root_mean_square_delta"])
    assert metrics["mean_absolute_delta"] > 0.0
    assert metrics["root_mean_square_delta"] > 0.0

    assert artifact["bound_vectors"]["independent_baseline_path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["bound_vectors"]["comparison_vector_path"] == "data/mascon_vectors/deficit_vector.npy"

    assert all(artifact["boundary"].values())
    assert artifact["next_admissible_object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN"

    print("AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_REAL_HOLDOUT_DATASET_BINDING_OK")

if __name__ == "__main__":
    main()

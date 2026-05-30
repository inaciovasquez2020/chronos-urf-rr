#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/gravity/external_gravity_model_vector_from_authentic_source_or_independent_holdout_comparison_protocol_2026_05_29.json")
DOC = Path("docs/status/EXTERNAL_GRAVITY_MODEL_VECTOR_FROM_AUTHENTIC_SOURCE_OR_INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/ExternalGravityModelVectorFromAuthenticSourceOrIndependentHoldoutComparisonProtocol.lean")
RUNNER = Path("tools/run_external_gravity_model_vector_from_authentic_source_or_independent_holdout_comparison_protocol.py")

def finite_number(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert RUNNER.exists(), f"missing runner: {RUNNER}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL_EXECUTED_EXTERNAL_GRAVITY_MODEL_VECTOR_NOT_SUPPLIED"
    assert artifact["branch_selected"] == "independent_holdout_comparison_protocol"
    assert artifact["external_gravity_model_vector_supplied"] is False
    assert artifact["independent_holdout_protocol_executed"] is True
    assert artifact["external_gravity_model_validation"] is False
    assert artifact["empirical_gravity_result"] is False

    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]

    holdout = artifact["holdout_selection"]
    assert holdout["rule"] == "time_index_mod_5_eq_0"
    assert holdout["time_count"] == 51
    assert holdout["spatial_slice_length"] == 259200
    assert holdout["holdout_vector_length"] == 13219200

    metrics = artifact["metrics"]
    assert metrics["holdout_vector_length"] == 13219200
    assert finite_number(metrics["mean_absolute_delta"])
    assert finite_number(metrics["root_mean_square_delta"])
    assert metrics["mean_absolute_delta"] > 0.0
    assert metrics["root_mean_square_delta"] > 0.0
    assert metrics["independent_baseline_nonzero_count"] > 0
    assert metrics["deficit_vector_nonzero_count"] > 0

    assert artifact["independent_baseline"]["path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["comparison_vector"]["path"] == "data/mascon_vectors/deficit_vector.npy"

    assert all(artifact["boundary"].values())
    assert artifact["next_admissible_object"] == "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_REAL_HOLDOUT_DATASET_BINDING"

    print("EXTERNAL_GRAVITY_MODEL_VECTOR_FROM_AUTHENTIC_SOURCE_OR_INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL_OK")

if __name__ == "__main__":
    main()

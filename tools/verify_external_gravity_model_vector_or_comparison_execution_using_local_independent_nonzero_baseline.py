#!/usr/bin/env python3
import json
import math
from pathlib import Path

ART = Path("artifacts/gravity/external_gravity_model_vector_or_comparison_execution_using_local_independent_nonzero_baseline_2026_05_29.json")
DOC = Path("docs/status/EXTERNAL_GRAVITY_MODEL_VECTOR_OR_COMPARISON_EXECUTION_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/ExternalGravityModelVectorOrComparisonExecutionUsingLocalIndependentNonzeroBaseline.lean")
RUNNER = Path("tools/run_external_gravity_model_vector_or_comparison_execution_using_local_independent_nonzero_baseline.py")

def finite_number(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert RUNNER.exists(), f"missing runner: {RUNNER}"

    artifact = json.loads(ART.read_text())

    assert artifact["status"] == "COMPARISON_EXECUTED_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_EXTERNAL_GRAVITY_MODEL_VECTOR_NOT_SUPPLIED"
    assert artifact["source_object"] == "SHAPE_COMPATIBLE_INDEPENDENT_NONZERO_BASELINE_VECTOR_FILE_2026_05_29"
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]
    assert artifact["external_gravity_model_vector_supplied"] is False
    assert artifact["comparison_execution_using_local_independent_baseline"] is True
    assert artifact["empirical_gravity_result"] is False

    assert artifact["independent_baseline"]["path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["independent_baseline"]["shape"] == [255, 360, 720]
    assert artifact["independent_baseline"]["size"] == 66096000
    assert artifact["independent_baseline"]["nonzero_sample_check"] is True

    assert artifact["comparison_vector"]["path"] == "data/mascon_vectors/deficit_vector.npy"
    assert artifact["comparison_vector"]["size"] == 66096000
    assert artifact["comparison_vector"]["nonzero_sample_check"] is True

    metrics = artifact["metrics"]
    assert metrics["vector_length"] == 66096000
    assert finite_number(metrics["mean_absolute_delta"])
    assert metrics["mean_absolute_delta"] > 0.0
    assert finite_number(metrics["root_mean_square_delta"])
    assert metrics["root_mean_square_delta"] > 0.0
    assert finite_number(metrics["max_absolute_delta"])
    assert metrics["independent_baseline_nonzero_count"] > 0
    assert metrics["deficit_vector_nonzero_count"] > 0

    assert all(artifact["boundary"].values())
    assert artifact["next_admissible_object"] == "EXTERNAL_GRAVITY_MODEL_VECTOR_FROM_AUTHENTIC_GRAVITY_MODEL_SOURCE_OR_INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL"

    print("EXTERNAL_GRAVITY_MODEL_VECTOR_OR_COMPARISON_EXECUTION_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_OK")

if __name__ == "__main__":
    main()

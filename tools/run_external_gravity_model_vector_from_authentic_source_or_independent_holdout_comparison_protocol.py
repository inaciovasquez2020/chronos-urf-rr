#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

import numpy as np

SHAPE = (255, 360, 720)
VECTOR_LENGTH = 66_096_000
SPATIAL_SLICE = 360 * 720
HOLDOUT_TIME_INDICES = list(range(0, 255, 5))
HOLDOUT_VECTOR_LENGTH = len(HOLDOUT_TIME_INDICES) * SPATIAL_SLICE

BASELINE = Path("data/mascon_vectors/independent_nonzero_baseline_vector.npy")
DEFICIT = Path("data/mascon_vectors/deficit_vector.npy")
ART = Path("artifacts/gravity/external_gravity_model_vector_from_authentic_source_or_independent_holdout_comparison_protocol_2026_05_29.json")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def load_vector(path: Path):
    if not path.exists():
        raise SystemExit(f"missing vector: {path}")
    arr = np.load(path, mmap_mode="r")
    if int(arr.size) != VECTOR_LENGTH:
        raise SystemExit(f"wrong vector length for {path}: {arr.size}")
    return arr

def compute_holdout_metrics(baseline, deficit):
    bflat = baseline.reshape(-1)
    dflat = deficit.reshape(-1)

    sum_delta = 0.0
    sum_abs_delta = 0.0
    sum_sq_delta = 0.0
    max_abs_delta = 0.0

    sum_abs_baseline = 0.0
    sum_abs_deficit = 0.0
    baseline_nonzero_count = 0
    deficit_nonzero_count = 0

    dot = 0.0
    norm_b = 0.0
    norm_d = 0.0

    for t in HOLDOUT_TIME_INDICES:
        start = t * SPATIAL_SLICE
        stop = start + SPATIAL_SLICE

        b = np.asarray(bflat[start:stop], dtype=np.float64)
        d = np.asarray(dflat[start:stop], dtype=np.float64)
        delta = d - b
        abs_delta = np.abs(delta)

        sum_delta += float(np.sum(delta))
        sum_abs_delta += float(np.sum(abs_delta))
        sum_sq_delta += float(np.sum(delta * delta))
        max_abs_delta = max(max_abs_delta, float(np.max(abs_delta)))

        sum_abs_baseline += float(np.sum(np.abs(b)))
        sum_abs_deficit += float(np.sum(np.abs(d)))
        baseline_nonzero_count += int(np.count_nonzero(b))
        deficit_nonzero_count += int(np.count_nonzero(d))

        dot += float(np.sum(b * d))
        norm_b += float(np.sum(b * b))
        norm_d += float(np.sum(d * d))

    cosine_similarity = None
    if norm_b > 0.0 and norm_d > 0.0:
        cosine_similarity = dot / math.sqrt(norm_b * norm_d)

    return {
        "holdout_time_count": len(HOLDOUT_TIME_INDICES),
        "holdout_vector_length": HOLDOUT_VECTOR_LENGTH,
        "mean_delta": sum_delta / HOLDOUT_VECTOR_LENGTH,
        "mean_absolute_delta": sum_abs_delta / HOLDOUT_VECTOR_LENGTH,
        "root_mean_square_delta": math.sqrt(sum_sq_delta / HOLDOUT_VECTOR_LENGTH),
        "max_absolute_delta": max_abs_delta,
        "mean_absolute_independent_baseline": sum_abs_baseline / HOLDOUT_VECTOR_LENGTH,
        "mean_absolute_deficit_vector": sum_abs_deficit / HOLDOUT_VECTOR_LENGTH,
        "independent_baseline_nonzero_count": baseline_nonzero_count,
        "deficit_vector_nonzero_count": deficit_nonzero_count,
        "cosine_similarity": cosine_similarity,
    }

def main():
    baseline = load_vector(BASELINE)
    deficit = load_vector(DEFICIT)

    if tuple(baseline.shape) != SHAPE:
        raise SystemExit(f"baseline shape mismatch: {baseline.shape}")

    metrics = compute_holdout_metrics(baseline, deficit)

    if metrics["mean_absolute_delta"] <= 0.0:
        raise SystemExit("holdout mean_absolute_delta is not positive")
    if metrics["root_mean_square_delta"] <= 0.0:
        raise SystemExit("holdout root_mean_square_delta is not positive")

    artifact = {
        "id": "EXTERNAL_GRAVITY_MODEL_VECTOR_FROM_AUTHENTIC_SOURCE_OR_INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL_2026_05_29",
        "status": "INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL_EXECUTED_EXTERNAL_GRAVITY_MODEL_VECTOR_NOT_SUPPLIED",
        "source_object": "EXTERNAL_GRAVITY_MODEL_VECTOR_OR_COMPARISON_EXECUTION_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_2026_05_29",
        "branch_selected": "independent_holdout_comparison_protocol",
        "external_gravity_model_vector_supplied": False,
        "independent_holdout_protocol_executed": True,
        "external_gravity_model_validation": False,
        "empirical_gravity_result": False,
        "required_vector_length": VECTOR_LENGTH,
        "required_shape": list(SHAPE),
        "holdout_selection": {
            "rule": "time_index_mod_5_eq_0",
            "time_indices": HOLDOUT_TIME_INDICES,
            "time_count": len(HOLDOUT_TIME_INDICES),
            "spatial_slice_length": SPATIAL_SLICE,
            "holdout_vector_length": HOLDOUT_VECTOR_LENGTH
        },
        "independent_baseline": {
            "path": str(BASELINE),
            "shape": list(baseline.shape),
            "size": int(baseline.size),
            "dtype": str(baseline.dtype),
            "sha256": sha256_file(BASELINE)
        },
        "comparison_vector": {
            "path": str(DEFICIT),
            "shape": list(deficit.shape),
            "size": int(deficit.size),
            "dtype": str(deficit.dtype),
            "sha256": sha256_file(DEFICIT)
        },
        "metrics": metrics,
        "boundary": {
            "local_holdout_control_protocol_only": True,
            "no_external_gravity_model_vector_supplied": True,
            "no_external_gravity_model_fabrication": True,
            "no_external_gravity_model_validation": True,
            "no_empirical_gravity_result": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement": True,
            "no_lambda_cdm_failure": True,
            "no_quantum_gravity": True,
            "no_clay_problem": True
        },
        "next_admissible_object": "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_REAL_HOLDOUT_DATASET_BINDING"
    }

    ART.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("EXTERNAL_GRAVITY_MODEL_VECTOR_FROM_AUTHENTIC_SOURCE_OR_INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL_EXECUTED")
    print(json.dumps({
        "status": artifact["status"],
        "branch_selected": artifact["branch_selected"],
        "holdout_vector_length": artifact["holdout_selection"]["holdout_vector_length"],
        "mean_absolute_delta": artifact["metrics"]["mean_absolute_delta"],
        "root_mean_square_delta": artifact["metrics"]["root_mean_square_delta"],
        "next_admissible_object": artifact["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

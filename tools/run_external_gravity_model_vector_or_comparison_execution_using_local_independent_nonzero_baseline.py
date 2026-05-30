#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

import numpy as np

VECTOR_LENGTH = 66_096_000
SHAPE = (255, 360, 720)

BASELINE = Path("data/mascon_vectors/independent_nonzero_baseline_vector.npy")
DEFICIT = Path("data/mascon_vectors/deficit_vector.npy")
ART = Path("artifacts/gravity/external_gravity_model_vector_or_comparison_execution_using_local_independent_nonzero_baseline_2026_05_29.json")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def require_vector(path: Path, *, require_shape: bool):
    if not path.exists():
        raise SystemExit(f"Missing required vector file: {path}")
    arr = np.load(path, mmap_mode="r")
    if int(arr.size) != VECTOR_LENGTH:
        raise SystemExit(f"Wrong vector length for {path}: {arr.size}")
    if require_shape and tuple(arr.shape) != SHAPE:
        raise SystemExit(f"Wrong vector shape for {path}: {arr.shape}")
    return arr

def sample_nonzero(arr) -> bool:
    flat = arr.reshape(-1)
    step = max(1, flat.size // 10000)
    return bool(np.any(flat[::step] != 0))

def compute_metrics(baseline, deficit):
    bflat = baseline.reshape(-1)
    dflat = deficit.reshape(-1)

    n = VECTOR_LENGTH
    chunk = 1_000_000

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

    for start in range(0, n, chunk):
        stop = min(start + chunk, n)
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
        "vector_length": n,
        "mean_delta": sum_delta / n,
        "mean_absolute_delta": sum_abs_delta / n,
        "root_mean_square_delta": math.sqrt(sum_sq_delta / n),
        "max_absolute_delta": max_abs_delta,
        "mean_absolute_independent_baseline": sum_abs_baseline / n,
        "mean_absolute_deficit_vector": sum_abs_deficit / n,
        "independent_baseline_nonzero_count": baseline_nonzero_count,
        "deficit_vector_nonzero_count": deficit_nonzero_count,
        "cosine_similarity": cosine_similarity,
    }

def main():
    baseline = require_vector(BASELINE, require_shape=True)
    deficit = require_vector(DEFICIT, require_shape=False)

    if not sample_nonzero(baseline):
        raise SystemExit("Independent baseline vector sampled as zero.")
    if not sample_nonzero(deficit):
        raise SystemExit("Deficit vector sampled as zero.")

    metrics = compute_metrics(baseline, deficit)

    artifact = {
        "id": "EXTERNAL_GRAVITY_MODEL_VECTOR_OR_COMPARISON_EXECUTION_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_2026_05_29",
        "status": "COMPARISON_EXECUTED_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_EXTERNAL_GRAVITY_MODEL_VECTOR_NOT_SUPPLIED",
        "source_object": "SHAPE_COMPATIBLE_INDEPENDENT_NONZERO_BASELINE_VECTOR_FILE_2026_05_29",
        "execution_mode": "local independent nonzero baseline comparison",
        "required_vector_length": VECTOR_LENGTH,
        "required_shape": list(SHAPE),
        "external_gravity_model_vector_supplied": False,
        "comparison_execution_using_local_independent_baseline": True,
        "comparison_result_type": "local control comparison only; not external-model validation",
        "independent_baseline": {
            "path": str(BASELINE),
            "shape": list(baseline.shape),
            "size": int(baseline.size),
            "dtype": str(baseline.dtype),
            "sha256": sha256_file(BASELINE),
            "nonzero_sample_check": True,
        },
        "comparison_vector": {
            "path": str(DEFICIT),
            "shape": list(deficit.shape),
            "size": int(deficit.size),
            "dtype": str(deficit.dtype),
            "sha256": sha256_file(DEFICIT),
            "nonzero_sample_check": True,
        },
        "metrics": metrics,
        "empirical_gravity_result": False,
        "boundary": {
            "no_external_gravity_model_fabrication": True,
            "no_external_gravity_model_validation": True,
            "no_empirical_gravity_result": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement": True,
            "no_lambda_cdm_failure": True,
            "no_quantum_gravity": True,
            "no_clay_problem": True,
        },
        "next_admissible_object": "EXTERNAL_GRAVITY_MODEL_VECTOR_FROM_AUTHENTIC_GRAVITY_MODEL_SOURCE_OR_INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL",
    }

    ART.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("EXTERNAL_GRAVITY_MODEL_VECTOR_OR_COMPARISON_EXECUTION_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_EXECUTED")
    print(json.dumps({
        "status": artifact["status"],
        "external_gravity_model_vector_supplied": artifact["external_gravity_model_vector_supplied"],
        "comparison_execution_using_local_independent_baseline": artifact["comparison_execution_using_local_independent_baseline"],
        "mean_absolute_delta": artifact["metrics"]["mean_absolute_delta"],
        "root_mean_square_delta": artifact["metrics"]["root_mean_square_delta"],
        "next_admissible_object": artifact["next_admissible_object"],
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

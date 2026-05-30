#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

import numpy as np

BASELINE = Path("data/mascon_vectors/baseline_vector.npy")
DEFICIT = Path("data/mascon_vectors/deficit_vector.npy")
OUT = Path("artifacts/gravity/mascon_model_comparison_numeric_execution_result_2026_05_29.json")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def scalar(x) -> float:
    return float(np.asarray(x, dtype=np.float64))

def main():
    if not BASELINE.exists():
        raise SystemExit(f"missing baseline vector: {BASELINE}")
    if not DEFICIT.exists():
        raise SystemExit(f"missing deficit vector: {DEFICIT}")

    baseline = np.load(BASELINE, mmap_mode="r").astype(np.float64)
    deficit = np.load(DEFICIT, mmap_mode="r").astype(np.float64)

    if baseline.shape != deficit.shape:
        raise SystemExit(f"shape mismatch: baseline={baseline.shape}, deficit={deficit.shape}")

    residual = deficit - baseline

    baseline_norm = scalar(np.linalg.norm(baseline))
    deficit_norm = scalar(np.linalg.norm(deficit))
    denominator = baseline_norm * deficit_norm

    cosine_similarity = None if denominator == 0.0 else scalar(np.dot(baseline, deficit) / denominator)
    pearson_correlation = None
    if scalar(np.std(baseline)) > 0.0 and scalar(np.std(deficit)) > 0.0:
        pearson_correlation = scalar(np.corrcoef(baseline, deficit)[0, 1])

    mse = scalar(np.mean(residual * residual))

    result = {
        "id": "MASCON_MODEL_COMPARISON_NUMERIC_EXECUTION_RESULT_2026_05_29",
        "status": "NUMERIC_MODEL_COMPARISON_EXECUTED_NO_EMPIRICAL_CLAIM",
        "baseline_vector": str(BASELINE),
        "deficit_vector": str(DEFICIT),
        "baseline_sha256": sha256(BASELINE),
        "deficit_sha256": sha256(DEFICIT),
        "shape": list(baseline.shape),
        "vector_length": int(baseline.size),
        "metrics": {
            "mean_absolute_error": scalar(np.mean(np.abs(residual))),
            "mean_squared_error": mse,
            "root_mean_squared_error": math.sqrt(mse),
            "max_absolute_residual": scalar(np.max(np.abs(residual))),
            "baseline_l2_norm": baseline_norm,
            "deficit_l2_norm": deficit_norm,
            "residual_l2_norm": scalar(np.linalg.norm(residual)),
            "cosine_similarity": cosine_similarity,
            "pearson_correlation": pearson_correlation
        },
        "numeric_metrics_executed": True,
        "model_comparison_executed": True,
        "empirical_gravity_result": False,
        "interpretation": "numeric residual comparison only against zero-anomaly baseline control",
        "boundary": {
            "no_empirical_gravity_result": True,
            "no_gr_failure_claim": True,
            "no_new_gravity_claim": True,
            "no_dark_matter_replacement": True,
            "no_lambda_cdm_failure": True,
            "no_quantum_gravity": True,
            "no_clay_problem": True
        },
        "next_admissible_object": "MASCON_MODEL_COMPARISON_INTERPRETATION_BOUNDARY"
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print("MASCON_MODEL_COMPARISON_NUMERIC_EXECUTION_RESULT_GENERATED")
    print(json.dumps({
        "vector_length": result["vector_length"],
        "mean_absolute_error": result["metrics"]["mean_absolute_error"],
        "root_mean_squared_error": result["metrics"]["root_mean_squared_error"],
        "max_absolute_residual": result["metrics"]["max_absolute_residual"],
        "cosine_similarity": result["metrics"]["cosine_similarity"],
        "pearson_correlation": result["metrics"]["pearson_correlation"]
    }, indent=2))

if __name__ == "__main__":
    main()

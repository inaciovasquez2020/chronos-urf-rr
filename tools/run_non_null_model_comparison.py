#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
UNIT = Path("artifacts/chronos/unit_conversion_certificate_2026_06_01.json")
DERIVATION = Path("artifacts/chronos/non_null_physical_model_vector_or_deficit_mass_derivation_2026_06_01.json")
OUT = Path("artifacts/chronos/non_null_model_comparison_run_output_2026_06_01.json")

def load(path: Path) -> dict:
    return json.loads(path.read_text())

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def finite_vector(values):
    out = [float(x) for x in values]
    assert all(math.isfinite(x) for x in out)
    return out

def main() -> None:
    baseline = load(BASELINE)
    unit = load(UNIT)
    derivation = load(DERIVATION)

    assert baseline["object"] == "BASELINE_GRAVITY_VECTOR"
    assert unit["object"] == "UNIT_CONVERSION_CERTIFICATE"
    assert derivation["object"] == "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION"

    factor = float(unit["unit_conversion"]["factor_to_canonical"])
    offset = float(unit["unit_conversion"]["offset_to_canonical"])

    baseline_raw = finite_vector(baseline["baseline_vector"]["values"])
    baseline_canonical = [x * factor + offset for x in baseline_raw]

    model_canonical = finite_vector(derivation["equivalent_lwe_model_vector_for_aligned_rerun"]["values"])

    assert len(baseline_canonical) == len(model_canonical)
    assert len(baseline_canonical) == derivation["equivalent_lwe_model_vector_for_aligned_rerun"]["vector_length"]

    diff = [b - m for b, m in zip(baseline_canonical, model_canonical)]
    n = len(diff)

    canonical_rmse = math.sqrt(sum(x * x for x in diff) / n)
    canonical_mae = sum(abs(x) for x in diff) / n
    canonical_mean_signed_error = sum(diff) / n
    canonical_max_abs_error = max(abs(x) for x in diff)

    runner_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    payload = {
        "artifact": "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_2026_06_01",
        "object": "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT",
        "status": "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_SUPPLIED_NO_EMPIRICAL_INTERPRETATION",
        "decision": "PASS",
        "depends_on": [
            "BASELINE_GRAVITY_VECTOR_2026_06_01",
            "UNIT_CONVERSION_CERTIFICATE_2026_06_01",
            "NON_NULL_PHYSICAL_MODEL_VECTOR_OR_DEFICIT_MASS_DERIVATION_2026_06_01"
        ],
        "metric_id": "canonical_rmse_between_aligned_vectors_v1",
        "primary_metric": "canonical_rmse",
        "metric_direction": "lower_is_better",
        "canonical_unit": unit["unit_conversion"]["canonical_unit"],
        "vector_length": n,
        "baseline_vector_sha256": baseline["baseline_vector"]["sha256"],
        "non_null_equivalent_lwe_vector_sha256": derivation["equivalent_lwe_model_vector_for_aligned_rerun"]["vector_sha256"],
        "surface_mass_density_vector_sha256": derivation["non_null_physical_model_vector_or_deficit_mass_derivation"]["vector_sha256"],
        "reproducible_run_script": "tools/run_non_null_model_comparison.py",
        "reproducible_run_script_sha256": runner_sha256,
        "canonical_rmse": float(f"{canonical_rmse:.17g}"),
        "canonical_mae": float(f"{canonical_mae:.17g}"),
        "canonical_mean_signed_error": float(f"{canonical_mean_signed_error:.17g}"),
        "canonical_max_abs_error": float(f"{canonical_max_abs_error:.17g}"),
        "run_output_supplied": True,
        "resolved_missing_input": "NonNullModelComparisonRunOutput",
        "certified_non_claims": [
            "non-null model comparison run output only",
            "model vector is derived from the observed LWE baseline",
            "not an independent predictive DFM-MKC model",
            "not a fitted model",
            "no empirical gravity result interpretation supplied",
            "no anomaly detection claim",
            "no model-favored result claim",
            "no baseline-favored result claim",
            "no DFM-MKC validation",
            "no Lambda-CDM failure",
            "no dark matter resolution",
            "no dark energy resolution",
            "no physical discovery claim",
            "no Chronos-RR closure",
            "no H4.1/FGL closure",
            "no P vs NP claim",
            "no Clay-problem claim"
        ],
        "next_admissible_object": "NON_NULL_MODEL_RESULT_INTERPRETATION",
        "weakest_sufficient_next_input": "NonNullModelResultInterpretation"
    }

    stable = json.dumps(payload, indent=2, sort_keys=True)
    payload["run_output_sha256"] = sha256_text(stable + "\n")

    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print("NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_WRITTEN")
    print(json.dumps({
        "artifact": str(OUT),
        "canonical_rmse": payload["canonical_rmse"],
        "canonical_mae": payload["canonical_mae"],
        "canonical_mean_signed_error": payload["canonical_mean_signed_error"],
        "canonical_max_abs_error": payload["canonical_max_abs_error"],
        "run_output_sha256": payload["run_output_sha256"],
        "next_admissible_object": payload["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

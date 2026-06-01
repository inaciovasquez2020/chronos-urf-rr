#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

ART = Path("artifacts/chronos/non_null_model_comparison_run_output_2026_06_01.json")
DOC = Path("docs/status/NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_2026_06_01.md")
RUNNER = Path("tools/run_non_null_model_comparison.py")
BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
DERIVATION = Path("artifacts/chronos/non_null_physical_model_vector_or_deficit_mass_derivation_2026_06_01.json")

REQUIRED_NON_CLAIMS = {
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
    "no Clay-problem claim",
}

FORBIDDEN_CLAIMS = [
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "ANOMALY_DETECTED_TRUE",
    "MODEL_FAVORED_RESULT_CLAIMED_TRUE",
    "DFM_MKC_VALIDATED_TRUE",
    "LAMBDA_CDM_FAILED_TRUE",
    "CLAY_CLOSED_TRUE"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert RUNNER.exists(), f"missing runner: {RUNNER}"
    assert BASELINE.exists(), f"missing baseline: {BASELINE}"
    assert DERIVATION.exists(), f"missing derivation: {DERIVATION}"

    data = json.loads(ART.read_text())
    baseline = json.loads(BASELINE.read_text())
    derivation = json.loads(DERIVATION.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_2026_06_01"
    assert data["object"] == "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT"
    assert data["status"] == "NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_SUPPLIED_NO_EMPIRICAL_INTERPRETATION"
    assert data["decision"] == "PASS"

    assert data["baseline_vector_sha256"] == baseline["baseline_vector"]["sha256"]
    assert data["non_null_equivalent_lwe_vector_sha256"] == derivation["equivalent_lwe_model_vector_for_aligned_rerun"]["vector_sha256"]
    assert data["surface_mass_density_vector_sha256"] == derivation["non_null_physical_model_vector_or_deficit_mass_derivation"]["vector_sha256"]
    assert data["vector_length"] == baseline["baseline_vector"]["length"]

    assert data["reproducible_run_script_sha256"] == hashlib.sha256(RUNNER.read_bytes()).hexdigest()

    for key in ["canonical_rmse", "canonical_mae", "canonical_mean_signed_error", "canonical_max_abs_error"]:
        assert isinstance(data[key], (int, float))
        assert math.isfinite(float(data[key]))

    assert data["run_output_supplied"] is True
    assert data["resolved_missing_input"] == "NonNullModelComparisonRunOutput"
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "NON_NULL_MODEL_RESULT_INTERPRETATION"
    assert data["weakest_sufficient_next_input"] == "NonNullModelResultInterpretation"

    print("NON_NULL_MODEL_COMPARISON_RUN_OUTPUT_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "canonical_rmse": data["canonical_rmse"],
        "canonical_mae": data["canonical_mae"],
        "run_output_sha256": data["run_output_sha256"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

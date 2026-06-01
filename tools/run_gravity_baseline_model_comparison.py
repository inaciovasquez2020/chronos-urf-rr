#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

AUTH = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")
COORD = Path("artifacts/chronos/coordinate_or_row_binding_certificate_2026_06_01.json")
BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
MODEL = Path("artifacts/chronos/model_or_deficit_mass_vector_2026_06_01.json")
UNIT = Path("artifacts/chronos/unit_conversion_certificate_2026_06_01.json")
METRIC = Path("artifacts/chronos/predeclared_comparison_metric_2026_06_01.json")
OUT = Path("artifacts/chronos/reproducible_comparison_run_output_2026_06_01.json")

def load(path: Path) -> dict:
    return json.loads(path.read_text())

def finite_float_vector(values):
    out = [float(x) for x in values]
    assert all(math.isfinite(x) for x in out)
    return out

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main() -> None:
    auth = load(AUTH)
    coord = load(COORD)
    baseline = load(BASELINE)
    model = load(MODEL)
    unit = load(UNIT)
    metric = load(METRIC)

    assert auth["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"
    assert coord["object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert baseline["object"] == "BASELINE_GRAVITY_VECTOR"
    assert model["object"] == "MODEL_OR_DEFICIT_MASS_VECTOR"
    assert unit["object"] == "UNIT_CONVERSION_CERTIFICATE"
    assert metric["object"] == "PREDECLARED_COMPARISON_METRIC"

    b = finite_float_vector(baseline["baseline_vector"]["values"])
    m = finite_float_vector(model["model_or_deficit_mass_vector"]["values"])

    assert len(b) == len(m)
    assert len(b) == metric["predeclared_metric"]["vector_length"]

    factor = float(metric["predeclared_metric"]["factor_to_canonical"])
    offset = float(metric["predeclared_metric"]["offset_to_canonical"])
    assert math.isfinite(factor) and factor > 0
    assert math.isfinite(offset)

    baseline_canonical = [x * factor + offset for x in b]
    model_canonical = [x * factor + offset for x in m]
    diff = [x - y for x, y in zip(baseline_canonical, model_canonical)]

    n = len(diff)
    squared = [x * x for x in diff]
    abs_diff = [abs(x) for x in diff]

    canonical_rmse = math.sqrt(sum(squared) / n)
    canonical_mae = sum(abs_diff) / n
    canonical_mean_signed_error = sum(diff) / n
    canonical_max_abs_error = max(abs_diff)

    runner_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    run_payload = {
        "artifact": "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_2026_06_01",
        "object": "REPRODUCIBLE_COMPARISON_RUN_OUTPUT",
        "status": "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_SUPPLIED_NO_EMPIRICAL_INTERPRETATION",
        "decision": "PASS",
        "depends_on": [
            "AUTHENTICATED_GRAVITY_PAYLOAD_2026_06_01",
            "COORDINATE_OR_ROW_BINDING_CERTIFICATE_2026_06_01",
            "BASELINE_GRAVITY_VECTOR_2026_06_01",
            "MODEL_OR_DEFICIT_MASS_VECTOR_2026_06_01",
            "UNIT_CONVERSION_CERTIFICATE_2026_06_01",
            "PREDECLARED_COMPARISON_METRIC_2026_06_01"
        ],
        "metric_id": metric["predeclared_metric"]["metric_id"],
        "primary_metric": metric["predeclared_metric"]["primary_metric"],
        "metric_direction": metric["predeclared_metric"]["metric_direction"],
        "canonical_unit": metric["predeclared_metric"]["canonical_unit"],
        "factor_to_canonical": factor,
        "offset_to_canonical": offset,
        "vector_length": n,
        "baseline_vector_sha256": baseline["baseline_vector"]["sha256"],
        "model_or_deficit_mass_vector_sha256": model["model_or_deficit_mass_vector"]["sha256"],
        "unit_conversion_artifact": unit["artifact"],
        "predeclared_metric_artifact": metric["artifact"],
        "reproducible_run_script": "tools/run_gravity_baseline_model_comparison.py",
        "reproducible_run_script_sha256": runner_sha256,
        "canonical_rmse": float(f"{canonical_rmse:.17g}"),
        "canonical_mae": float(f"{canonical_mae:.17g}"),
        "canonical_mean_signed_error": float(f"{canonical_mean_signed_error:.17g}"),
        "canonical_max_abs_error": float(f"{canonical_max_abs_error:.17g}"),
        "run_output_supplied": True,
        "resolved_missing_input": "reproducible_comparison_run_output",
        "remaining_missing_inputs": [],
        "remaining_missing_input_count": 0,
        "certified_non_claims": [
            "reproducible comparison run output only",
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
        "next_admissible_object": "GRAVITY_BASELINE_VS_MODEL_COMPARISON_RESULT_INTERPRETATION",
        "weakest_sufficient_next_input": "GravityBaselineVsModelComparisonResultInterpretation"
    }

    stable = json.dumps(run_payload, indent=2, sort_keys=True)
    run_payload["run_output_sha256"] = sha256_text(stable + "\n")
    OUT.write_text(json.dumps(run_payload, indent=2, sort_keys=True) + "\n")

    print("REPRODUCIBLE_COMPARISON_RUN_OUTPUT_WRITTEN")
    print(json.dumps({
        "artifact": str(OUT),
        "metric_id": run_payload["metric_id"],
        "vector_length": n,
        "canonical_rmse": run_payload["canonical_rmse"],
        "canonical_mae": run_payload["canonical_mae"],
        "canonical_mean_signed_error": run_payload["canonical_mean_signed_error"],
        "canonical_max_abs_error": run_payload["canonical_max_abs_error"],
        "run_output_sha256": run_payload["run_output_sha256"],
        "next_admissible_object": run_payload["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

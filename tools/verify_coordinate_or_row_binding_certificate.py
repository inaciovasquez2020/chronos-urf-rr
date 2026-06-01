#!/usr/bin/env python3
import json
import re
from pathlib import Path

ART = Path("artifacts/chronos/coordinate_or_row_binding_certificate_2026_06_01.json")
DOC = Path("docs/status/COORDINATE_OR_ROW_BINDING_CERTIFICATE_2026_06_01.md")
AUTH = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")

EXPECTED_REMAINING = {
    "baseline_gravity_vector",
    "model_or_deficit_mass_vector",
    "unit_conversion_certificate",
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
}

REQUIRED_NON_CLAIMS = {
    "coordinate and row binding only",
    "payload bytes are local external data and are not committed to git",
    "no baseline gravity vector supplied",
    "no model or deficit-mass vector supplied",
    "no unit conversion certificate supplied",
    "no predeclared comparison metric supplied",
    "no reproducible comparison run output supplied",
    "no empirical gravity result supplied",
    "no anomaly detection result",
    "no model-favored result",
    "no baseline-favored result",
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
    "BASELINE_GRAVITY_VECTOR_SUPPLIED_TRUE",
    "MODEL_VECTOR_SUPPLIED_TRUE",
    "UNIT_CONVERSION_CERTIFICATE_SUPPLIED_TRUE",
    "PREDECLARED_COMPARISON_METRIC_SUPPLIED_TRUE",
    "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_SUPPLIED_TRUE",
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "ANOMALY_DETECTED",
    "DFM_MKC_VALIDATED",
    "LAMBDA_CDM_FAILED",
    "CLAY_CLOSED"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert AUTH.exists(), f"missing authenticated payload artifact: {AUTH}"

    data = json.loads(ART.read_text())
    auth = json.loads(AUTH.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE_2026_06_01"
    assert data["object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert data["status"] == "COORDINATE_ROW_BINDING_CERTIFICATE_SUPPLIED_FROM_LOCAL_NETCDF_METADATA"
    assert data["decision"] == "PASS"

    assert auth["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"
    assert auth["decision"] == "PASS"
    assert data["source_payload"]["sha256"] == auth["sha256"]
    assert data["source_payload"]["byte_count"] == auth["byte_count"]
    assert data["source_payload"]["payload_bytes_committed_to_git"] is False

    assert re.fullmatch(r"[0-9a-f]{64}", data["source_payload"]["sha256"])
    assert data["netcdf_dimensions"]
    assert data["netcdf_variable_count"] >= 1
    assert data["coordinate_variables"]
    assert data["data_variables"]
    assert data["variable_bindings"]

    for name in data["coordinate_variables"]:
        assert name in data["variable_bindings"], f"missing coordinate binding: {name}"
        assert "dimensions" in data["variable_bindings"][name]
        assert "shape" in data["variable_bindings"][name]

    for name in data["data_variables"]:
        assert name in data["variable_bindings"], f"missing data binding: {name}"
        assert "dimensions" in data["variable_bindings"][name]
        assert "shape" in data["variable_bindings"][name]

    assert data["row_binding_rule"]["kind"] == "netCDF dimension-order binding"
    assert data["resolved_missing_input"] == "coordinate_or_row_binding_certificate"
    assert set(data["remaining_missing_inputs"]) == EXPECTED_REMAINING
    assert data["remaining_missing_input_count"] == 5
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in EXPECTED_REMAINING:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "BASELINE_GRAVITY_VECTOR"
    assert data["weakest_sufficient_next_input"] == "BaselineGravityVector"

    print("COORDINATE_OR_ROW_BINDING_CERTIFICATE_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "dimension_count": len(data["netcdf_dimensions"]),
        "coordinate_variable_count": len(data["coordinate_variables"]),
        "data_variable_count": len(data["data_variables"]),
        "resolved_missing_input": data["resolved_missing_input"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

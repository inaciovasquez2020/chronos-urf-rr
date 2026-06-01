#!/usr/bin/env python3
import hashlib
import json
import math
import re
from pathlib import Path

ART = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
DOC = Path("docs/status/BASELINE_GRAVITY_VECTOR_2026_06_01.md")
AUTH = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")
COORD = Path("artifacts/chronos/coordinate_or_row_binding_certificate_2026_06_01.json")

EXPECTED_REMAINING = {
    "model_or_deficit_mass_vector",
    "unit_conversion_certificate",
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
}

REQUIRED_NON_CLAIMS = {
    "baseline gravity vector only",
    "deterministic finite sample only",
    "payload bytes are local external data and are not committed to git",
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
    assert COORD.exists(), f"missing coordinate binding artifact: {COORD}"

    data = json.loads(ART.read_text())
    auth = json.loads(AUTH.read_text())
    coord = json.loads(COORD.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "BASELINE_GRAVITY_VECTOR_2026_06_01"
    assert data["object"] == "BASELINE_GRAVITY_VECTOR"
    assert data["status"] == "BASELINE_GRAVITY_VECTOR_SUPPLIED_FROM_AUTHENTICATED_NETCDF_PAYLOAD_DETERMINISTIC_FINITE_SAMPLE"
    assert data["decision"] == "PASS"

    assert auth["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"
    assert coord["object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert data["source_payload"]["sha256"] == auth["sha256"]
    assert data["source_payload"]["byte_count"] == auth["byte_count"]
    assert data["source_payload"]["payload_bytes_committed_to_git"] is False

    vec = data["baseline_vector"]
    assert vec["length"] == len(vec["values"])
    assert vec["length"] > 0
    assert vec["length"] <= 4096
    assert re.fullmatch(r"[0-9a-f]{64}", vec["sha256"])

    vector_text = "\n".join(f"{float(x):.12g}" for x in vec["values"]) + "\n"
    assert hashlib.sha256(vector_text.encode("utf-8")).hexdigest() == vec["sha256"]

    for key in ["min", "max", "mean", "std"]:
        assert isinstance(vec[key], (int, float))
        assert math.isfinite(float(vec[key]))

    assert data["baseline_variable"]["name"]
    assert data["baseline_variable"]["dimensions"]
    assert data["baseline_variable"]["shape"]

    assert data["baseline_vector_rule"]["kind"] == "deterministic finite sample from authenticated netCDF numeric data variable"
    assert data["resolved_missing_input"] == "baseline_gravity_vector"
    assert set(data["remaining_missing_inputs"]) == EXPECTED_REMAINING
    assert data["remaining_missing_input_count"] == 4
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in EXPECTED_REMAINING:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "MODEL_OR_DEFICIT_MASS_VECTOR"
    assert data["weakest_sufficient_next_input"] == "ModelOrDeficitMassVector"

    print("BASELINE_GRAVITY_VECTOR_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "baseline_variable": data["baseline_variable"]["name"],
        "baseline_vector_length": vec["length"],
        "baseline_vector_sha256": vec["sha256"],
        "resolved_missing_input": data["resolved_missing_input"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

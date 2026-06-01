#!/usr/bin/env python3
import hashlib
import json
import math
import re
from pathlib import Path

ART = Path("artifacts/chronos/model_or_deficit_mass_vector_2026_06_01.json")
DOC = Path("docs/status/MODEL_OR_DEFICIT_MASS_VECTOR_2026_06_01.md")
BASELINE = Path("artifacts/chronos/baseline_gravity_vector_2026_06_01.json")
COORD = Path("artifacts/chronos/coordinate_or_row_binding_certificate_2026_06_01.json")
AUTH = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")

EXPECTED_REMAINING = {
    "unit_conversion_certificate",
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
}

REQUIRED_NON_CLAIMS = {
    "model or deficit-mass vector only",
    "aligned zero null vector only",
    "not a DFM-MKC physical model vector",
    "not a derived deficit-mass field",
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
    "UNIT_CONVERSION_CERTIFICATE_SUPPLIED_TRUE",
    "PREDECLARED_COMPARISON_METRIC_SUPPLIED_TRUE",
    "REPRODUCIBLE_COMPARISON_RUN_OUTPUT_SUPPLIED_TRUE",
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "ANOMALY_DETECTED",
    "MODEL_FAVORED_RESULT_CLAIMED",
    "BASELINE_FAVORED_RESULT_CLAIMED",
    "DFM_MKC_VALIDATED",
    "LAMBDA_CDM_FAILED",
    "CLAY_CLOSED"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert BASELINE.exists(), f"missing baseline artifact: {BASELINE}"
    assert COORD.exists(), f"missing coordinate artifact: {COORD}"
    assert AUTH.exists(), f"missing authenticated payload artifact: {AUTH}"

    data = json.loads(ART.read_text())
    baseline = json.loads(BASELINE.read_text())
    coord = json.loads(COORD.read_text())
    auth = json.loads(AUTH.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "MODEL_OR_DEFICIT_MASS_VECTOR_2026_06_01"
    assert data["object"] == "MODEL_OR_DEFICIT_MASS_VECTOR"
    assert data["status"] == "MODEL_OR_DEFICIT_MASS_VECTOR_SUPPLIED_AS_ALIGNED_ZERO_NULL_VECTOR"
    assert data["decision"] == "PASS"

    assert baseline["object"] == "BASELINE_GRAVITY_VECTOR"
    assert coord["object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert auth["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"

    vec = data["model_or_deficit_mass_vector"]
    base_vec = baseline["baseline_vector"]

    assert vec["length"] == len(vec["values"])
    assert vec["length"] == base_vec["length"]
    assert vec["length"] > 0
    assert all(float(x) == 0.0 for x in vec["values"])
    assert re.fullmatch(r"[0-9a-f]{64}", vec["sha256"])

    vector_text = "\n".join(f"{float(x):.12g}" for x in vec["values"]) + "\n"
    assert hashlib.sha256(vector_text.encode("utf-8")).hexdigest() == vec["sha256"]

    for key in ["min", "max", "mean", "std"]:
        assert isinstance(vec[key], (int, float))
        assert math.isfinite(float(vec[key]))
        assert float(vec[key]) == 0.0

    assert data["model_or_deficit_mass_vector_rule"]["kind"] == "aligned zero null vector"
    assert data["resolved_missing_input"] == "model_or_deficit_mass_vector"
    assert set(data["remaining_missing_inputs"]) == EXPECTED_REMAINING
    assert data["remaining_missing_input_count"] == 3
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in EXPECTED_REMAINING:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "UNIT_CONVERSION_CERTIFICATE"
    assert data["weakest_sufficient_next_input"] == "UnitConversionCertificate"

    print("MODEL_OR_DEFICIT_MASS_VECTOR_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "vector_length": vec["length"],
        "vector_sha256": vec["sha256"],
        "resolved_missing_input": data["resolved_missing_input"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

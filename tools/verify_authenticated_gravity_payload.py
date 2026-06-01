#!/usr/bin/env python3
import json
import re
from pathlib import Path

ART = Path("artifacts/chronos/authenticated_gravity_payload_2026_06_01.json")
DOC = Path("docs/status/AUTHENTICATED_GRAVITY_PAYLOAD_2026_06_01.md")
PRIOR = Path("artifacts/chronos/gravity_empirical_result_inputs_missing_certificate_2026_06_01.json")

EXPECTED_REMAINING = {
    "coordinate_or_row_binding_certificate",
    "baseline_gravity_vector",
    "model_or_deficit_mass_vector",
    "unit_conversion_certificate",
    "predeclared_comparison_metric",
    "reproducible_comparison_run_output",
}

REQUIRED_NON_CLAIMS = {
    "payload bytes are local external data and are not committed to git",
    "no coordinate or row binding certificate supplied",
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
    "EMPIRICAL_GRAVITY_RESULT_SUPPLIED_TRUE",
    "GRAVITY_COMPARISON_CLOSED",
    "MODEL_FAVORED_RESULT_CLAIMED",
    "BASELINE_FAVORED_RESULT_CLAIMED",
    "ANOMALY_DETECTED",
    "DFM_MKC_VALIDATED",
    "LAMBDA_CDM_FAILED",
    "DARK_MATTER_RESOLVED",
    "DARK_ENERGY_RESOLVED",
    "CLAY_CLOSED"
]

def main() -> None:
    assert ART.exists(), f"missing artifact: {ART}"
    assert DOC.exists(), f"missing doc: {DOC}"
    assert PRIOR.exists(), f"missing prior artifact: {PRIOR}"

    data = json.loads(ART.read_text())
    prior = json.loads(PRIOR.read_text())
    doc = DOC.read_text()
    joined = json.dumps(data, sort_keys=True) + "\n" + doc

    assert data["artifact"] == "AUTHENTICATED_GRAVITY_PAYLOAD_2026_06_01"
    assert data["object"] == "AUTHENTICATED_GRAVITY_PAYLOAD"
    assert data["status"] == "AUTHENTICATED_PO_DAAC_GRACE_GRACE_FO_MASCON_PAYLOAD_DIGEST_BOUND_LOCAL_BYTES_NOT_COMMITTED"
    assert data["decision"] == "PASS"

    assert prior["object"] == "GRAVITY_EMPIRICAL_RESULT_INPUTS_MISSING_CERTIFICATE"
    assert prior["status"] == "EXPLICIT_EMPIRICAL_INPUTS_MISSING_NO_RESULT_SUPPLIED"
    assert "authenticated_gravity_payload" in prior["missing_inputs"]

    assert data["source_agency"] == "NASA/JPL PO.DAAC"
    assert data["provider"] == "POCLOUD"
    assert data["mission"] == "GRACE/GRACE-FO"
    assert data["dataset_short_name"] == "TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4"
    assert data["granule_filename"] == "GRCTellus.JPL.200204_202603.GLO.RL06.3M.MSCNv04CRI.nc"
    assert data["payload_format"] == "netCDF"
    assert data["payload_bytes_committed_to_git"] is False

    assert re.fullmatch(r"[0-9a-f]{64}", data["sha256"])
    assert data["sha256"] == "6554527f30e77923eae9f9793bcb315577551ad86ed763aa8a86110df463fd29"
    assert data["byte_count"] == 45289360
    assert data["downloaded_files"] == 1
    assert data["failed_files"] == 0
    assert data["success_count"] == 1

    assert data["resolved_missing_input"] == "authenticated_gravity_payload"
    assert set(data["remaining_missing_inputs"]) == EXPECTED_REMAINING
    assert data["remaining_missing_input_count"] == 6
    assert REQUIRED_NON_CLAIMS.issubset(set(data["certified_non_claims"]))

    for token in EXPECTED_REMAINING:
        assert token in doc

    for token in REQUIRED_NON_CLAIMS:
        assert token in doc

    for claim in FORBIDDEN_CLAIMS:
        assert claim not in joined, f"forbidden claim present: {claim}"

    assert data["next_admissible_object"] == "COORDINATE_OR_ROW_BINDING_CERTIFICATE"
    assert data["weakest_sufficient_next_input"] == "CoordinateOrRowBindingCertificate"

    print("AUTHENTICATED_GRAVITY_PAYLOAD_OK")
    print(json.dumps({
        "artifact": str(ART),
        "decision": data["decision"],
        "status": data["status"],
        "dataset_short_name": data["dataset_short_name"],
        "granule_filename": data["granule_filename"],
        "sha256": data["sha256"],
        "byte_count": data["byte_count"],
        "resolved_missing_input": data["resolved_missing_input"],
        "remaining_missing_input_count": data["remaining_missing_input_count"],
        "next_admissible_object": data["next_admissible_object"]
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

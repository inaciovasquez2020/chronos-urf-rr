#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_trace_pairing_discharge_lemma_2026_06_15.json"
)

EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_TRACE_PAIRING_DISCHARGE_LEMMA"
EXPECTED_PREDECESSOR = "RESTRICTED_CONTINUATION_NORMAL_TRACE_EXISTENCE_DISCHARGE_LEMMA"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_PAIRING_DISCHARGE_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "restricted_continuation_trace_pairing_discharge_lemma"
    assert data["date"] == "2026-06-15"
    assert data["solves"] == EXPECTED_SOLVES
    assert data["predecessor"] == EXPECTED_PREDECESSOR
    assert data["type"] == "conditional_discharge_lemma"

    lemma = data["lemma_statement"]
    assert lemma["name"] == "restricted_continuation_trace_pairing_discharge_lemma"
    assert "trace pairing" in lemma["claim"]
    assert "scalar boundary trace" in lemma["claim"]
    assert "normal trace" in lemma["claim"]
    assert lemma["domain"] == "restricted continuation region"
    assert lemma["boundary"] == "partial Sigma_R"
    assert lemma["pairing_object"] == "restricted_continuation_trace_pairing"

    required = data["required_inputs"]
    names = {item["name"] for item in required}
    assert "restricted_continuation_boundary_trace_exists" in names
    assert "restricted_continuation_normal_trace_exists" in names
    assert "boundary_trace_space_duality_compatible" in names
    assert "trace_pairing_operator_available" in names
    assert "boundary_measure_orientation_compatible" in names
    assert all(item["role"] for item in required)

    discharged = data["discharged_obligations"]
    assert any("trace pairing" in item for item in discharged)
    assert any("boundary trace existence" in item for item in discharged)
    assert any("normal trace existence" in item for item in discharged)
    assert any("conditional discharge lemma" in item for item in discharged)

    non_claims = data["non_claims"]
    assert "Does not prove boundary flux pairing." in non_claims
    assert "Does not prove integration by parts." in non_claims
    assert "Does not identify the trace pairing with the physical boundary flux term." in non_claims
    assert "Does not prove flux sign control." in non_claims
    assert "Does not prove full RR closure." in non_claims

    assert data["next_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    print("RUNALL_RESTRICTED_CONTINUATION_TRACE_PAIRING_DISCHARGE_LEMMA_OK")


if __name__ == "__main__":
    main()

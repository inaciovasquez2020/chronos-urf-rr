#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_restricted_integration_by_parts_discharge_lemma_2026_06_15.json"
)

EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_RESTRICTED_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA"
EXPECTED_PREDECESSOR = "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_COERCIVITY_DISCHARGE_LEMMA"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_ENERGY_IDENTITY_DISCHARGE_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "restricted_continuation_restricted_integration_by_parts_discharge_lemma"
    assert data["date"] == "2026-06-15"
    assert data["solves"] == EXPECTED_SOLVES
    assert data["predecessor"] == EXPECTED_PREDECESSOR
    assert data["type"] == "conditional_discharge_lemma"

    lemma = data["lemma_statement"]
    assert lemma["name"] == "restricted_continuation_restricted_integration_by_parts_discharge_lemma"
    assert "integration-by-parts identity" in lemma["claim"]
    assert "interior regularity" in lemma["claim"]
    assert "boundary-flux pairing" in lemma["claim"]
    assert lemma["domain"] == "restricted continuation region"
    assert lemma["boundary"] == "partial Sigma_R"
    assert lemma["identity_object"] == "restricted_continuation_integration_by_parts_identity"

    required = data["required_inputs"]
    names = {item["name"] for item in required}
    assert "state_spatial_regularitiy_on_restricted_region" in names
    assert "restricted_continuation_boundary_trace_exists" in names
    assert "restricted_continuation_normal_trace_exists" in names
    assert "restricted_continuation_boundary_flux_pairing_exists" in names
    assert "restricted_boundary_orientation_matches_divergence_theorem" in names
    assert "interior_boundary_decomposition_has_no_uncontrolled_remainder" in names
    assert all(item["role"] for item in required)

    discharged = data["discharged_obligations"]
    assert any("restricted integration by parts" in item for item in discharged)
    assert any("boundary trace existence" in item for item in discharged)
    assert any("normal trace existence" in item for item in discharged)
    assert any("boundary flux pairing" in item for item in discharged)
    assert any("conditional discharge lemma" in item for item in discharged)

    non_claims = data["non_claims"]
    assert "Does not prove the energy identity." in non_claims
    assert "Does not prove the energy inequality." in non_claims
    assert "Does not prove source-term absorption." in non_claims
    assert "Does not prove continuation or contradiction." in non_claims
    assert "Does not prove full RR closure." in non_claims

    assert data["next_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    print("RUNALL_RESTRICTED_CONTINUATION_RESTRICTED_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA_OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_boundary_flux_sign_control_discharge_lemma_2026_06_15.json"
)

EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_SIGN_CONTROL_DISCHARGE_LEMMA"
EXPECTED_PREDECESSOR = "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_PAIRING_DISCHARGE_LEMMA"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_COERCIVITY_DISCHARGE_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "restricted_continuation_boundary_flux_sign_control_discharge_lemma"
    assert data["date"] == "2026-06-15"
    assert data["solves"] == EXPECTED_SOLVES
    assert data["predecessor"] == EXPECTED_PREDECESSOR
    assert data["type"] == "conditional_discharge_lemma"

    lemma = data["lemma_statement"]
    assert lemma["name"] == "restricted_continuation_boundary_flux_sign_control_discharge_lemma"
    assert "boundary flux pairing" in lemma["claim"]
    assert "sign control" in lemma["claim"]
    assert "outward-orientation" in lemma["claim"]
    assert lemma["domain"] == "restricted continuation region"
    assert lemma["boundary"] == "partial Sigma_R"
    assert lemma["controlled_object"] == "restricted_continuation_boundary_flux_pairing"
    assert lemma["sign_control_object"] == "restricted_continuation_boundary_flux_sign_control"

    required = data["required_inputs"]
    names = {item["name"] for item in required}
    assert "restricted_continuation_boundary_flux_pairing_exists" in names
    assert "outward_normal_orientation_matches_energy_identity" in names
    assert "flux_payload_has_boundary_dissipativity_sign" in names
    assert "restricted_boundary_support_excludes_uncontrolled_faces" in names
    assert "boundary_flux_sign_control_operator_available" in names
    assert all(item["role"] for item in required)

    discharged = data["discharged_obligations"]
    assert any("boundary flux sign control" in item for item in discharged)
    assert any("boundary flux pairing existence" in item for item in discharged)
    assert any("required sign" in item for item in discharged)
    assert any("conditional discharge lemma" in item for item in discharged)

    non_claims = data["non_claims"]
    assert "Does not prove flux coercivity." in non_claims
    assert "Does not prove restricted integration by parts." in non_claims
    assert "Does not prove the energy inequality." in non_claims
    assert "Does not prove continuation or contradiction." in non_claims
    assert "Does not prove full RR closure." in non_claims

    assert data["next_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    print("RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_FLUX_SIGN_CONTROL_DISCHARGE_LEMMA_OK")


if __name__ == "__main__":
    main()

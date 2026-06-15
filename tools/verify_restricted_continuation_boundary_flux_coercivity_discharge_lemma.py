#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_boundary_flux_coercivity_discharge_lemma_2026_06_15.json"
)

EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_COERCIVITY_DISCHARGE_LEMMA"
EXPECTED_PREDECESSOR = "RESTRICTED_CONTINUATION_BOUNDARY_FLUX_SIGN_CONTROL_DISCHARGE_LEMMA"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_RESTRICTED_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "restricted_continuation_boundary_flux_coercivity_discharge_lemma"
    assert data["date"] == "2026-06-15"
    assert data["solves"] == EXPECTED_SOLVES
    assert data["predecessor"] == EXPECTED_PREDECESSOR
    assert data["type"] == "conditional_discharge_lemma"

    lemma = data["lemma_statement"]
    assert lemma["name"] == "restricted_continuation_boundary_flux_coercivity_discharge_lemma"
    assert "boundary flux pairing" in lemma["claim"]
    assert "coercive boundary control" in lemma["claim"]
    assert "coercivity constant" in lemma["claim"]
    assert lemma["domain"] == "restricted continuation region"
    assert lemma["boundary"] == "partial Sigma_R"
    assert lemma["controlled_object"] == "restricted_continuation_boundary_flux_pairing"
    assert lemma["coercivity_object"] == "restricted_continuation_boundary_flux_coercivity"

    required = data["required_inputs"]
    names = {item["name"] for item in required}
    assert "restricted_continuation_boundary_flux_sign_control_exists" in names
    assert "boundary_flux_coercivity_constant_positive" in names
    assert "boundary_trace_norm_matches_energy_boundary_norm" in names
    assert "coercive_flux_lower_bound_available" in names
    assert "restricted_boundary_support_contains_only_coercive_faces" in names
    assert all(item["role"] for item in required)

    discharged = data["discharged_obligations"]
    assert any("boundary flux coercivity" in item for item in discharged)
    assert any("boundary flux sign control" in item for item in discharged)
    assert any("quantitative coercive control" in item for item in discharged)
    assert any("conditional discharge lemma" in item for item in discharged)

    non_claims = data["non_claims"]
    assert "Does not prove restricted integration by parts." in non_claims
    assert "Does not prove the energy inequality." in non_claims
    assert "Does not prove continuation or contradiction." in non_claims
    assert "Does not prove source-term absorption." in non_claims
    assert "Does not prove full RR closure." in non_claims

    assert data["next_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    print("RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_FLUX_COERCIVITY_DISCHARGE_LEMMA_OK")


if __name__ == "__main__":
    main()

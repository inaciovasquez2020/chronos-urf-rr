#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_boundary_sign_condition_payload_2026_06_15.json"
)

EXPECTED_ID = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_CONDITION_PAYLOAD"
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_BOUNDARY_SIGN_CONDITION_PAYLOAD"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_SELECTED_TRACE_FLUX_WITNESS_BRANCH"
)
EXPECTED_STATUS = "PAYLOAD_SURFACE_ONLY_BOUNDARY_SIGN_CONDITION_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_BOUNDARY_ORIENTATION_COMPATIBILITY_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    payload = data["payload_statement"]
    assert payload["name"] == "restricted_continuation_boundary_sign_condition_payload"
    assert payload["selected_branch"] == "boundary_sign"

    required = payload["required_inputs"]
    assert "oriented_boundary_flux_term" in required
    assert "restricted_boundary_orientation" in required
    assert "declared_boundary_sign_condition" in required
    assert "boundary_flux_pairing_well_defined_on_restricted_boundary" in required

    sign_payload = payload["declared_sign_payload"]
    assert sign_payload["condition"] == (
        "oriented_boundary_flux_term_is_nonpositive_or_absorbable_on_the_restricted_boundary"
    )
    assert sign_payload["scope"] == "restricted_continuation_boundary_only"
    assert sign_payload["role"] == (
        "prevents_the_selected_boundary_sign_branch_from_contributing_uncontrolled_positive_energy"
    )

    intended = payload["intended_conclusion"]
    assert "the_boundary_sign_condition_payload_is_declared" in intended
    assert "the_selected_trace_flux_witness_branch_has_a_sign_condition_input" in intended
    assert "orientation_compatibility_is_now_the_next_required_boundary_flux_check" in intended

    negative = data["claim"]["negative"]
    assert "Does not prove the boundary sign condition." in negative
    assert "Does not prove restricted boundary orientation compatibility." in negative
    assert "Does not prove the boundary flux pairing exists." in negative
    assert "Does not prove signed flux is nonpositive or absorbable." in negative
    assert "Does not close the restricted energy inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_CONDITION_PAYLOAD_OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_boundary_orientation_compatibility_lemma_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_ORIENTATION_COMPATIBILITY_LEMMA"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_BOUNDARY_ORIENTATION_COMPATIBILITY_LEMMA"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_CONDITION_PAYLOAD"
)
EXPECTED_STATUS = "LEMMA_SURFACE_ONLY_BOUNDARY_ORIENTATION_COMPATIBILITY_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_SIGNED_FLUX_NONPOSITIVE_OR_ABSORBABLE_PAYLOAD"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    lemma = data["lemma_statement"]
    assert lemma["name"] == "restricted_continuation_boundary_orientation_compatibility"
    assert lemma["selected_branch"] == "boundary_sign"

    required = lemma["required_inputs"]
    assert "restricted_boundary_orientation" in required
    assert "oriented_boundary_flux_term" in required
    assert "declared_boundary_sign_condition" in required
    assert "boundary_flux_pairing_well_defined_on_restricted_boundary" in required

    compatibility = lemma["compatibility_payload"]
    assert "restricted_boundary_orientation_matches_the_flux_sign_convention" in compatibility
    assert "no_orientation_reversal_changes_the_declared_boundary_sign_condition" in compatibility
    assert (
        "oriented_boundary_flux_term_is_interpreted_with_the_selected_restricted_boundary_orientation"
        in compatibility
    )

    intended = lemma["intended_conclusion"]
    assert (
        "the_boundary_sign_condition_uses_the_same_orientation_as_the_restricted_flux_pairing"
        in intended
    )
    assert "the_selected_boundary_sign_branch_has_orientation-compatible_input" in intended
    assert (
        "signed_flux_nonpositive_or_absorbable_payload_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove restricted boundary orientation compatibility." in negative
    assert "Does not prove the boundary sign condition." in negative
    assert "Does not prove the boundary flux pairing exists." in negative
    assert "Does not prove signed flux is nonpositive or absorbable." in negative
    assert "Does not close the restricted energy inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_ORIENTATION_COMPATIBILITY_LEMMA_OK")


if __name__ == "__main__":
    main()

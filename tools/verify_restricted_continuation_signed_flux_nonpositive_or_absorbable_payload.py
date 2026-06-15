#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_signed_flux_nonpositive_or_absorbable_payload_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_SIGNED_FLUX_NONPOSITIVE_OR_ABSORBABLE_PAYLOAD"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_SIGNED_FLUX_NONPOSITIVE_OR_ABSORBABLE_PAYLOAD"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_ORIENTATION_COMPATIBILITY_LEMMA"
)
EXPECTED_STATUS = "PAYLOAD_SURFACE_ONLY_SIGNED_FLUX_NONPOSITIVE_OR_ABSORBABLE_NOT_PROVED"
EXPECTED_NEXT = (
    "RESTRICTED_CONTINUATION_BOUNDARY_SIGN_BRANCH_ENERGY_INEQUALITY_INSERTION_LEMMA"
)


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
    assert payload["name"] == (
        "restricted_continuation_signed_flux_nonpositive_or_absorbable_payload"
    )
    assert payload["selected_branch"] == "boundary_sign"

    required = payload["required_inputs"]
    assert "oriented_boundary_flux_term" in required
    assert (
        "restricted_boundary_orientation_compatible_with_flux_sign_convention"
        in required
    )
    assert "declared_boundary_sign_condition" in required
    assert "boundary_flux_pairing_well_defined_on_restricted_boundary" in required

    alternatives = payload["signed_flux_alternatives"]
    assert len(alternatives) == 2
    modes = {alternative["mode"] for alternative in alternatives}
    assert modes == {"nonpositive", "absorbable"}

    nonpositive = next(
        alternative for alternative in alternatives if alternative["mode"] == "nonpositive"
    )
    absorbable = next(
        alternative for alternative in alternatives if alternative["mode"] == "absorbable"
    )

    assert nonpositive["condition"] == (
        "oriented_boundary_flux_term_is_less_than_or_equal_to_zero_on_the_restricted_boundary"
    )
    assert nonpositive["intended_effect"] == (
        "boundary_flux_can_be_dropped_from_the_upper_energy_bound"
    )

    assert absorbable["condition"] == (
        "oriented_boundary_flux_term_is_bounded_by_terms_absorbable_into_the_restricted_energy_inequality"
    )
    assert absorbable["intended_effect"] == (
        "boundary_flux_can_be_moved_into_the_controlled_side_of_the_energy_estimate"
    )

    intended = payload["intended_conclusion"]
    assert "one_signed_flux_control_mode_is_declared" in intended
    assert (
        "the_selected_boundary_sign_branch_has_a_signed_flux_control_payload"
        in intended
    )
    assert (
        "boundary_sign_branch_insertion_into_the_restricted_energy_inequality_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove signed flux is nonpositive." in negative
    assert "Does not prove signed flux is absorbable." in negative
    assert "Does not prove the boundary flux pairing exists." in negative
    assert "Does not prove the restricted energy inequality insertion step." in negative
    assert "Does not close the restricted energy inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_SIGNED_FLUX_NONPOSITIVE_OR_ABSORBABLE_PAYLOAD_OK")


if __name__ == "__main__":
    main()

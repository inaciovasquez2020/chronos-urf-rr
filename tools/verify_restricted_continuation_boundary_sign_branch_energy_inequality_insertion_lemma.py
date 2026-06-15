#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_boundary_sign_branch_energy_inequality_insertion_lemma_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_BRANCH_ENERGY_INEQUALITY_INSERTION_LEMMA"
)
EXPECTED_SOLVES = (
    "RESTRICTED_CONTINUATION_BOUNDARY_SIGN_BRANCH_ENERGY_INEQUALITY_INSERTION_LEMMA"
)
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_SIGNED_FLUX_NONPOSITIVE_OR_ABSORBABLE_PAYLOAD"
)
EXPECTED_STATUS = (
    "LEMMA_SURFACE_ONLY_BOUNDARY_SIGN_BRANCH_ENERGY_INEQUALITY_INSERTION_NOT_PROVED"
)
EXPECTED_NEXT = (
    "RESTRICTED_CONTINUATION_BOUNDARY_TERM_DISCHARGE_IN_RESTRICTED_ENERGY_INEQUALITY"
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

    lemma = data["lemma_statement"]
    assert lemma["name"] == (
        "restricted_continuation_boundary_sign_branch_energy_inequality_insertion"
    )
    assert lemma["selected_branch"] == "boundary_sign"

    required = lemma["required_inputs"]
    assert "oriented_boundary_flux_term" in required
    assert (
        "restricted_boundary_orientation_compatible_with_flux_sign_convention"
        in required
    )
    assert "declared_boundary_sign_condition" in required
    assert "signed_flux_nonpositive_or_absorbable_payload" in required
    assert "restricted_energy_identity_after_integration_by_parts" in required

    insertion_modes = lemma["insertion_modes"]
    assert len(insertion_modes) == 2
    modes = {mode["mode"] for mode in insertion_modes}
    assert modes == {"nonpositive_drop", "absorbable_transfer"}

    nonpositive = next(
        mode for mode in insertion_modes if mode["mode"] == "nonpositive_drop"
    )
    absorbable = next(
        mode for mode in insertion_modes if mode["mode"] == "absorbable_transfer"
    )

    assert nonpositive["insertion_rule"] == (
        "drop_the_nonpositive_boundary_flux_from_the_upper_energy_bound"
    )
    assert absorbable["insertion_rule"] == (
        "move_the_absorbable_boundary_flux_terms_to_the_controlled_side_of_the_energy_estimate"
    )

    intended = lemma["intended_conclusion"]
    assert (
        "the_selected_boundary_sign_branch_can_be_inserted_into_the_restricted_energy_inequality"
        in intended
    )
    assert (
        "no_uncontrolled_positive_boundary_flux_term_remains_after_the_selected_insertion_rule"
        in intended
    )
    assert (
        "restricted_energy_inequality_boundary_term_discharge_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert (
        "Does not prove the restricted energy identity after integration by parts."
        in negative
    )
    assert "Does not prove the insertion rule." in negative
    assert (
        "Does not discharge the boundary term in the restricted energy inequality."
        in negative
    )
    assert "Does not close the restricted energy inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print(
        "RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_BRANCH_ENERGY_INEQUALITY_INSERTION_LEMMA_OK"
    )


if __name__ == "__main__":
    main()

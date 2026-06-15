#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_boundary_term_discharge_in_restricted_energy_inequality_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_TERM_DISCHARGE_IN_RESTRICTED_ENERGY_INEQUALITY"
)
EXPECTED_SOLVES = (
    "RESTRICTED_CONTINUATION_BOUNDARY_TERM_DISCHARGE_IN_RESTRICTED_ENERGY_INEQUALITY"
)
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_BRANCH_ENERGY_INEQUALITY_INSERTION_LEMMA"
)
EXPECTED_STATUS = "DISCHARGE_SURFACE_ONLY_BOUNDARY_TERM_DISCHARGE_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_RESTRICTED_ENERGY_INEQUALITY_CLOSURE_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    discharge = data["discharge_statement"]
    assert discharge["name"] == (
        "restricted_continuation_boundary_term_discharge_in_restricted_energy_inequality"
    )
    assert discharge["selected_branch"] == "boundary_sign"

    required = discharge["required_inputs"]
    assert "restricted_energy_identity_after_integration_by_parts" in required
    assert "boundary_sign_branch_energy_inequality_insertion" in required
    assert "signed_flux_nonpositive_or_absorbable_payload" in required
    assert (
        "restricted_boundary_orientation_compatible_with_flux_sign_convention"
        in required
    )
    assert "boundary_flux_pairing_well_defined_on_restricted_boundary" in required

    modes = discharge["discharge_modes"]
    assert len(modes) == 2
    mode_names = {mode["mode"] for mode in modes}
    assert mode_names == {"dropped", "absorbed"}

    dropped = next(mode for mode in modes if mode["mode"] == "dropped")
    absorbed = next(mode for mode in modes if mode["mode"] == "absorbed")

    assert dropped["discharge_rule"] == (
        "delete_the_nonpositive_boundary_term_from_the_upper_bound"
    )
    assert absorbed["discharge_rule"] == (
        "absorb_the_boundary_term_into_declared_controlled_energy_terms"
    )

    intended = discharge["intended_conclusion"]
    assert (
        "the_boundary_flux_term_is_discharged_in_the_restricted_energy_inequality"
        in intended
    )
    assert "no_uncontrolled_boundary_flux_contribution_remains" in intended
    assert (
        "the_restricted_energy_inequality_may_next_be_closed_by_assembling_remaining_interior_and_control_terms"
        in intended
    )

    negative = data["claim"]["negative"]
    assert (
        "Does not prove the restricted energy identity after integration by parts."
        in negative
    )
    assert "Does not prove the boundary discharge rule." in negative
    assert "Does not close the restricted energy inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print(
        "RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_TERM_DISCHARGE_IN_RESTRICTED_ENERGY_INEQUALITY_OK"
    )


if __name__ == "__main__":
    main()

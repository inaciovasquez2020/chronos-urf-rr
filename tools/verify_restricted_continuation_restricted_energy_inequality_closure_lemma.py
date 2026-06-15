#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_restricted_energy_inequality_closure_lemma_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_RESTRICTED_ENERGY_INEQUALITY_CLOSURE_LEMMA"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_RESTRICTED_ENERGY_INEQUALITY_CLOSURE_LEMMA"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_BOUNDARY_TERM_DISCHARGE_IN_RESTRICTED_ENERGY_INEQUALITY"
)
EXPECTED_STATUS = "LEMMA_SURFACE_ONLY_RESTRICTED_ENERGY_INEQUALITY_CLOSURE_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_ENERGY_TO_NORM_CONTROL_TRANSFER_LEMMA"


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
    assert lemma["name"] == "restricted_continuation_restricted_energy_inequality_closure"

    required = lemma["required_inputs"]
    assert "restricted_energy_identity_after_integration_by_parts" in required
    assert "boundary_term_discharge_in_restricted_energy_inequality" in required
    assert "interior_error_terms_are_declared_controlled" in required
    assert "coercive_energy_terms_are_declared_positive_or_absorbable" in required
    assert "restricted_continuation_energy_functional_is_well_defined" in required

    closure_steps = lemma["closure_steps"]
    assert len(closure_steps) == 4
    step_names = {step["step"] for step in closure_steps}
    assert step_names == {
        "boundary_discharge",
        "interior_term_collection",
        "coercive_term_alignment",
        "closed_inequality_form",
    }

    intended = lemma["intended_conclusion"]
    assert (
        "the_restricted_energy_inequality_is_closed_at_the_formal_target_level"
        in intended
    )
    assert "all_boundary_terms_are_classified_as_discharged" in intended
    assert (
        "all_interior_error_terms_are_classified_as_controlled_or_absorbable"
        in intended
    )
    assert (
        "energy_to_norm_control_transfer_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert (
        "Does not prove the restricted energy identity after integration by parts."
        in negative
    )
    assert "Does not prove boundary-term discharge." in negative
    assert "Does not prove interior error control." in negative
    assert "Does not prove coercivity or absorption." in negative
    assert "Does not prove the energy-to-norm transfer." in negative
    assert "Does not close the restricted continuation norm-control theorem." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_RESTRICTED_ENERGY_INEQUALITY_CLOSURE_LEMMA_OK")


if __name__ == "__main__":
    main()

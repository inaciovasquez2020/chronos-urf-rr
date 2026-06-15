#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_energy_to_norm_control_transfer_lemma_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_ENERGY_TO_NORM_CONTROL_TRANSFER_LEMMA"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_ENERGY_TO_NORM_CONTROL_TRANSFER_LEMMA"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_RESTRICTED_ENERGY_INEQUALITY_CLOSURE_LEMMA"
)
EXPECTED_STATUS = "LEMMA_SURFACE_ONLY_ENERGY_TO_NORM_CONTROL_TRANSFER_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_NORM_CONTROL_CLOSURE_ASSEMBLY_LEMMA"


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
    assert lemma["name"] == "restricted_continuation_energy_to_norm_control_transfer"

    required = lemma["required_inputs"]
    assert "restricted_energy_inequality_is_closed" in required
    assert "restricted_continuation_energy_functional_is_well_defined" in required
    assert "energy_functional_controls_declared_norm" in required
    assert "coercive_energy_terms_are_positive_or_absorbable" in required
    assert "all_boundary_terms_are_discharged" in required
    assert "all_interior_error_terms_are_controlled_or_absorbable" in required

    transfer_steps = lemma["transfer_steps"]
    assert len(transfer_steps) == 4
    step_names = {step["step"] for step in transfer_steps}
    assert step_names == {
        "energy_control_extraction",
        "coercive_norm_comparison",
        "controlled_term_absorption",
        "norm_control_form",
    }

    intended = lemma["intended_conclusion"]
    assert (
        "the_closed_restricted_energy_inequality_transfers_to_declared_norm_control"
        in intended
    )
    assert (
        "the_norm_control_estimate_has_no_unclassified_boundary_flux_term"
        in intended
    )
    assert (
        "the_norm_control_estimate_has_no_unclassified_interior_error_term"
        in intended
    )
    assert (
        "restricted_continuation_norm_control_closure_assembly_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove the closed restricted energy inequality." in negative
    assert "Does not prove the energy functional controls the declared norm." in negative
    assert "Does not prove coercive norm comparison." in negative
    assert "Does not prove controlled-term absorption." in negative
    assert (
        "Does not prove the restricted continuation norm-control theorem."
        in negative
    )
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_ENERGY_TO_NORM_CONTROL_TRANSFER_LEMMA_OK")


if __name__ == "__main__":
    main()

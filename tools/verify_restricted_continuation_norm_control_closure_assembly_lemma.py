#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_norm_control_closure_assembly_lemma_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_CLOSURE_ASSEMBLY_LEMMA"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_NORM_CONTROL_CLOSURE_ASSEMBLY_LEMMA"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_ENERGY_TO_NORM_CONTROL_TRANSFER_LEMMA"
)
EXPECTED_STATUS = "LEMMA_SURFACE_ONLY_NORM_CONTROL_CLOSURE_ASSEMBLY_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM_CLOSURE_PAYLOAD"


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
    assert lemma["name"] == "restricted_continuation_norm_control_closure_assembly"

    required = lemma["required_inputs"]
    assert (
        "closed_restricted_energy_inequality_transfers_to_declared_norm_control"
        in required
    )
    assert (
        "norm_control_estimate_has_no_unclassified_boundary_flux_term"
        in required
    )
    assert (
        "norm_control_estimate_has_no_unclassified_interior_error_term"
        in required
    )
    assert "restricted_continuation_energy_functional_is_well_defined" in required
    assert "declared_norm_control_quantity_is_well_defined" in required

    assembly_steps = lemma["assembly_steps"]
    assert len(assembly_steps) == 4
    step_names = {step["step"] for step in assembly_steps}
    assert step_names == {
        "import_energy_to_norm_transfer",
        "boundary_cleanliness_check",
        "interior_cleanliness_check",
        "closure_statement_packaging",
    }

    intended = lemma["intended_conclusion"]
    assert (
        "the_restricted_continuation_norm_control_closure_statement_is_assembled_at_the_formal_target_level"
        in intended
    )
    assert (
        "the_assembled_norm_control_statement_has_no_unclassified_boundary_flux_term"
        in intended
    )
    assert (
        "the_assembled_norm_control_statement_has_no_unclassified_interior_error_term"
        in intended
    )
    assert (
        "restricted_continuation_norm_control_theorem_closure_payload_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove the energy-to-norm transfer lemma." in negative
    assert "Does not prove boundary cleanliness." in negative
    assert "Does not prove interior error cleanliness." in negative
    assert "Does not prove the assembled norm-control theorem." in negative
    assert (
        "Does not close the restricted continuation norm-control theorem."
        in negative
    )
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_CLOSURE_ASSEMBLY_LEMMA_OK")


if __name__ == "__main__":
    main()

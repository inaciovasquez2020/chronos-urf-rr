#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_norm_control_theorem_closure_payload_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM_CLOSURE_PAYLOAD"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM_CLOSURE_PAYLOAD"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_CLOSURE_ASSEMBLY_LEMMA"
)
EXPECTED_STATUS = "PAYLOAD_SURFACE_ONLY_NORM_CONTROL_THEOREM_CLOSURE_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_RR_ROUTE_CLOSURE_GATE"


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
    assert payload["name"] == "restricted_continuation_norm_control_theorem_closure_payload"

    required = payload["required_inputs"]
    assert (
        "restricted_continuation_norm_control_closure_statement_is_assembled"
        in required
    )
    assert (
        "assembled_norm_control_statement_has_no_unclassified_boundary_flux_term"
        in required
    )
    assert (
        "assembled_norm_control_statement_has_no_unclassified_interior_error_term"
        in required
    )
    assert "declared_norm_control_quantity_is_well_defined" in required
    assert "restricted_continuation_energy_functional_is_well_defined" in required

    components = payload["closure_payload_components"]
    assert len(components) == 4
    component_names = {component["component"] for component in components}
    assert component_names == {
        "assembled_norm_control_estimate",
        "boundary_cleanliness_certificate",
        "interior_cleanliness_certificate",
        "theorem_payload_packaging",
    }

    intended = payload["intended_conclusion"]
    assert (
        "the_restricted_continuation_norm_control_theorem_payload_is_declared"
        in intended
    )
    assert "the_payload_has_no_unclassified_boundary_flux_term" in intended
    assert "the_payload_has_no_unclassified_interior_error_term" in intended
    assert (
        "rr_restricted_continuation_route_closure_gate_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove the assembled norm-control theorem." in negative
    assert "Does not prove boundary cleanliness." in negative
    assert "Does not prove interior error cleanliness." in negative
    assert "Does not prove the full restricted continuation theorem." in negative
    assert "Does not close the RR restricted-continuation route." in negative
    assert "Does not close the full RR theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM_CLOSURE_PAYLOAD_OK")


if __name__ == "__main__":
    main()

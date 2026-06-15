#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_selected_trace_flux_witness_branch_2026_06_15.json"
)

EXPECTED_ID = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_SELECTED_TRACE_FLUX_WITNESS_BRANCH"
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_SELECTED_TRACE_FLUX_WITNESS_BRANCH"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_TRACE_INEQUALITY_OR_BOUNDARY_SIGN_WITNESS"
)
EXPECTED_STATUS = "SELECTED_BRANCH_SURFACE_ONLY_BOUNDARY_SIGN_PAYLOAD_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_BOUNDARY_SIGN_CONDITION_PAYLOAD"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    selected = data["selected_branch"]
    assert selected["branch"] == "boundary_sign"
    assert "declared_boundary_sign_condition" in selected["required_payload"]
    assert "restricted_boundary_orientation_compatibility" in selected["required_payload"]
    assert "signed_flux_nonpositive_or_absorbable_payload" in selected["required_payload"]
    assert (
        "boundary_flux_term_does_not_create_uncontrolled_positive_energy"
        in selected["intended_conclusion"]
    )

    unselected = data["unselected_branch"]
    assert unselected["branch"] == "trace_inequality"
    assert unselected["status"] == "not_selected_for_this_route"
    assert "finite_trace_constant" in unselected["not_used_payload"]

    negative = data["claim"]["negative"]
    assert "Does not prove the boundary sign condition." in negative
    assert "Does not prove orientation compatibility." in negative
    assert "Does not prove signed flux is nonpositive or absorbable." in negative
    assert "Does not prove a quantitative trace inequality." in negative
    assert "Does not close the restricted energy inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_SELECTED_TRACE_FLUX_WITNESS_BRANCH_OK")


if __name__ == "__main__":
    main()

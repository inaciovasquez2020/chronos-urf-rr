#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_trace_inequality_or_boundary_sign_witness_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_TRACE_INEQUALITY_OR_BOUNDARY_SIGN_WITNESS"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_TRACE_INEQUALITY_OR_BOUNDARY_SIGN_WITNESS"
EXPECTED_PREDECESSOR = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_TRACE_FLUX_CONTROL_LEMMA"
EXPECTED_STATUS = "WITNESS_SURFACE_ONLY_TRACE_INEQUALITY_OR_BOUNDARY_SIGN_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_SELECTED_TRACE_FLUX_WITNESS_BRANCH"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    statement = data["witness_statement"]
    assert statement["name"] == "restricted_continuation_trace_inequality_or_boundary_sign_witness"

    branches = statement["admissible_branches"]
    assert len(branches) == 2
    branch_names = {branch["branch"] for branch in branches}
    assert branch_names == {"trace_inequality", "boundary_sign"}

    trace_branch = next(branch for branch in branches if branch["branch"] == "trace_inequality")
    sign_branch = next(branch for branch in branches if branch["branch"] == "boundary_sign")

    assert "finite_trace_constant" in trace_branch["required_payload"]
    assert "boundary_flux_abs_bound_by_trace_norm" in trace_branch["required_payload"]
    assert trace_branch["conclusion"] == "boundary_flux_term_is_quantitatively_controlled"

    assert "declared_sign_condition" in sign_branch["required_payload"]
    assert "signed_flux_is_nonpositive_or_absorbable" in sign_branch["required_payload"]
    assert sign_branch["conclusion"] == (
        "boundary_flux_term_does_not_create_uncontrolled_positive_energy"
    )

    common = statement["common_conclusion"]
    assert "one_admissible_trace_flux_witness_branch_is_declared" in common
    assert "the_restricted_energy_inequality_has_no_uncontrolled_boundary_flux_term" in common

    negative = data["claim"]["negative"]
    assert "Does not select a concrete branch." in negative
    assert "Does not prove a quantitative trace inequality." in negative
    assert "Does not prove a finite trace constant." in negative
    assert "Does not prove a boundary sign condition." in negative
    assert "Does not close the restricted energy inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_TRACE_INEQUALITY_OR_BOUNDARY_SIGN_WITNESS_OK")


if __name__ == "__main__":
    main()

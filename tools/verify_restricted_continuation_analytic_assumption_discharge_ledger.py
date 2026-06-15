#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_analytic_assumption_discharge_ledger_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_ANALYTIC_ASSUMPTION_DISCHARGE_LEDGER"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_ANALYTIC_ASSUMPTION_DISCHARGE_LEDGER"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_FORMAL_RR_THEOREM_PROOF_TARGET"
)
EXPECTED_STATUS = "LEDGER_SURFACE_ONLY_ANALYTIC_ASSUMPTIONS_NOT_DISCHARGED"
EXPECTED_NEXT = (
    "RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_DISCHARGE_TARGET"
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

    ledger = data["ledger_statement"]
    assert ledger["name"] == "restricted_continuation_analytic_assumption_discharge_ledger"

    groups = ledger["required_assumption_groups"]
    assert len(groups) == 5
    group_names = {group["group"] for group in groups}
    assert group_names == {
        "regularity_and_differentiation",
        "trace_and_boundary_flux",
        "boundary_sign_and_orientation",
        "energy_inequality_closure",
        "energy_to_norm_transfer",
    }

    for group in groups:
        assert group["discharge_status"] == "declared_not_discharged"
        assert len(group["assumptions"]) >= 3

    regularity = next(
        group for group in groups if group["group"] == "regularity_and_differentiation"
    )
    assert "solution_has_time_regular_energy" in regularity["assumptions"]
    assert (
        "energy_density_is_differentiable_along_restricted_continuation"
        in regularity["assumptions"]
    )

    trace = next(group for group in groups if group["group"] == "trace_and_boundary_flux")
    assert "boundary_trace_exists_on_restricted_continuation_domain" in trace["assumptions"]
    assert "boundary_flux_pairing_well_defined_on_restricted_boundary" in trace["assumptions"]

    checks = ledger["ledger_checks"]
    assert len(checks) == 4
    check_names = {check["check"] for check in checks}
    assert check_names == {
        "all_route_assumption_groups_named",
        "each_group_has_discharge_status",
        "undischarged_status_preserved",
        "next_discharge_target_selected",
    }

    intended = ledger["intended_conclusion"]
    assert "the_analytic_assumption_discharge_ledger_is_declared" in intended
    assert "all_major_undischarged_analytic_assumption_groups_are_visible" in intended
    assert (
        "no_analytic_assumption_is_marked_as_discharged_without_proof"
        in intended
    )
    assert (
        "regularity_and_differentiation_discharge_target_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not discharge any analytic assumption." in negative
    assert "Does not prove regularity or differentiation." in negative
    assert "Does not prove trace existence or boundary flux pairing." in negative
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not close the full RR theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_ANALYTIC_ASSUMPTION_DISCHARGE_LEDGER_OK")


if __name__ == "__main__":
    main()

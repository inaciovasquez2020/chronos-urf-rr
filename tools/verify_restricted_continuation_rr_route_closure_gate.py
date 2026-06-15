#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_rr_route_closure_gate_2026_06_15.json"
)

EXPECTED_ID = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_RR_ROUTE_CLOSURE_GATE"
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_RR_ROUTE_CLOSURE_GATE"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM_CLOSURE_PAYLOAD"
)
EXPECTED_STATUS = "GATE_SURFACE_ONLY_RR_ROUTE_CLOSURE_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_FORMAL_RR_THEOREM_PROOF"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    gate = data["gate_statement"]
    assert gate["name"] == "restricted_continuation_rr_route_closure_gate"

    required = gate["required_inputs"]
    assert "restricted_continuation_norm_control_theorem_payload_is_declared" in required
    assert "payload_has_no_unclassified_boundary_flux_term" in required
    assert "payload_has_no_unclassified_interior_error_term" in required
    assert "restricted_continuation_route_chain_has_verified_artifact_successors" in required
    assert "full_rr_closure_boundary_remains_declared" in required

    checks = gate["gate_checks"]
    assert len(checks) == 4
    check_names = {check["check"] for check in checks}
    assert check_names == {
        "route_chain_assembled",
        "boundary_flux_classified",
        "energy_to_norm_path_classified",
        "full_rr_boundary_preserved",
    }

    intended = gate["intended_conclusion"]
    assert (
        "the_runall_rr_restricted_continuation_route_closure_gate_is_declared"
        in intended
    )
    assert (
        "the_route_has_a_verified_documented_successor_chain_to_norm_control_payload"
        in intended
    )
    assert "the_gate_preserves_the_not_full_rr_closure_boundary" in intended
    assert (
        "formal_restricted_continuation_rr_theorem_proof_is_now_the_next_required_check"
        in intended
    )

    negative = data["claim"]["negative"]
    assert "Does not prove the norm-control theorem." in negative
    assert "Does not prove the formal restricted-continuation theorem." in negative
    assert "Does not prove the full RR theorem." in negative
    assert "Does not discharge all analytic assumptions in Lean." in negative
    assert "Does not claim full RR closure." in negative
    assert "Does not claim final scientific closure." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_RR_ROUTE_CLOSURE_GATE_OK")


if __name__ == "__main__":
    main()

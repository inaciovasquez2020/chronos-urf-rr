#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_regularity_trace_and_boundary_flux_assumptions_2026_06_15.json"
)

EXPECTED_ID = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_REGULARITY_TRACE_AND_BOUNDARY_FLUX_ASSUMPTIONS"
)
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_REGULARITY_TRACE_AND_BOUNDARY_FLUX_ASSUMPTIONS"
EXPECTED_STATUS = "ASSUMPTION_SURFACE_ONLY_TRACE_AND_BOUNDARY_FLUX_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_TRACE_FLUX_CONTROL_LEMMA"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    assumptions = data["required_assumptions"]
    assert set(assumptions) == {"regularity", "trace", "boundary_flux"}
    assert len(assumptions["regularity"]) >= 3
    assert len(assumptions["trace"]) >= 3
    assert len(assumptions["boundary_flux"]) >= 3

    negative = data["claim"]["negative"]
    assert any("Does not prove the regularity theorem." == item for item in negative)
    assert any("Does not prove trace existence." == item for item in negative)
    assert any("Does not close the full RR restricted-continuation theorem." == item for item in negative)

    print("RUNALL_RESTRICTED_CONTINUATION_REGULARITY_TRACE_AND_BOUNDARY_FLUX_ASSUMPTIONS_OK")


if __name__ == "__main__":
    main()

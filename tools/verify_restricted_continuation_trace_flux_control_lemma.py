#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "restricted_continuation_trace_flux_control_lemma_2026_06_15.json"
)

EXPECTED_ID = "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_TRACE_FLUX_CONTROL_LEMMA"
EXPECTED_SOLVES = "RESTRICTED_CONTINUATION_TRACE_FLUX_CONTROL_LEMMA"
EXPECTED_PREDECESSOR = (
    "RUNALL_VERIFIED_RESTRICTED_CONTINUATION_REGULARITY_TRACE_AND_BOUNDARY_FLUX_ASSUMPTIONS"
)
EXPECTED_STATUS = "LEMMA_TARGET_ONLY_TRACE_FLUX_CONTROL_NOT_PROVED"
EXPECTED_NEXT = "RESTRICTED_CONTINUATION_TRACE_INEQUALITY_OR_BOUNDARY_SIGN_WITNESS"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["id"] == EXPECTED_ID
    assert data["repository"] == "chronos-urf-rr"
    assert data["solves_missing_object"] == EXPECTED_SOLVES
    assert data["predecessor_object"] == EXPECTED_PREDECESSOR
    assert data["status"] == EXPECTED_STATUS
    assert data["current_weakest_missing_object"] == EXPECTED_NEXT
    assert data["boundary"] == "NOT_FULL_RR_CLOSURE"

    statement = data["lemma_statement"]
    assert statement["name"] == "restricted_continuation_trace_flux_control"
    assert "input_assumptions" in statement
    assert "conclusion" in statement
    assert len(statement["input_assumptions"]) >= 6
    assert len(statement["conclusion"]) >= 3

    control_modes = data["control_modes"]
    assert set(control_modes) == {"vanishing", "sign", "trace_norm_bound"}

    negative = data["claim"]["negative"]
    assert "Does not prove boundary trace existence." in negative
    assert "Does not prove a sign condition." in negative
    assert "Does not prove boundary flux vanishing." in negative
    assert "Does not prove a quantitative trace inequality." in negative
    assert "Does not close the full RR restricted-continuation theorem." in negative

    print("RUNALL_RESTRICTED_CONTINUATION_TRACE_FLUX_CONTROL_LEMMA_OK")


if __name__ == "__main__":
    main()

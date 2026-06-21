#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/"
    "classifier_bounded_closure_reference_downstream_adoption_2026_06_21.json"
)

EXPECTED_ID = "classifier_bounded_closure_reference_downstream_adoption"
EXPECTED_STATUS = "DOWNSTREAM_ADOPTION_SURFACE_ONLY"
EXPECTED_SOURCE_PROJECT = "theorem-closure-classifier"
EXPECTED_SURFACE = "BOUNDED_CLOSURE_PROOF_PATTERN_REFERENCE"
EXPECTED_DOWNSTREAM_PROJECT = "chronos-urf-rr"
EXPECTED_FIRST_DOWNSTREAM_PROJECT = "CSLIB-FMT"

REQUIRED_BOUNDARY = {
    "This artifact records a downstream adoption surface only.",
    "It does not assert that the classifier independent-project usefulness criterion is fully satisfied.",
    "It records chronos-urf-rr as one downstream project separate from CSLIB-FMT.",
    "It does not prove external acceptance, theorem completeness, or general mathematical usefulness.",
}

REQUIRED_FLAGS = {
    "names_adopted_classifier_surface",
    "has_downstream_artifact",
    "has_downstream_verifier",
    "has_downstream_regression_test",
    "records_weakest_gap_boundary",
}

FORBIDDEN_STATUS_TERMS = {
    "SATISFIED",
    "COMPLETE",
    "PROVED",
    "CLOSED",
    "EXTERNALLY_ACCEPTED",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(ARTIFACT.exists(), f"MISSING_OBJECT := {ARTIFACT}")
    data = json.loads(ARTIFACT.read_text())

    require(data.get("id") == EXPECTED_ID, "INVALID_ID")
    require(data.get("status") == EXPECTED_STATUS, "INVALID_STATUS")

    status = str(data.get("status", ""))
    require(not any(term in status for term in FORBIDDEN_STATUS_TERMS), "OVERCLAIMED_STATUS")

    source_project = data.get("source_project")
    require(isinstance(source_project, dict), "MISSING_SOURCE_PROJECT")
    require(source_project.get("name") == EXPECTED_SOURCE_PROJECT, "INVALID_SOURCE_PROJECT")
    require(source_project.get("surface") == EXPECTED_SURFACE, "INVALID_CLASSIFIER_SURFACE")

    downstream_project = data.get("downstream_project")
    require(isinstance(downstream_project, dict), "MISSING_DOWNSTREAM_PROJECT")
    require(
        downstream_project.get("name") == EXPECTED_DOWNSTREAM_PROJECT,
        "INVALID_DOWNSTREAM_PROJECT",
    )
    require(
        downstream_project.get("repository_role") == "separate formalization target",
        "INVALID_DOWNSTREAM_REPOSITORY_ROLE",
    )

    relation = data.get("relation_to_existing_downstream_evidence")
    require(isinstance(relation, dict), "MISSING_RELATION_TO_EXISTING_DOWNSTREAM_EVIDENCE")
    require(
        relation.get("first_downstream_project") == EXPECTED_FIRST_DOWNSTREAM_PROJECT,
        "INVALID_FIRST_DOWNSTREAM_PROJECT",
    )
    require(
        relation.get("separate_from_first_downstream_project") is True,
        "MISSING_SEPARATION_FLAG",
    )
    require(relation.get("minimum_project_count_target") == 2, "INVALID_PROJECT_COUNT_TARGET")

    evidence_shape = data.get("evidence_shape")
    require(isinstance(evidence_shape, dict), "MISSING_EVIDENCE_SHAPE")
    for flag in REQUIRED_FLAGS:
        require(evidence_shape.get(flag) is True, f"MISSING_EVIDENCE_FLAG := {flag}")

    boundary = set(data.get("boundary", []))
    require(REQUIRED_BOUNDARY.issubset(boundary), "MISSING_BOUNDARY")

    weakest_gap = data.get("weakest_gap")
    require(isinstance(weakest_gap, str) and weakest_gap, "MISSING_WEAKEST_GAP")
    require("theorem-closure-classifier must aggregate" in weakest_gap, "INVALID_WEAKEST_GAP")

    print("CLASSIFIER_BOUNDED_CLOSURE_REFERENCE_DOWNSTREAM_ADOPTION_OK")


if __name__ == "__main__":
    main()

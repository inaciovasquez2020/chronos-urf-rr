#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/restricted_non_symmetric_collapse_closure_refinement_2026_05_21.json"
DOC = ROOT / "docs/status/RESTRICTED_NON_SYMMETRIC_COLLAPSE_CLOSURE_REFINEMENT_2026_05_21.md"

REQUIRED_ARTIFACT = {
    "status": "STRICT_REFINEMENT_TARGET_OPEN",
    "classification": "RESTRICTED_REFINEMENT_TARGET_ONLY",
    "parent_macro_axiom": "NonSymmetricEinsteinMatterCollapseClosure",
    "restricted_refinement_target": "RestrictedNonSymmetricCollapseClosure",
}

REQUIRED_RESTRICTED_COMPONENTS = {
    "RestrictedUniversalBoundaryCompactness(D)",
    "RestrictedQLCollapseGate(D,S)",
    "RestrictedHoopFromQLGate(S)",
}

REQUIRED_OBJECTS = {
    "RestrictedCollapseDomain",
    "RestrictedCollapseSurface",
    "RestrictedNonSymmetricCollapseClosure",
}

REQUIRED_BOUNDARY_TOKENS = [
    "Does not prove NonSymmetricEinsteinMatterCollapseClosure.",
    "Does not prove unrestricted non-symmetric Einstein-matter collapse closure.",
    "Does not prove unrestricted universal boundary compactness.",
    "Does not prove unrestricted QL-collapse gating.",
    "Does not prove unrestricted weak cosmic censorship.",
    "Does not prove unrestricted hoop theorem.",
    "Does not prove unrestricted PDE bootstrap closure.",
    "Does not prove operator-algebraic nuclearity-to-bulk-collapse closure.",
    "Does not prove P vs NP.",
    "Does not prove any Clay problem.",
]

REQUIRED_DOC_TOKENS = [
    "Status: STRICT_REFINEMENT_TARGET_OPEN",
    "Classification: RESTRICTED_REFINEMENT_TARGET_ONLY",
    "Parent macro-axiom: `NonSymmetricEinsteinMatterCollapseClosure`",
    "Restricted refinement target: `RestrictedNonSymmetricCollapseClosure`",
    "The parent macro-axiom is not logically contradictory",
    "scope mismatch",
    "`RestrictedCollapseDomain`",
    "`RestrictedCollapseSurface`",
    "`RestrictedNonSymmetricCollapseClosure`",
    "Does not prove:",
    "unrestricted universal boundary compactness",
    "unrestricted QL-collapse gating",
    "unrestricted weak cosmic censorship",
    "unrestricted hoop theorem",
    "P vs NP",
    "any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    for key, expected in REQUIRED_ARTIFACT.items():
        assert data[key] == expected, (key, data.get(key), expected)

    assert set(data["restricted_components"]) == REQUIRED_RESTRICTED_COMPONENTS
    assert set(data["minimal_new_objects"]) == REQUIRED_OBJECTS

    corrected = data["corrected_obstruction"]
    assert "not logically contradictory" in corrected
    assert "scope mismatch" in corrected

    boundary = "\n".join(data["boundary"])
    for token in REQUIRED_BOUNDARY_TOKENS:
        assert token in boundary, token

    for token in REQUIRED_DOC_TOKENS:
        assert token in doc, token

    print("Restricted non-symmetric collapse closure refinement verified.")

if __name__ == "__main__":
    main()

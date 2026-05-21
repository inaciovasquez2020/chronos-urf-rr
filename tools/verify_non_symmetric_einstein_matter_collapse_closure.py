#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/non_symmetric_einstein_matter_collapse_closure_2026_05_20.json"
DOC = ROOT / "docs/status/NON_SYMMETRIC_EINSTEIN_MATTER_COLLAPSE_CLOSURE_2026_05_20.md"

REQUIRED_COMPONENTS = {
    "NonSymmetricTrappedSurfaceCriterion",
    "CollapseToCensorshipBridge",
    "HoopFromQLGate",
    "UnrestrictedUniversalBoundaryCompactness",
    "UnrestrictedQLCollapseGate",
}

REQUIRED_DOC_TOKENS = [
    "Status: OPEN_PROBLEM_REQUIRED",
    "Classification: MACRO_AXIOM_BOUNDARY_ONLY",
    "Minimal missing lemma: `NonSymmetricEinsteinMatterCollapseClosure`",
    "Does not prove:",
    "unrestricted non-symmetric Einstein-matter collapse closure",
    "unrestricted weak cosmic censorship",
    "unrestricted hoop theorem",
    "operator-algebraic nuclearity-to-bulk-collapse closure",
    "P vs NP",
    "any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["status"] == "OPEN_PROBLEM_REQUIRED"
    assert data["classification"] == "MACRO_AXIOM_BOUNDARY_ONLY"
    assert data["macro_axiom"] == "NonSymmetricEinsteinMatterCollapseClosure"
    assert data["minimal_missing_lemma"] == "NonSymmetricEinsteinMatterCollapseClosure"
    assert set(data["components"]) == REQUIRED_COMPONENTS

    boundary = "\n".join(data["boundary"])
    for token in [
        "No unrestricted non-symmetric Einstein-matter collapse theorem is proved.",
        "No unrestricted weak cosmic censorship theorem is proved.",
        "No unrestricted hoop theorem is proved.",
        "No PDE bootstrap closure is proved.",
        "No operator-algebraic nuclearity-to-bulk-collapse theorem is proved.",
        "No P vs NP claim.",
        "No Clay-problem closure.",
    ]:
        assert token in boundary

    for token in REQUIRED_DOC_TOKENS:
        assert token in doc

    print("Non-symmetric Einstein-matter collapse closure boundary verified.")

if __name__ == "__main__":
    main()

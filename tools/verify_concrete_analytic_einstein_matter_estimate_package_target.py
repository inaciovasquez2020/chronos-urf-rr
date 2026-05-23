#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT = ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_target_2026_05_23.json"
STATUS = ROOT / "docs/status/CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_TARGET_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteAnalyticEinsteinMatterEstimatePackageTarget.lean"

EXPECTED = "TARGET_FORMALIZED_ANALYTIC_PACKAGE_NOT_PROVED"

LEAN_TOKENS = [
    "structure ConcreteAnalyticEinsteinMatterEstimateDatum",
    "continuationNormN",
    "bootstrapInequalitiesB",
    "concentrationFunctionalQ",
    "thresholdQ",
    "def RESTRICTED_CONCENTRATION_MONOTONICITY",
    "def RESTRICTED_CONTINUATION_NORM_CONTROL",
    "def ConcreteAnalyticEinsteinMatterEstimatePackage",
    "structure ConcreteAnalyticEinsteinMatterEstimatePackageTarget",
    "theorem concrete_analytic_einstein_matter_estimate_package_of_target",
    "theorem finite_continuation_norm_of_target",
    "theorem concentration_monotone_of_target"
]

BOUNDARIES = [
    "analytic Einstein-matter bootstrap package",
    "concrete analytic Einstein-matter estimate package",
    "finite continuation norm",
    "bootstrap bounds",
    "concentration monotonicity",
    "threshold crossing",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem"
]

def main() -> None:
    assert ARTIFACT.exists(), ARTIFACT
    assert STATUS.exists(), STATUS
    assert LEAN.exists(), LEAN

    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_TARGET"
    assert data["status"] == EXPECTED
    assert data["lean_module"] == "Chronos.Frontier.ConcreteAnalyticEinsteinMatterEstimatePackageTarget"

    for token in LEAN_TOKENS:
        assert token in lean, token

    for object_name in ["continuationNormN", "bootstrapInequalitiesB", "concentrationFunctionalQ", "thresholdQ"]:
        assert object_name in data["formalized_objects"], object_name
        assert object_name in lean, object_name

    for lemma in ["RESTRICTED_CONCENTRATION_MONOTONICITY", "RESTRICTED_CONTINUATION_NORM_CONTROL"]:
        assert lemma in data["formalized_missing_lemmas"], lemma
        assert lemma in status, lemma
        assert lemma in lean, lemma

    for boundary in BOUNDARIES:
        assert boundary in data["does_not_prove"], boundary
        assert boundary in status, boundary
        assert boundary in lean, boundary

    blob = (status + "\n" + lean).lower()
    assert "gravity solved" not in blob
    assert "clay solved" not in blob
    assert "p vs np solved" not in blob

    print("Concrete analytic Einstein-matter estimate package target verification OK.")
    print("Status:", data["status"])

if __name__ == "__main__":
    main()

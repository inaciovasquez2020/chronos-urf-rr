#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ARTIFACT = Path("artifacts/chronos/mathematical_physics_gap_audit_2026_06_10.json")
EXPECTED_ID = "MATHEMATICAL_PHYSICS_GAP_AUDIT_2026_06_10"

REQUIRED_TARGETS = {
    "ExternalPhysicsNotationSemanticDriftAudit",
    "ConstructiveQFTExternalCertificateIntake",
    "YangMillsMassGapBoundaryClassification",
    "SpectralGapDecidabilityBoundaryAudit",
    "GRRegularityClassBoundarySchema",
    "QuantumInfoFormalProofGapIntake",
    "ProbabilisticQFTExternalSourceMap",
}

REQUIRED_EXCLUSIONS = {
    "new physics theorem proof",
    "QFT phenomenology expansion",
    "Yang-Mills mass-gap proof",
    "cosmic-censorship proof",
    "scattering-amplitude theorem",
}


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    assert data["id"] == EXPECTED_ID
    assert data["status"] == "frontier_gap_audit_only"
    assert data["scope"] == "mathematical physics"
    assert data["best_next_object"] == EXPECTED_ID

    included = set(data["toolkit_fit"]["included"])
    assert "external notation and semantic-drift audit" in included
    assert "external theorem certificate intake" in included
    assert "frontier boundary classification" in included
    assert "proof-gap intake schema" in included
    assert "assumption inventory" in included

    excluded = set(data["toolkit_fit"]["excluded"])
    assert REQUIRED_EXCLUSIONS <= excluded

    gaps = data["gaps"]
    assert len(gaps) == 7

    targets = {gap["admissible_target"] for gap in gaps}
    assert REQUIRED_TARGETS == targets

    for gap in gaps:
        assert gap["fit"].endswith("-fit")
        assert gap["basis"]
        assert gap["source"].startswith("https://")

    boundary = data["boundary"]
    assert "no new physics theorem" in boundary
    assert "no scientific payload" in boundary
    assert "no theorem promotion" in boundary

    print("MATHEMATICAL_PHYSICS_GAP_AUDIT_OK")


if __name__ == "__main__":
    main()

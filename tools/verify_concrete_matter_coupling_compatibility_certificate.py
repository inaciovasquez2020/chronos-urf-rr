#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/concrete_matter_coupling_compatibility_certificate_2026_05_23.json"
STATUS = ROOT / "docs/status/CONCRETE_MATTER_COUPLING_COMPATIBILITY_CERTIFICATE_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteMatterCouplingCompatibilityCertificate.lean"

EXPECTED = "CONCRETE_MATTER_COUPLING_COMPATIBILITY_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE"

BOUNDARIES = [
    "analytic Einstein-matter bootstrap package",
    "constraint propagation",
    "energy-condition preservation",
    "continuation until collapse threshold",
    "restricted collapse-gate trigger",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

LEAN_TOKENS = [
    "structure ConcreteMatterCouplingDatum",
    "def SelectedStressPreserved",
    "structure ConcreteMatterCouplingCompatibilityCertificate",
    "theorem concrete_matter_coupling_compatibility_certificate",
    "theorem selected_stress_eq_canonical_of_certificate",
]

def main() -> None:
    assert ARTIFACT.exists(), ARTIFACT
    assert STATUS.exists(), STATUS
    assert LEAN.exists(), LEAN

    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "CONCRETE_MATTER_COUPLING_COMPATIBILITY_CERTIFICATE"
    assert data["status"] == EXPECTED
    assert data["lean_module"] == "Chronos.Frontier.ConcreteMatterCouplingCompatibilityCertificate"

    for token in LEAN_TOKENS:
        assert token in lean, token

    for boundary in BOUNDARIES:
        assert boundary in data["does_not_prove"], boundary
        assert boundary in status, boundary
        assert boundary in lean, boundary

    blob = (status + "\n" + lean).lower()
    assert "gravity solved" not in blob
    assert "clay solved" not in blob
    assert "p vs np solved" not in blob

    print("Concrete matter-coupling compatibility certificate verification OK.")
    print("Status:", data["status"])

if __name__ == "__main__":
    main()

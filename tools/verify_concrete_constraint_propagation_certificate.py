#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/concrete_constraint_propagation_certificate_2026_05_23.json"
STATUS = ROOT / "docs/status/CONCRETE_CONSTRAINT_PROPAGATION_CERTIFICATE_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/ConcreteConstraintPropagationCertificate.lean"

EXPECTED = "CONCRETE_CONSTRAINT_PROPAGATION_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE"

BOUNDARIES = [
    "analytic Einstein-matter bootstrap package",
    "matter-coupling compatibility",
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
    "structure ConcreteConstraintPropagationDatum",
    "def ConstraintsPropagate",
    "structure HomogeneousConstraintPropagationCertificate",
    "theorem concrete_constraint_propagation_certificate",
    "theorem constraint_zero_at_time_of_certificate",
]

def main() -> None:
    assert ARTIFACT.exists(), ARTIFACT
    assert STATUS.exists(), STATUS
    assert LEAN.exists(), LEAN

    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "CONCRETE_CONSTRAINT_PROPAGATION_CERTIFICATE"
    assert data["status"] == EXPECTED
    assert data["lean_module"] == "Chronos.Frontier.ConcreteConstraintPropagationCertificate"
    assert data["next_admissible_object"] == "ConcreteEnergyConditionPreservationCertificate"

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

    print("Concrete constraint-propagation certificate verification OK.")
    print("Status:", data["status"])

if __name__ == "__main__":
    main()

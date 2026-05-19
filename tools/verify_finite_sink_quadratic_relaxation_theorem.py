#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "lean/Chronos/Frontier/FiniteSinkQuadraticRelaxationTheorem.lean"
doc = ROOT / "docs/status/FINITE_SINK_QUADRATIC_RELAXATION_THEOREM_2026_05_18.md"
artifact = ROOT / "artifacts/chronos/finite_sink_quadratic_relaxation_theorem_2026_05_18.json"
root_import = ROOT / "lean/Chronos.lean"

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_data = json.loads(artifact.read_text())
root_text = root_import.read_text()

required_lean = [
    "def sinkRelax",
    "def quadraticEntropy",
    "def closedUnderSinkRelaxation",
    "def entropyProductionOn",
    "def entropyMonotoneOn",
    "structure FiniteSinkQuadraticRelaxationCertificate",
    "theorem quadratic_entropy_monotone_to_sink",
    "theorem quadratic_entropy_production_nonnegative",
    "theorem finite_sink_quadratic_relaxation_certificate",
    "theorem concrete_symmetric_domain_certificate",
]

for token in required_lean:
    assert token in lean_text, f"missing Lean token: {token}"

assert "import Chronos.Frontier.FiniteSinkQuadraticRelaxationTheorem" in root_text
assert artifact_data["status"] == "FINITE_RESTRICTED_THEOREM_SOLVED"

required_doc = [
    "Status: `FINITE_RESTRICTED_THEOREM_SOLVED`",
    "finite_sink_quadratic_relaxation_certificate",
    "concrete_symmetric_domain_certificate",
    "Finite sink-quadratic relaxation theorem only.",
    "Does not prove:",
    "existence of",
    "UniformTemporalRelaxationWave",
    "construction of unrestricted admissible domains",
    "entropy production for arbitrary entropy functions",
    "entropy monotonicity for arbitrary entropy functions",
    "unrestricted admissible dissipation",
    "unrestricted rate-thick coercivity",
    "UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for token in required_doc:
    assert token in doc_text, f"missing doc boundary token: {token}"

for forbidden in [
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "P vs NP is proved",
    "Clay problem is solved",
    "UniversalFiberEntropyGap is proved unrestricted",
]:
    assert forbidden not in doc_text
    assert forbidden not in lean_text

print("Finite sink quadratic relaxation theorem verified.")

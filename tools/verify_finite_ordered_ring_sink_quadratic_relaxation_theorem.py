#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path.cwd()
lean = ROOT / "lean/Chronos/Frontier/FiniteOrderedRingSinkQuadraticRelaxationTheorem.lean"
doc = ROOT / "docs/status/FINITE_ORDERED_RING_SINK_QUADRATIC_RELAXATION_THEOREM_2026_05_19.md"
artifact = ROOT / "artifacts/chronos/finite_ordered_ring_sink_quadratic_relaxation_theorem_2026_05_19.json"
root_import = ROOT / "lean/Chronos.lean"
lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_data = json.loads(artifact.read_text())
root_text = root_import.read_text()
required_lean = [
"structure QuadraticSinkOrderData",
"zero_square_zero",
"square_nonnegative",
"def orderedRingSinkRelax",
"def orderedRingQuadraticEntropy",
"def orderedRingClosedUnderSinkRelaxation",
"def orderedRingEntropyProductionOn",
"def orderedRingEntropyMonotoneOn",
"structure FiniteOrderedRingSinkQuadraticRelaxationCertificate",
"theorem ordered_ring_quadratic_entropy_monotone_to_sink",
"theorem ordered_ring_quadratic_entropy_production_nonnegative",
"theorem finite_ordered_ring_sink_quadratic_relaxation_certificate",
"def intQuadraticSinkOrderData",
"def ratQuadraticSinkOrderData",
"theorem finite_ordered_ring_sink_quadratic_relaxation_certificate_int",
"theorem finite_ordered_ring_sink_quadratic_relaxation_certificate_rat",
"mul_self_nonneg",
]
missing_lean = [token for token in required_lean if token not in lean_text]
assert not missing_lean, f"missing Lean tokens: {missing_lean}"
assert "import Chronos.Frontier.FiniteOrderedRingSinkQuadraticRelaxationTheorem" in root_text
assert artifact_data["status"] == "FINITE_ORDERED_DATA_RESTRICTED_THEOREM_SOLVED"
required_doc = [
"FINITE_ORDERED_DATA_RESTRICTED_THEOREM_SOLVED",
"QuadraticSinkOrderData",
"explicit square-nonnegative quadratic sink order data",
"finite_ordered_ring_sink_quadratic_relaxation_certificate",
"finite_ordered_ring_sink_quadratic_relaxation_certificate_int",
"finite_ordered_ring_sink_quadratic_relaxation_certificate_rat",
"finite integer and finite rational domains",
"Finite ordered-data sink-quadratic relaxation theorem only.",
"Does not prove:",
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
missing_doc = [token for token in required_doc if token not in doc_text]
assert not missing_doc, f"missing doc boundary tokens: {missing_doc}"
forbidden = [
"unrestricted Chronos-RR is proved",
"unrestricted H4.1/FGL is proved",
"P vs NP is proved",
"Clay problem is solved",
"UniversalFiberEntropyGap is proved unrestricted",
]
violations = [token for token in forbidden if token in doc_text or token in lean_text]
assert not violations, f"forbidden overclaim tokens: {violations}"
print("Finite ordered-data sink quadratic relaxation theorem verified.")

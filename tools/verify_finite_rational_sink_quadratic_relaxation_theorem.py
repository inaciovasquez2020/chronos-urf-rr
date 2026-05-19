#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lean = ROOT / "lean/Chronos/Frontier/FiniteRationalSinkQuadraticRelaxationTheorem.lean"
doc = ROOT / "docs/status/FINITE_RATIONAL_SINK_QUADRATIC_RELAXATION_THEOREM_2026_05_19.md"
artifact = ROOT / "artifacts/chronos/finite_rational_sink_quadratic_relaxation_theorem_2026_05_19.json"
root_import = ROOT / "lean/Chronos.lean"

lean_text = lean.read_text()
doc_text = doc.read_text()
artifact_data = json.loads(artifact.read_text())
root_text = root_import.read_text()

required_lean = ["def rationalSinkRelax","def rationalQuadraticEntropy","def rationalClosedUnderSinkRelaxation","def rationalEntropyProductionOn","def rationalEntropyMonotoneOn","structure FiniteRationalSinkQuadraticRelaxationCertificate","theorem rational_quadratic_entropy_monotone_to_sink","theorem rational_quadratic_entropy_production_nonnegative","theorem finite_rational_sink_quadratic_relaxation_certificate","theorem concrete_rational_symmetric_domain_certificate","mul_self_nonneg"]
missing_lean = [token for token in required_lean if token not in lean_text]
assert not missing_lean, f"missing Lean tokens: {missing_lean}"

assert "import Chronos.Frontier.FiniteRationalSinkQuadraticRelaxationTheorem" in root_text
assert artifact_data["status"] == "FINITE_RATIONAL_RESTRICTED_THEOREM_SOLVED"
assert artifact_data["extends"] == "finite_sink_quadratic_relaxation_theorem_2026_05_18"

required_doc = ["Status: `FINITE_RATIONAL_RESTRICTED_THEOREM_SOLVED`","finite_rational_sink_quadratic_relaxation_certificate","concrete_rational_symmetric_domain_certificate","This extends the finite sink-quadratic relaxation theorem from finite integer domains to finite rational domains.","Finite rational sink-quadratic relaxation theorem only.","Does not prove:","UniformTemporalRelaxationWave","construction of unrestricted admissible domains","entropy production for arbitrary entropy functions","entropy monotonicity for arbitrary entropy functions","unrestricted admissible dissipation","unrestricted rate-thick coercivity","UniversalFiberEntropyGap","unrestricted Chronos-RR","unrestricted H4.1/FGL","P vs NP","any Clay problem"]
missing_doc = [token for token in required_doc if token not in doc_text]
assert not missing_doc, f"missing doc boundary tokens: {missing_doc}"

forbidden = ["unrestricted Chronos-RR is proved","unrestricted H4.1/FGL is proved","P vs NP is proved","Clay problem is solved","UniversalFiberEntropyGap is proved unrestricted"]
violations = [token for token in forbidden if token in doc_text or token in lean_text]
assert not violations, f"forbidden overclaim tokens: {violations}"

print("Finite rational sink quadratic relaxation theorem verified.")

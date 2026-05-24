#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/R1R2R3SemanticTheoremProofTargets.lean"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/r1_r2_r3_semantic_theorem_proof_targets_2026_05_24.json"
STATUS = ROOT / "docs/status/R1_R2_R3_SEMANTIC_THEOREM_PROOF_TARGETS_2026_05_24.md"

lean = LEAN.read_text()
root_import = ROOT_IMPORT.read_text()
artifact = json.loads(ARTIFACT.read_text())
status = STATUS.read_text()

required_lean_tokens = [
    "structure R1SemanticData",
    "def R1LongChordExclusionTheorem",
    "structure R1TheoremProofInputs",
    "theorem R1_LongChordExclusion_from_semantic_inputs",
    "structure R2SemanticData",
    "def R2DiameterSeparationFillingObstructionTheorem",
    "structure R2TheoremProofInputs",
    "theorem R2_DiameterSeparationFillingObstruction_from_semantic_inputs",
    "structure R3SemanticData",
    "def R3UniformLocalTypeCapacityTheorem",
    "structure R3TheoremProofInputs",
    "theorem R3_UniformLocalTypeCapacity_from_semantic_inputs",
    "structure R1R2R3SemanticTheoremProofData",
    "theorem R1_R2_R3_theorem_proof_targets_from_semantic_inputs",
    "structure R1R2R3ConcreteSemanticObjects",
    "def R1R2R3ConcreteSemanticsSupplied",
    "theorem no_R1_R2_R3_theorem_promotion_without_concrete_semantics",
]
for token in required_lean_tokens:
    assert token in lean, f"missing Lean token: {token}"

for forbidden in [
    "axiom ",
    "admit",
    "sorry",
    "unconditional proof",
    "proved LongChordExclusion",
    "proved DiameterSeparationFillingObstruction",
    "proved UniformLocalTypeCapacity",
    "proved NON_FACTORISATION",
    "proved Chronos-RR",
    "proved H4.1/FGL",
    "P vs NP proved",
    "Clay problem solved",
]:
    assert forbidden not in lean, f"forbidden Lean token present: {forbidden}"

assert "import Chronos.Frontier.R1R2R3SemanticTheoremProofTargets" in root_import

assert artifact["status"] == "CONDITIONAL_SEMANTIC_THEOREM_PROOF_ROUTE_ONLY"

for token in [
    "concreteR1WordEdgeFaceSupportModel",
    "concreteR2FiberChainBoundaryDiameterModel",
    "concreteR3LocalTypeQuotientDimensionModel",
]:
    assert token in artifact["required_concrete_semantic_objects"], f"missing semantic object: {token}"
    assert token in status, f"missing status semantic object: {token}"

for phrase in [
    "conditional theorem-proof route only",
    "does not prove concrete R1 semantics",
    "does not prove concrete R2 semantics",
    "does not prove concrete R3 semantics",
    "does not prove LongChordExclusion",
    "does not prove DiameterSeparationFillingObstruction",
    "does not prove UniformLocalTypeCapacity",
    "does not prove NON_FACTORISATION",
    "does not prove Chronos-RR",
    "does not prove H4.1/FGL",
    "does not prove P vs NP",
    "does not prove any Clay problem",
]:
    assert phrase in artifact["boundary"], f"missing artifact boundary: {phrase}"
    assert phrase in status, f"missing status boundary: {phrase}"

print("R1/R2/R3 semantic theorem-proof targets verified.")

#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos" / "CPDLCCSLGate.lean"
doc = root / "docs" / "status" / "CHRONOS_CPDL_CCSL_CONDITIONAL_GATE_2026_05_04.md"
artifact = root / "artifacts" / "chronos" / "cpdl_ccsl_conditional_gate.json"

for path in (lean, doc, artifact):
    assert path.exists(), f"missing {path}"

lean_text = lean.read_text()
required_lean = [
    "structure CPDLGate",
    "def ValidChr",
    "structure CCSLGate",
    "structure CPDLCCSLGate",
    "def MissingCPDLCCSLWitness",
    "CPDLCCSLGate.ofWitness",
    "theorem ccsl_injective",
    "theorem cpdl_validity_of_ccsl_embedding",
]
for token in required_lean:
    assert token in lean_text, f"missing Lean token: {token}"

doc_text = doc.read_text()
required_doc = [
    "Status: CONDITIONAL_GATE_ONLY",
    "MissingCPDLCCSLWitness",
    "does not construct",
    "does not define",
    "does not prove ChronosCertificateEmbedding",
    "does not prove H4.1/FGL theorem closure",
    "does not prove P vs NP closure",
]
for token in required_doc:
    assert token in doc_text, f"missing doc token: {token}"

data = json.loads(artifact.read_text())
assert data["status"] == "CONDITIONAL_GATE_ONLY"
assert data["cpdl_gate"] == "DEFINED"
assert data["ccsl_gate"] == "DEFINED"
assert data["missing_object"] == "MissingCPDLCCSLWitness G"
assert data["theorem_closure"] is False
assert data["chronos_certificate_embedding"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False

print("Chronos CPDL+CCSL conditional gate verified: CONDITIONAL_GATE_ONLY")

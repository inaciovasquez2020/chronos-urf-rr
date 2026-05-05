#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos" / "CPDLCCSLBitTraceWitness.lean"
DOC = ROOT / "docs" / "status" / "CHRONOS_CPDL_CCSL_BITTRACE_WITNESS_2026_05_05.md"
ARTIFACT = ROOT / "artifacts" / "chronos" / "cpdl_ccsl_bittrace_witness.json"

assert LEAN.exists(), f"missing file: {LEAN}"
assert DOC.exists(), f"missing file: {DOC}"
assert ARTIFACT.exists(), f"missing file: {ARTIFACT}"

lean_text = LEAN.read_text()
assert "structure CPDLGate" in lean_text
assert "def ValidChr" in lean_text
assert "structure CCSLGate" in lean_text
assert "structure CPDLCCSLGate" in lean_text
assert "def MissingCPDLCCSLWitness" in lean_text
assert "abbrev BitTraceTChr" in lean_text
assert "def bitTraceCPDL" in lean_text
assert "def bitTraceEmbed" in lean_text
assert "theorem bitTraceEmbed_injective" in lean_text
assert "theorem bitTrace_missingCPDLCCSLWitness" in lean_text
assert "def bitTraceCCSL" in lean_text
assert "def bitTraceCPDLCCSLGate" in lean_text
assert "theorem bitTrace_cpdl_validity" in lean_text
assert "theorem bitTrace_ccsl_injective" in lean_text
assert "theorem bitTrace_ccsl_size_lower_bound" not in lean_text

doc_text = DOC.read_text()
assert "Status: MODEL_WITNESS_ONLY" in doc_text
assert "model-level witness only" in doc_text
assert "does not bind the witness to the native Chronos certificate carrier" in doc_text
assert "does not construct" in doc_text
assert "does not define" in doc_text
assert "does not prove ChronosCertificateEmbedding" in doc_text
assert "does not prove H4.1/FGL theorem closure" in doc_text
assert "does not prove P vs NP closure" in doc_text

data = json.loads(ARTIFACT.read_text())
assert data["status"] == "MODEL_WITNESS_ONLY"
assert data["missing_witness_closed"] is True
assert data["ccsl_size_lower_bound_closed"] is False
assert data["native_chronos_certificate_carrier"] is False
assert data["nu_n_defined"] is False
assert data["entropy_bridge"] is False
assert data["chronos_certificate_embedding"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False

if shutil.which("lake") is not None:
    subprocess.run(["lake", "env", "lean", str(LEAN)], cwd=ROOT, check=True)

print("Chronos CPDL+CCSL bittrace witness verified: MODEL_WITNESS_ONLY")

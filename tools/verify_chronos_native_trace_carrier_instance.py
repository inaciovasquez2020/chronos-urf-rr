#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos" / "NativeTraceCarrierInstance.lean"
DOC = ROOT / "docs" / "status" / "CHRONOS_NATIVE_TRACE_CARRIER_INSTANCE_2026_05_05.md"
ARTIFACT = ROOT / "artifacts" / "chronos" / "native_trace_carrier_instance.json"

assert LEAN.exists(), f"missing file: {LEAN}"
assert DOC.exists(), f"missing file: {DOC}"
assert ARTIFACT.exists(), f"missing file: {ARTIFACT}"

lean_text = LEAN.read_text()
assert "structure NativeTraceCarrier" in lean_text
assert "def nativeTracePredicate" in lean_text
assert "def nativeTraceEncode" in lean_text
assert "def nativeTraceDecode" in lean_text
assert "theorem nativeTraceDecodeEncode" in lean_text
assert "def nativeTraceBinding" in lean_text
assert "def nativeTraceCPDL" in lean_text
assert "theorem nativeTraceMissingCPDLCCSLWitness" in lean_text
assert "theorem nativeTraceEmbedInjective" in lean_text

doc_text = DOC.read_text()
assert "Status: MODEL_NATIVE_CARRIER_INSTANCE_ONLY" in doc_text
assert "model native-carrier instance only" in doc_text
assert "does not identify the model carrier with the repository-native Chronos certificate carrier" in doc_text
assert "does not construct `C_n^Chr`" in doc_text
assert "does not define `nu_n`" in doc_text
assert "does not prove the entropy bridge" in doc_text
assert "does not prove ChronosCertificateEmbedding" in doc_text
assert "does not prove H4.1/FGL theorem closure" in doc_text
assert "does not prove P vs NP closure" in doc_text

data = json.loads(ARTIFACT.read_text())
assert data["status"] == "MODEL_NATIVE_CARRIER_INSTANCE_ONLY"
assert data["decode_encode_closed"] is True
assert data["missing_cpdl_ccsl_witness_closed_for_model"] is True
assert data["repository_native_carrier_identified"] is False
assert data["c_n_chr_defined"] is False
assert data["nu_n_defined"] is False
assert data["entropy_bridge"] is False
assert data["chronos_certificate_embedding"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False

if shutil.which("lake") is not None:
    subprocess.run(["lake", "env", "lean", str(LEAN)], cwd=ROOT, check=True)

print("Chronos native trace carrier instance verified: MODEL_NATIVE_CARRIER_INSTANCE_ONLY")

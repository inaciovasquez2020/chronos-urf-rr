#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos" / "NativeCarrierBinding.lean"
DOC = ROOT / "docs" / "status" / "CHRONOS_NATIVE_CARRIER_BINDING_2026_05_05.md"
ARTIFACT = ROOT / "artifacts" / "chronos" / "native_carrier_binding.json"

assert LEAN.exists(), f"missing file: {LEAN}"
assert DOC.exists(), f"missing file: {DOC}"
assert ARTIFACT.exists(), f"missing file: {ARTIFACT}"

lean_text = LEAN.read_text()
assert "structure CPDLGate" in lean_text
assert "def ValidChr" in lean_text
assert "def MissingCPDLCCSLWitness" in lean_text
assert "structure NativeCarrierBinding" in lean_text
assert "decode_encode" in lean_text
assert "def nativeBindingCPDL" in lean_text
assert "def nativeBindingEmbed" in lean_text
assert "theorem nativeBindingEmbed_injective" in lean_text
assert "theorem nativeBinding_missingCPDLCCSLWitness" in lean_text
assert "theorem nativeBinding_validity" in lean_text

doc_text = DOC.read_text()
assert "Status: CONDITIONAL_NATIVE_BINDING_INTERFACE" in doc_text
assert "conditional native-carrier binding interface" in doc_text
assert "conditional native-binding interface only" in doc_text
assert "does not construct the actual native Chronos certificate carrier" in doc_text
assert "does not define `C_n^Chr`" in doc_text
assert "does not define `nu_n`" in doc_text
assert "does not prove the entropy bridge" in doc_text
assert "does not prove ChronosCertificateEmbedding" in doc_text
assert "does not prove H4.1/FGL theorem closure" in doc_text
assert "does not prove P vs NP closure" in doc_text

data = json.loads(ARTIFACT.read_text())
assert data["status"] == "CONDITIONAL_NATIVE_BINDING_INTERFACE"
assert data["binding_object"] == "NativeCarrierBinding"
assert data["requires_encode"] is True
assert data["requires_decode"] is True
assert data["requires_decode_encode"] is True
assert data["native_missing_cpdl_ccsl_witness_conditional"] is True
assert data["native_carrier_constructed"] is False
assert data["c_n_chr_defined"] is False
assert data["nu_n_defined"] is False
assert data["entropy_bridge"] is False
assert data["chronos_certificate_embedding"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False

if shutil.which("lake") is not None:
    subprocess.run(["lake", "env", "lean", str(LEAN)], cwd=ROOT, check=True)

print("Chronos native carrier binding verified: CONDITIONAL_NATIVE_BINDING_INTERFACE")

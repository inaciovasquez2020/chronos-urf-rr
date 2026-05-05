#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import shutil
ROOT = Path(file).resolve().parents[1]
LEAN = ROOT / "Chronos" / "RepositoryNativeCarrierIso.lean"
DOC = ROOT / "docs" / "status" / "CHRONOS_REPOSITORY_NATIVE_CARRIER_ISO_2026_05_05.md"
ARTIFACT = ROOT / "artifacts" / "chronos" / "repository_native_carrier_iso.json"
assert LEAN.exists(), f"missing file: {LEAN}"
assert DOC.exists(), f"missing file: {DOC}"
assert ARTIFACT.exists(), f"missing file: {ARTIFACT}"
lean_text = LEAN.read_text()
assert "structure RepositoryNativeCarrierIso" in lean_text
assert "def repoCPDL" in lean_text
assert "def repoEmbed" in lean_text
assert "theorem repoEmbed_injective" in lean_text
assert "theorem repo_missingCPDLCCSLWitness" in lean_text
assert "theorem repo_validity" in lean_text
assert "modelTraceDecodeEncode" in lean_text
assert "from_to" in lean_text
doc_text = DOC.read_text()
assert "Status: CONDITIONAL_REPOSITORY_NATIVE_ISO_INTERFACE" in doc_text
assert "conditional repository-native iso interface only" in doc_text
assert "does not construct the actual repository-native Chronos certificate carrier" in doc_text
assert "does not identify any existing repository certificate type with ModelTraceCarrier" in doc_text
assert "does not define C_n^Chr" in doc_text
assert "does not define nu_n" in doc_text
assert "does not prove the entropy bridge" in doc_text
assert "does not prove ChronosCertificateEmbedding" in doc_text
assert "does not prove H4.1/FGL theorem closure" in doc_text
assert "does not prove P vs NP closure" in doc_text
data = json.loads(ARTIFACT.read_text())
assert data["status"] == "CONDITIONAL_REPOSITORY_NATIVE_ISO_INTERFACE"
assert data["iso_object"] == "RepositoryNativeCarrierIso"
assert data["requires_to_repo"] is True
assert data["requires_from_repo"] is True
assert data["requires_from_to"] is True
assert data["repo_missing_cpdl_ccsl_witness_conditional"] is True
assert data["actual_repository_carrier_constructed"] is False
assert data["repository_carrier_identified_with_model"] is False
assert data["c_n_chr_defined"] is False
assert data["nu_n_defined"] is False
assert data["entropy_bridge"] is False
assert data["chronos_certificate_embedding"] is False
assert data["h41_fgl_closure"] is False
assert data["p_vs_np_closure"] is False
if shutil.which("lake") is not None:
subprocess.run(["lake", "env", "lean", str(LEAN)], cwd=ROOT, check=True)
print("Chronos repository native carrier iso verified: CONDITIONAL_REPOSITORY_NATIVE_ISO_INTERFACE")

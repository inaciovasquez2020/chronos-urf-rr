#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "Chronos/RepositoryNativeCarrierSelection.lean"
DOC = ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_CARRIER_SELECTION_2026_05_05.md"
ARTIFACT = ROOT / "artifacts/chronos/repository_native_carrier_selection.json"

lean_text = LEAN.read_text()
doc_text = DOC.read_text()
data = json.loads(ARTIFACT.read_text())

for token in [
    "structure RepositoryNativeCarrierSelection",
    "selectedCPDL",
    "selectedEmbed",
    "selectedEmbed_injective",
    "selected_missingCPDLCCSLWitness",
    "selected_validity",
    "selectedEmbed_property",
]:
    assert token in lean_text

assert "Status: CONDITIONAL_SELECTION_OBJECT_ONLY" in doc_text
assert "S : RepositoryNativeCarrierSelection" in doc_text
assert "does not construct the actual repository carrier" in doc_text
assert "does not identify the repository carrier with ModelTraceCarrier" in doc_text
assert "does not define C_n^Chr" in doc_text
assert "does not define nu_n" in doc_text
assert "does not prove the entropy bridge" in doc_text
assert "does not prove ChronosCertificateEmbedding" in doc_text
assert "does not prove H4.1/FGL theorem closure" in doc_text
assert "does not prove P vs NP closure" in doc_text

assert data["status"] == "CONDITIONAL_SELECTION_OBJECT_ONLY"
assert data["selection_object"] == "RepositoryNativeCarrierSelection"
assert data["requires_TRepo"] is True
assert data["requires_iso"] is True
assert data["selected_missing_cpdl_ccsl_witness_conditional"] is True
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

print("Chronos repository native carrier selection verified: CONDITIONAL_SELECTION_OBJECT_ONLY")

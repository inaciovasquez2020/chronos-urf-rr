from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_repository_native_carrier_iso_artifact():
    data = json.loads((ROOT / "artifacts/chronos/repository_native_carrier_iso.json").read_text())
    assert data["status"] == "CONDITIONAL_REPOSITORY_NATIVE_ISO_INTERFACE"
    assert data["iso_object"] == "RepositoryNativeCarrierIso"
    assert data["repo_missing_cpdl_ccsl_witness_conditional"] is True
    assert data["actual_repository_carrier_constructed"] is False
    assert data["repository_carrier_identified_with_model"] is False
    assert data["chronos_certificate_embedding"] is False
    assert data["h41_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False

def test_repository_native_carrier_iso_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_CARRIER_ISO_2026_05_05.md").read_text()
    assert "Status: CONDITIONAL_REPOSITORY_NATIVE_ISO_INTERFACE" in text
    assert "conditional repository-native iso interface only" in text
    assert "does not construct the actual repository-native Chronos certificate carrier" in text
    assert "does not identify any existing repository certificate type with `ModelTraceCarrier`" in text
    assert "does not prove ChronosCertificateEmbedding" in text
    assert "does not prove H4.1/FGL theorem closure" in text
    assert "does not prove P vs NP closure" in text

def test_repository_native_carrier_iso_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_repository_native_carrier_iso.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CONDITIONAL_REPOSITORY_NATIVE_ISO_INTERFACE" in result.stdout

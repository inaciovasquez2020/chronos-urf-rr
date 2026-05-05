from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_native_carrier_binding_artifact():
    data = json.loads((ROOT / "artifacts/chronos/native_carrier_binding.json").read_text())
    assert data["status"] == "CONDITIONAL_NATIVE_BINDING_INTERFACE"
    assert data["binding_object"] == "NativeCarrierBinding"
    assert data["native_missing_cpdl_ccsl_witness_conditional"] is True
    assert data["native_carrier_constructed"] is False
    assert data["chronos_certificate_embedding"] is False
    assert data["h41_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False

def test_native_carrier_binding_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_NATIVE_CARRIER_BINDING_2026_05_05.md").read_text()
    assert "Status: CONDITIONAL_NATIVE_BINDING_INTERFACE" in text
    assert "conditional native-carrier binding interface" in text
    assert "does not construct the actual native Chronos certificate carrier" in text
    assert "does not prove ChronosCertificateEmbedding" in text
    assert "does not prove H4.1/FGL theorem closure" in text
    assert "does not prove P vs NP closure" in text

def test_native_carrier_binding_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_native_carrier_binding.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CONDITIONAL_NATIVE_BINDING_INTERFACE" in result.stdout

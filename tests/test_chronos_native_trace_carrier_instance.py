from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_native_trace_carrier_instance_artifact():
    data = json.loads((ROOT / "artifacts/chronos/native_trace_carrier_instance.json").read_text())
    assert data["status"] == "MODEL_NATIVE_CARRIER_INSTANCE_ONLY"
    assert data["decode_encode_closed"] is True
    assert data["missing_cpdl_ccsl_witness_closed_for_model"] is True
    assert data["repository_native_carrier_identified"] is False
    assert data["chronos_certificate_embedding"] is False
    assert data["h41_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False

def test_native_trace_carrier_instance_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_NATIVE_TRACE_CARRIER_INSTANCE_2026_05_05.md").read_text()
    assert "Status: MODEL_NATIVE_CARRIER_INSTANCE_ONLY" in text
    assert "model native-carrier instance only" in text
    assert "does not identify the model carrier with the repository-native Chronos certificate carrier" in text
    assert "does not prove ChronosCertificateEmbedding" in text
    assert "does not prove H4.1/FGL theorem closure" in text
    assert "does not prove P vs NP closure" in text

def test_native_trace_carrier_instance_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_native_trace_carrier_instance.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "MODEL_NATIVE_CARRIER_INSTANCE_ONLY" in result.stdout

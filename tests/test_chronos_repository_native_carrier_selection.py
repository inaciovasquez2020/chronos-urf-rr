import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_repository_native_carrier_selection_artifact():
    data = json.loads((ROOT / "artifacts/chronos/repository_native_carrier_selection.json").read_text())
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

def test_repository_native_carrier_selection_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_repository_native_carrier_selection.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CONDITIONAL_SELECTION_OBJECT_ONLY" in result.stdout

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_carrier_support_signature_invariant_artifact():
    data = json.loads((ROOT / "artifacts/chronos/carrier_support_signature_invariant.json").read_text())
    assert data["status"] == "CONDITIONAL_CLASSIFICATION_INVARIANT"
    assert data["new_ingredient"] == "finite support signature classification"
    assert "CarrierRegistryExhaustiveness follows" in data["conditional_result"]
    assert data["boundary"]["carrier_registry_exhaustiveness"] == "NO_CARRIER_REGISTRY_EXHAUSTIVENESS_PROOF"
    assert data["boundary"]["unrestricted_reg_snf"] == "NO_UNRESTRICTED_REG_SNF_CLOSURE"
    assert data["boundary"]["universal_fiber_entropy_gap"] == "NO_UNIVERSAL_FIBER_ENTROPY_GAP_PROOF"
    assert data["boundary"]["depth_bridge"] == "NO_DEPTH_BRIDGE_EXTENSION_BEYOND_SELECTED_FINAL_CARRIER_DOMAIN"

def test_carrier_support_signature_invariant_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_CARRIER_SUPPORT_SIGNATURE_INVARIANT_2026_05_10.md").read_text()
    assert "Status: CONDITIONAL_CLASSIFICATION_INVARIANT" in text
    assert "CarrierRegistryExhaustiveness remains FRONTIER_OPEN" in text
    assert "No CarrierRegistryExhaustiveness proof." in text
    assert "No unrestricted Reg-SNF closure." in text
    assert "No UniversalFiberEntropyGap proof." in text
    assert "No DepthBridge extension beyond selected final carrier domain." in text
    assert "No Chronos-RR closure." in text
    assert "No H4.1/FGL closure." in text
    assert "No P vs NP closure." in text
    assert "No Clay-problem closure." in text

def test_carrier_support_signature_invariant_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_carrier_support_signature_invariant.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CarrierSupportSignatureInvariant verified: CONDITIONAL_CLASSIFICATION_INVARIANT" in result.stdout

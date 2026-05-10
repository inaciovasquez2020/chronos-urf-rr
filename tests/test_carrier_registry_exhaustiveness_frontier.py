import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_carrier_registry_exhaustiveness_frontier_artifact():
    data = json.loads((ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_frontier.json").read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["weakest_missing_lemma"] == "CarrierRegistryExhaustiveness"
    assert data["boundary"]["chronos_rr"] == "NO_CHRONOS_RR_CLOSURE"
    assert data["boundary"]["h4_1_fgl"] == "NO_H4_1_FGL_CLOSURE"
    assert data["boundary"]["p_vs_np"] == "NO_P_VS_NP_CLOSURE"
    assert data["boundary"]["clay"] == "NO_CLAY_PROBLEM_CLOSURE"
    assert data["boundary"]["universal_fiber_entropy_gap"] == "NO_UNIVERSAL_FIBER_ENTROPY_GAP_PROOF"
    assert data["boundary"]["depth_bridge"] == "NO_DEPTH_BRIDGE_EXTENSION_BEYOND_SELECTED_FINAL_CARRIER_DOMAIN"

def test_carrier_registry_exhaustiveness_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_CARRIER_REGISTRY_EXHAUSTIVENESS_FRONTIER_2026_05_10.md").read_text()
    assert "Status: FRONTIER_OPEN" in text
    assert "No Chronos-RR closure." in text
    assert "No H4.1/FGL closure." in text
    assert "No P vs NP closure." in text
    assert "No Clay-problem closure." in text
    assert "No UniversalFiberEntropyGap proof." in text
    assert "No unrestricted Reg-SNF closure is claimed by this artifact." in text

def test_carrier_registry_exhaustiveness_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_carrier_registry_exhaustiveness_frontier.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CarrierRegistryExhaustiveness frontier verified: FRONTIER_OPEN" in result.stdout

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_repository_registered_reg_snf_closure_artifact():
    data = json.loads((ROOT / "artifacts/chronos/repository_registered_reg_snf_closure.json").read_text())
    assert data["status"] == "WEAKENED_THEOREM_PACKAGE"
    assert data["domain"] == "REPOSITORY_REGISTERED_CARRIERS_ONLY"
    assert data["boundary"]["unrestricted_reg_snf"] == "NO_UNRESTRICTED_REG_SNF_CLOSURE"
    assert data["boundary"]["carrier_registry_exhaustiveness"] == "NO_CARRIER_REGISTRY_EXHAUSTIVENESS_PROOF"
    assert data["boundary"]["universal_fiber_entropy_gap"] == "NO_UNIVERSAL_FIBER_ENTROPY_GAP_PROOF"
    assert data["boundary"]["depth_bridge"] == "NO_DEPTH_BRIDGE_EXTENSION_BEYOND_SELECTED_FINAL_CARRIER_DOMAIN"
    assert data["boundary"]["chronos_rr"] == "NO_CHRONOS_RR_CLOSURE"
    assert data["boundary"]["h4_1_fgl"] == "NO_H4_1_FGL_CLOSURE"
    assert data["boundary"]["p_vs_np"] == "NO_P_VS_NP_CLOSURE"
    assert data["boundary"]["clay"] == "NO_CLAY_PROBLEM_CLOSURE"

def test_carrier_registry_exhaustiveness_remains_open():
    data = json.loads((ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_frontier.json").read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["weakest_missing_lemma"] == "CarrierRegistryExhaustiveness"

def test_repository_registered_reg_snf_closure_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_REPOSITORY_REGISTERED_REG_SNF_CLOSURE_2026_05_10.md").read_text()
    assert "Status: WEAKENED_THEOREM_PACKAGE" in text
    assert "REPOSITORY_REGISTERED_CARRIERS_ONLY" in text
    assert "CarrierRegistryExhaustiveness remains FRONTIER_OPEN." in text
    assert "No unrestricted Reg-SNF closure." in text
    assert "No CarrierRegistryExhaustiveness proof." in text
    assert "No UniversalFiberEntropyGap proof." in text
    assert "No DepthBridge extension beyond selected final carrier domain." in text
    assert "No Chronos-RR closure." in text
    assert "No H4.1/FGL closure." in text
    assert "No P vs NP closure." in text
    assert "No Clay-problem closure." in text

def test_repository_registered_reg_snf_closure_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_repository_registered_reg_snf_closure.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "Repository-registered Reg-SNF closure package verified: WEAKENED_THEOREM_PACKAGE" in result.stdout

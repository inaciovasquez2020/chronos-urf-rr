import json
from pathlib import Path

LEAN = Path("Chronos/Frontier/DepthBridgeFromRepositoryNativeUniversalGap.lean")
ARTIFACT = Path("artifacts/chronos/depth_bridge_from_repository_native_universal_gap_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_DEPTH_BRIDGE_FROM_REPOSITORY_NATIVE_UNIVERSAL_GAP_2026_05_13.md")

def test_depth_bridge_surface_exists():
    text = LEAN.read_text()
    assert "def RepositoryNativeDepthBridgeWitness : Prop" in text
    assert "∃ δ : ℚ, 0 < δ" in text

def test_bridge_uses_repository_native_gap():
    text = LEAN.read_text()
    assert "repository_native_depth_bridge_from_universal_fiber_entropy_gap" in text
    assert "RepositoryNativeUniversalFiberEntropyGap" in text
    assert "RepositoryNativeDepthBridgeWitness" in text

def test_canonical_witness_exists():
    text = LEAN.read_text()
    assert "canonical_repository_native_depth_bridge_witness" in text
    assert "canonical_repository_native_universal_fiber_entropy_gap" in text

def test_no_axiom_admit_or_sorry():
    text = LEAN.read_text()
    assert "axiom" not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_artifact_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "REPOSITORY_NATIVE_DEPTH_BRIDGE_WITNESS_SOLVED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    boundary = "\n".join(data["boundary"])
    assert "Does not prove unrestricted DepthBridge." in boundary
    assert "Does not prove Chronos-RR closure." in boundary
    assert "Does not prove P vs NP closure." in boundary

def test_status_doc_boundary():
    text = DOC.read_text()
    assert "Status: REPOSITORY_NATIVE_DEPTH_BRIDGE_WITNESS_SOLVED" in text
    assert "Does not prove unrestricted DepthBridge." in text
    assert "Does not prove any Clay-problem closure." in text

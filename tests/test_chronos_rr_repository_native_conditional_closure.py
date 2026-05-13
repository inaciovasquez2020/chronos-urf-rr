import json
from pathlib import Path

LEAN = Path("Chronos/Frontier/ChronosRRRepositoryNativeConditionalClosure.lean")
ARTIFACT = Path("artifacts/chronos/chronos_rr_repository_native_conditional_closure_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_RR_REPOSITORY_NATIVE_CONDITIONAL_CLOSURE_2026_05_13.md")

def test_conditional_closure_surface_exists():
    text = LEAN.read_text()
    assert "def RepositoryNativeChronosRRConditionalClosure : Prop" in text
    assert "RepositoryNativeDepthBridgeWitness" in text

def test_bridge_uses_depth_bridge_witness():
    text = LEAN.read_text()
    assert "repository_native_chronos_rr_conditional_closure_from_depth_bridge" in text
    assert "(h : RepositoryNativeDepthBridgeWitness)" in text
    assert "RepositoryNativeChronosRRConditionalClosure" in text

def test_canonical_witness_exists():
    text = LEAN.read_text()
    assert "canonical_repository_native_chronos_rr_conditional_closure" in text
    assert "canonical_repository_native_depth_bridge_witness" in text

def test_no_axiom_admit_or_sorry():
    text = LEAN.read_text()
    assert "axiom" not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_artifact_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "REPOSITORY_NATIVE_CHRONOS_RR_CONDITIONAL_SURFACE_SOLVED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    boundary = "\n".join(data["boundary"])
    assert "Does not prove unrestricted Chronos-RR closure." in boundary
    assert "Does not prove unrestricted DepthBridge." in boundary
    assert "Does not prove P vs NP closure." in boundary

def test_status_doc_boundary():
    text = DOC.read_text()
    assert "Status: REPOSITORY_NATIVE_CHRONOS_RR_CONDITIONAL_SURFACE_SOLVED" in text
    assert "Does not prove unrestricted Chronos-RR closure." in text
    assert "Does not prove any Clay-problem closure." in text

import json
from pathlib import Path

LEAN = Path("Chronos/Frontier/UnrestrictedChronosRRStatusLock.lean")
ARTIFACT = Path("artifacts/chronos/unrestricted_chronos_rr_status_lock_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_UNRESTRICTED_RR_STATUS_LOCK_2026_05_13.md")

def test_status_marker_exists():
    text = LEAN.read_text()
    assert "inductive UnrestrictedChronosRRStatus" in text
    assert "| frontierOpen" in text
    assert "def unrestrictedChronosRRStatusLock" in text

def test_status_lock_uses_obstruction_registry():
    text = LEAN.read_text()
    assert "def UnrestrictedChronosRRStatusLockedOpen" in text
    assert "unrestrictedChronosRRObstructionRegistry.Nonempty" in text
    assert "unrestricted_chronos_rr_obstruction_registry_nonempty" in text

def test_repository_native_conditional_does_not_promote_status():
    text = LEAN.read_text()
    assert "RepositoryNativeConditionalClosurePreservesUnrestrictedOpenStatus" in text
    assert "repository_native_conditional_closure_preserves_unrestricted_open_status" in text
    assert "canonical_repository_native_conditional_closure_preserves_unrestricted_open_status" in text

def test_no_axiom_admit_or_sorry():
    text = LEAN.read_text()
    assert "axiom" not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_artifact_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "UNRESTRICTED_CHRONOS_RR_FRONTIER_OPEN_LOCKED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    boundary = "\n".join(data["boundary"])
    assert "Repository-native conditional closure does not promote unrestricted Chronos-RR status." in boundary
    assert "Does not prove unrestricted Chronos-RR closure." in boundary
    assert "Does not prove P vs NP closure." in boundary

def test_status_doc_boundary():
    text = DOC.read_text()
    assert "Status: UNRESTRICTED_CHRONOS_RR_FRONTIER_OPEN_LOCKED" in text
    assert "Locks unrestricted Chronos-RR status as FRONTIER_OPEN while the obstruction registry is nonempty." in text
    assert "Does not prove any Clay-problem closure." in text

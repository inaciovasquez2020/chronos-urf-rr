import json
from pathlib import Path

LEAN = Path("Chronos/Frontier/H4FGLUnrestrictedStatusLock.lean")
ARTIFACT = Path("artifacts/chronos/h4fgl_unrestricted_status_lock_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_H4FGL_UNRESTRICTED_STATUS_LOCK_2026_05_13.md")

def test_status_marker_exists():
    text = LEAN.read_text()
    assert "inductive H4FGLUnrestrictedStatus" in text
    assert "| frontierOpen" in text
    assert "def h4FGLUnrestrictedStatusLock" in text

def test_status_lock_uses_chronos_rr_status_lock():
    text = LEAN.read_text()
    assert "def H4FGLUnrestrictedStatusLockedOpen" in text
    assert "UnrestrictedChronosRRStatusLockedOpen" in text
    assert "unrestricted_chronos_rr_status_lock_from_obstruction_registry" in text

def test_repository_native_chronos_rr_conditional_does_not_promote_h4fgl_status():
    text = LEAN.read_text()
    assert "RepositoryNativeChronosRRConditionalClosurePreservesH4FGLOpenStatus" in text
    assert "repository_native_chronos_rr_conditional_closure_preserves_h4fgl_open_status" in text
    assert "canonical_repository_native_chronos_rr_conditional_closure_preserves_h4fgl_open_status" in text

def test_no_axiom_admit_or_sorry():
    text = LEAN.read_text()
    assert "axiom" not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_artifact_boundary():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "H4FGL_UNRESTRICTED_FRONTIER_OPEN_LOCKED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    boundary = "\n".join(data["boundary"])
    assert "Repository-native Chronos-RR conditional closure does not promote unrestricted H4.1/FGL status." in boundary
    assert "Does not prove unrestricted H4.1/FGL closure." in boundary
    assert "Does not prove P vs NP closure." in boundary

def test_status_doc_boundary():
    text = DOC.read_text()
    assert "Status: H4FGL_UNRESTRICTED_FRONTIER_OPEN_LOCKED" in text
    assert "Locks unrestricted H4.1/FGL status as FRONTIER_OPEN while unrestricted Chronos-RR remains locked open." in text
    assert "Does not prove any Clay-problem closure." in text

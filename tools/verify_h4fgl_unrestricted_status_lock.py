from pathlib import Path
import json
import re

LEAN = Path("Chronos/Frontier/H4FGLUnrestrictedStatusLock.lean")
ARTIFACT = Path("artifacts/chronos/h4fgl_unrestricted_status_lock_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_H4FGL_UNRESTRICTED_STATUS_LOCK_2026_05_13.md")
ROOT = Path("Chronos.lean")

REQUIRED_LEAN = [
    "import Chronos.Frontier.UnrestrictedChronosRRStatusLock",
    "inductive H4FGLUnrestrictedStatus",
    "| frontierOpen",
    "def h4FGLUnrestrictedStatusLock",
    "def H4FGLUnrestrictedStatusLockedOpen",
    "UnrestrictedChronosRRStatusLockedOpen",
    "theorem h4fgl_unrestricted_status_lock_from_chronos_rr_status_lock",
    "unrestricted_chronos_rr_status_lock_from_obstruction_registry",
    "RepositoryNativeChronosRRConditionalClosurePreservesH4FGLOpenStatus",
    "repository_native_chronos_rr_conditional_closure_preserves_h4fgl_open_status",
    "canonical_repository_native_chronos_rr_conditional_closure_preserves_h4fgl_open_status"
]

REQUIRED_DOC = [
    "Status: H4FGL_UNRESTRICTED_FRONTIER_OPEN_LOCKED",
    "Locks unrestricted H4.1/FGL status as FRONTIER_OPEN while unrestricted Chronos-RR remains locked open.",
    "Repository-native Chronos-RR conditional closure does not promote unrestricted H4.1/FGL status.",
    "Does not prove unrestricted H4.1/FGL closure.",
    "Does not prove unrestricted Chronos-RR closure.",
    "Does not prove unrestricted DepthBridge.",
    "Does not prove unrestricted UniversalFiberEntropyGap.",
    "Does not prove SemanticRankRateToFiberEntropySoundness.",
    "Does not prove P vs NP closure.",
    "Does not prove any Clay-problem closure."
]

def require(path: Path) -> str:
    assert path.exists(), f"missing {path}"
    return path.read_text()

def main() -> None:
    lean = require(LEAN)
    doc = require(DOC)
    root = require(ROOT)
    data = json.loads(require(ARTIFACT))

    for token in REQUIRED_LEAN:
        assert token in lean, f"missing Lean token: {token}"

    for token in REQUIRED_DOC:
        assert token in doc, f"missing doc token: {token}"

    assert "import Chronos.Frontier.H4FGLUnrestrictedStatusLock" in root

    assert data["status"] == "H4FGL_UNRESTRICTED_FRONTIER_OPEN_LOCKED"
    assert data["status_marker"] == "h4FGLUnrestrictedStatusLock"
    assert data["main_theorem"] == "h4fgl_unrestricted_status_lock_from_chronos_rr_status_lock"
    assert data["dependency"] == "unrestricted_chronos_rr_status_lock_from_obstruction_registry"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False

    for pattern in [r"\baxiom\b", r"\badmit\b", r"\bsorry\b"]:
        assert re.search(pattern, lean) is None, f"forbidden Lean token: {pattern}"

    print("H4FGL unrestricted status lock verified.")

if __name__ == "__main__":
    main()

from pathlib import Path
import json
import re

LEAN = Path("Chronos/Frontier/UnrestrictedChronosRRStatusLock.lean")
ARTIFACT = Path("artifacts/chronos/unrestricted_chronos_rr_status_lock_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_UNRESTRICTED_RR_STATUS_LOCK_2026_05_13.md")
ROOT = Path("Chronos.lean")

REQUIRED_LEAN = [
    "import Chronos.Frontier.UnrestrictedChronosRRObstructionRegistry",
    "inductive UnrestrictedChronosRRStatus",
    "| frontierOpen",
    "def unrestrictedChronosRRStatusLock",
    "def UnrestrictedChronosRRStatusLockedOpen",
    "unrestrictedChronosRRObstructionRegistry.Nonempty",
    "theorem unrestricted_chronos_rr_status_lock_from_obstruction_registry",
    "unrestricted_chronos_rr_obstruction_registry_nonempty",
    "def RepositoryNativeConditionalClosurePreservesUnrestrictedOpenStatus",
    "theorem repository_native_conditional_closure_preserves_unrestricted_open_status",
    "theorem canonical_repository_native_conditional_closure_preserves_unrestricted_open_status"
]

REQUIRED_DOC = [
    "Status: UNRESTRICTED_CHRONOS_RR_FRONTIER_OPEN_LOCKED",
    "Locks unrestricted Chronos-RR status as FRONTIER_OPEN while the obstruction registry is nonempty.",
    "Repository-native conditional closure does not promote unrestricted Chronos-RR status.",
    "Does not prove unrestricted Chronos-RR closure.",
    "Does not prove unrestricted DepthBridge.",
    "Does not prove unrestricted UniversalFiberEntropyGap.",
    "Does not prove SemanticRankRateToFiberEntropySoundness.",
    "Does not prove H4.1/FGL closure.",
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

    assert "import Chronos.Frontier.UnrestrictedChronosRRStatusLock" in root

    assert data["status"] == "UNRESTRICTED_CHRONOS_RR_FRONTIER_OPEN_LOCKED"
    assert data["status_marker"] == "unrestrictedChronosRRStatusLock"
    assert data["main_theorem"] == "unrestricted_chronos_rr_status_lock_from_obstruction_registry"
    assert data["dependency"] == "unrestricted_chronos_rr_obstruction_registry_nonempty"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False

    for pattern in [r"\baxiom\b", r"\badmit\b", r"\bsorry\b"]:
        assert re.search(pattern, lean) is None, f"forbidden Lean token: {pattern}"

    print("Unrestricted Chronos-RR status lock verified.")

if __name__ == "__main__":
    main()

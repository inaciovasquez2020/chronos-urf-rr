from pathlib import Path
import json
import re

LEAN = Path("Chronos/Frontier/ChronosRRRepositoryNativeConditionalClosure.lean")
ARTIFACT = Path("artifacts/chronos/chronos_rr_repository_native_conditional_closure_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_RR_REPOSITORY_NATIVE_CONDITIONAL_CLOSURE_2026_05_13.md")
ROOT = Path("Chronos.lean")

REQUIRED_LEAN = [
    "import Chronos.Frontier.DepthBridgeFromRepositoryNativeUniversalGap",
    "def RepositoryNativeChronosRRConditionalClosure : Prop",
    "RepositoryNativeDepthBridgeWitness",
    "theorem repository_native_chronos_rr_conditional_closure_from_depth_bridge",
    "theorem canonical_repository_native_chronos_rr_conditional_closure",
    "canonical_repository_native_depth_bridge_witness"
]

REQUIRED_DOC = [
    "Status: REPOSITORY_NATIVE_CHRONOS_RR_CONDITIONAL_SURFACE_SOLVED",
    "Solves only the repository-native Chronos-RR conditional closure surface.",
    "Depends on the repository-native numerical depth-bridge witness surface.",
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

    assert "import Chronos.Frontier.ChronosRRRepositoryNativeConditionalClosure" in root

    assert data["status"] == "REPOSITORY_NATIVE_CHRONOS_RR_CONDITIONAL_SURFACE_SOLVED"
    assert data["main_theorem"] == "repository_native_chronos_rr_conditional_closure_from_depth_bridge"
    assert data["dependency"] == "repository_native_depth_bridge_from_universal_fiber_entropy_gap"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False

    for pattern in [r"\baxiom\b", r"\badmit\b", r"\bsorry\b"]:
        assert re.search(pattern, lean) is None, f"forbidden Lean token: {pattern}"

    print("Chronos-RR repository-native conditional closure surface verified.")

if __name__ == "__main__":
    main()

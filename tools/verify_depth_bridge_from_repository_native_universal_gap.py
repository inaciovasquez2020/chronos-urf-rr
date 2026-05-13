from pathlib import Path
import json
import re

LEAN = Path("Chronos/Frontier/DepthBridgeFromRepositoryNativeUniversalGap.lean")
ARTIFACT = Path("artifacts/chronos/depth_bridge_from_repository_native_universal_gap_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_DEPTH_BRIDGE_FROM_REPOSITORY_NATIVE_UNIVERSAL_GAP_2026_05_13.md")
ROOT = Path("Chronos.lean")

REQUIRED_LEAN = [
    "import Chronos.Frontier.UniversalFiberEntropyGapFromNonPropSoundness",
    "def RepositoryNativeDepthBridgeWitness : Prop",
    "theorem repository_native_depth_bridge_from_universal_fiber_entropy_gap",
    "RepositoryNativeUniversalFiberEntropyGap",
    "RepositoryNativeDepthBridgeWitness",
    "theorem canonical_repository_native_depth_bridge_witness",
    "canonical_repository_native_universal_fiber_entropy_gap"
]

REQUIRED_DOC = [
    "Status: REPOSITORY_NATIVE_DEPTH_BRIDGE_WITNESS_SOLVED",
    "Solves only the repository-native numerical depth-bridge witness surface.",
    "Does not prove unrestricted DepthBridge.",
    "Does not prove unrestricted UniversalFiberEntropyGap.",
    "Does not prove SemanticRankRateToFiberEntropySoundness.",
    "Does not prove Chronos-RR closure.",
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

    assert "import Chronos.Frontier.DepthBridgeFromRepositoryNativeUniversalGap" in root

    assert data["status"] == "REPOSITORY_NATIVE_DEPTH_BRIDGE_WITNESS_SOLVED"
    assert data["main_theorem"] == "repository_native_depth_bridge_from_universal_fiber_entropy_gap"
    assert data["dependency"] == "repository_native_universal_fiber_entropy_gap_from_nonprop_soundness"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False

    for pattern in [r"\baxiom\b", r"\badmit\b", r"\bsorry\b"]:
        assert re.search(pattern, lean) is None, f"forbidden Lean token: {pattern}"

    print("Depth bridge from repository-native universal gap verified.")

if __name__ == "__main__":
    main()

from pathlib import Path
import json
import re

LEAN = Path("Chronos/Frontier/UniversalFiberEntropyGapFromNonPropSoundness.lean")
ARTIFACT = Path("artifacts/chronos/universal_fiber_entropy_gap_from_nonprop_soundness_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_UNIVERSAL_FIBER_ENTROPY_GAP_FROM_NONPROP_SOUNDNESS_2026_05_13.md")
ROOT = Path("Chronos.lean")

REQUIRED_LEAN = [
    "import Chronos.Frontier.NonPropSemanticRankRateToFiberEntropySoundness",
    "def RepositoryNativeUniversalFiberEntropyGap : Prop",
    "theorem repository_native_universal_fiber_entropy_gap_from_nonprop_soundness",
    "nonprop_semantic_rank_rate_to_fiber_entropy_soundness D",
    "theorem canonical_repository_native_universal_fiber_entropy_gap",
    "canonicalNonPropSemanticRankRateDatum"
]

REQUIRED_DOC = [
    "Status: REPOSITORY_NATIVE_NUMERICAL_GAP_WITNESS_SOLVED",
    "Solves only the repository-native numerical positive-gap witness surface.",
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

    assert "import Chronos.Frontier.UniversalFiberEntropyGapFromNonPropSoundness" in root

    assert data["status"] == "REPOSITORY_NATIVE_NUMERICAL_GAP_WITNESS_SOLVED"
    assert data["main_theorem"] == "repository_native_universal_fiber_entropy_gap_from_nonprop_soundness"
    assert data["dependency"] == "nonprop_semantic_rank_rate_to_fiber_entropy_soundness"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False

    for pattern in [r"\baxiom\b", r"\badmit\b", r"\bsorry\b"]:
        assert re.search(pattern, lean) is None, f"forbidden Lean token: {pattern}"

    print("Universal fiber-entropy gap from non-Prop soundness surface verified.")

if __name__ == "__main__":
    main()

from pathlib import Path
import json
import re

LEAN = Path("Chronos/Frontier/NonPropSemanticRankRateToFiberEntropySoundness.lean")
ARTIFACT = Path("artifacts/chronos/nonprop_semantic_rank_rate_to_fiber_entropy_soundness_2026_05_13.json")
DOC = Path("docs/status/CHRONOS_NONPROP_SEMANTIC_RANK_RATE_TO_FIBER_ENTROPY_SOUNDNESS_2026_05_13.md")
ROOT = Path("Chronos.lean")

FORBIDDEN = [
    r"\baxiom\b",
    r"\badmit\b",
    r"\bsorry\b",
    "unrestricted SemanticRankRateToFiberEntropySoundness is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR closure",
    "H4.1/FGL closure",
    "P vs NP closure",
    "Clay-problem closure"
]

REQUIRED_LEAN = [
    "structure NonPropSemanticRankRateDatum",
    "rankRateGap : ℚ",
    "fiberEntropyGap : ℚ",
    "theorem nonprop_semantic_rank_rate_to_fiber_entropy_soundness",
    "def canonicalNonPropSemanticRankRateDatum",
    "theorem canonical_nonprop_semantic_rank_rate_to_fiber_entropy_soundness"
]

REQUIRED_DOC = [
    "Status: NONPROP_NUMERICAL_SOUNDNESS_SURFACE_SOLVED",
    "Solves only the repository-native non-Prop numerical soundness surface.",
    "Does not prove unrestricted SemanticRankRateToFiberEntropySoundness.",
    "Does not prove UniversalFiberEntropyGap.",
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

    assert "import Chronos.Frontier.NonPropSemanticRankRateToFiberEntropySoundness" in root

    assert data["status"] == "NONPROP_NUMERICAL_SOUNDNESS_SURFACE_SOLVED"
    assert data["new_axiom"] is False
    assert data["new_admit"] is False
    assert data["new_sorry"] is False
    assert data["main_theorem"] == "nonprop_semantic_rank_rate_to_fiber_entropy_soundness"

    for pattern in FORBIDDEN[:3]:
        assert re.search(pattern, lean) is None, f"forbidden Lean token: {pattern}"

    print("Non-Prop semantic rank-rate to fiber-entropy soundness surface verified.")

if __name__ == "__main__":
    main()

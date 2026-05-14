#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/public/VASQUEZ_FRONTIER_AI_TEST_INVITATION_2026_05_14.md"
ARTIFACT = ROOT / "artifacts/evals/ai_frontier_test_invitation_results_2026_05_14.json"

DOC_REQUIRED = [
    "PUBLIC_EVALUATION_INVITATION_ONLY",
    "AI systems are welcome",
    "Unrestricted GraphSemanticCycleOverlapRankDominatedByColapRank is false.",
    "colapRank = 0",
    "cycleOverlapRank = 1",
    "cycleOverlap_le_colap : cycleOverlapRank <= colapRank",
    "OPEN_PROBLEM_REQUIRED / NEGATIVE_UNRESTRICTED_RESULT",
    "For every admissible graph-semantic input X, cycleOverlapRank X <= colapRank X.",
    "DeepAI",
    "Claude",
    "Gemini",
    "No P vs NP closure.",
    "No Clay-problem closure.",
    "No Chronos-RR closure.",
    "No H4.1/FGL closure.",
    "No UniversalFiberEntropyGap proof.",
    "No SemanticRankRateToFiberEntropySoundness proof.",
    "No unconditional graph-theoretic cycle-overlap-rank bound.",
    "No rigidity closure.",
]

FORBIDDEN = [
    "P vs NP is solved",
    "Clay problem is solved",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "UniversalFiberEntropyGap is proved",
    "SemanticRankRateToFiberEntropySoundness is proved",
    "rigidity closure is proved",
]

def main() -> int:
    doc = DOC.read_text()
    artifact_text = ARTIFACT.read_text()
    artifact = json.loads(artifact_text)

    for phrase in DOC_REQUIRED:
        assert phrase in doc, phrase

    for phrase in FORBIDDEN:
        assert phrase not in doc, phrase
        assert phrase not in artifact_text, phrase

    assert artifact["status"] == "PUBLIC_EVALUATION_INVITATION_ONLY"
    assert artifact["gold_classification"] == "OPEN_PROBLEM_REQUIRED / NEGATIVE_UNRESTRICTED_RESULT"
    assert artifact["gold_weakest_sufficient_missing_lemma"] == (
        "For every admissible graph-semantic input X, cycleOverlapRank X <= colapRank X."
    )

    scores = {entry["system"]: entry["score"] for entry in artifact["results"]}
    assert scores == {"DeepAI": 4, "Claude": 5, "Gemini": 4}

    print("AI frontier test invitation verified: PUBLIC_EVALUATION_INVITATION_ONLY")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

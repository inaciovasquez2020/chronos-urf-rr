from pathlib import Path
import json

doc = Path("docs/status/CHRONOS_SEMANTIC_RANK_RATE_TO_FIBER_ENTROPY_SOUNDNESS_2026_05_15.md").read_text()
artifact = json.loads(Path("artifacts/chronos/semantic_rank_rate_to_fiber_entropy_soundness_2026_05_15.json").read_text())

required = [
    "FRONTIER_OPEN / WEAKEST_SUFFICIENT_LEMMA_ISOLATED",
    "SemanticRankDefectControlsEntropyDefectOn",
    "Does not prove unrestricted Chronos-RR.",
    "Does not prove H4.1/FGL.",
    "Does not prove P vs NP.",
    "Does not prove any Clay problem."
]

for phrase in required:
    assert phrase in doc, phrase

assert artifact["status"] == "FRONTIER_OPEN / WEAKEST_SUFFICIENT_LEMMA_ISOLATED"
assert artifact["weakest_missing_lemma"] == "SemanticRankDefectControlsEntropyDefectOn"
assert artifact["allowed_closure"] == "conditional_bridge_only"

print("Semantic rank-rate to fiber entropy soundness frontier verified.")

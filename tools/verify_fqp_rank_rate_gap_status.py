from pathlib import Path
import json

doc = Path("docs/status/CHRONOS_FQP_RANK_RATE_GAP_STATUS_2026_05_11.md")
artifact = Path("artifacts/chronos/fqp_rank_rate_gap_status_2026_05_11.json")

text = doc.read_text()
data = json.loads(artifact.read_text())

required_doc_tokens = [
    "FRONTIER_OPEN / WEAKEST_MISSING_THEOREM_ONLY",
    "FQP reduces UniversalFiberEntropyGap to theorem-level RankRateGap.",
    "RankRateGap remains unproved.",
    "No theorem-level UniversalFiberEntropyGap proof is claimed.",
    "No unrestricted Chronos-RR closure is claimed.",
    "No H4.1/FGL theorem-level closure is claimed.",
    "No P vs NP result is claimed.",
    "No Clay-problem result is claimed.",
]

for token in required_doc_tokens:
    assert token in text, token

assert data["status"] == "FRONTIER_OPEN / WEAKEST_MISSING_THEOREM_ONLY"
assert data["weakest_missing_object"] == "RankRateGap"
assert data["reduction"] == "FQP reduces UniversalFiberEntropyGap to theorem-level RankRateGap."

for token in [
    "RankRateGap remains unproved",
    "No theorem-level UniversalFiberEntropyGap proof is claimed",
    "No unrestricted Chronos-RR closure is claimed",
    "No H4.1/FGL theorem-level closure is claimed",
    "No P vs NP result is claimed",
    "No Clay-problem result is claimed",
]:
    assert token in data["boundary"], token

for forbidden in [
    "RankRateGap is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is solved",
    "Clay problem is solved",
]:
    assert forbidden not in text
    assert forbidden not in artifact.read_text()

print("FQP RankRateGap status verified.")

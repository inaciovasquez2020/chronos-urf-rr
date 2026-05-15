from pathlib import Path
import json

status_path = Path("docs/status/DECISIVE_RESULT_LOCK_2026_05_15.md")
artifact_path = Path("artifacts/chronos/decisive_result_lock_2026_05_15.json")

assert status_path.exists(), status_path
assert artifact_path.exists(), artifact_path

status = status_path.read_text()
artifact_text = artifact_path.read_text()
artifact = json.loads(artifact_text)

assert artifact["status"] == "DECISIVE_TARGET_LOCKED"
assert artifact["chosen_target"] == "FiberMassBalance from CountingFiberSeparation"

required_status_phrases = [
    "No new frontier surface is admissible unless it directly serves this target.",
    "FiberMassBalance from CountingFiberSeparation",
    "This lock does not prove:",
    "UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status_phrases:
    assert phrase in status, phrase

required_nonclaims = {
    "FiberMassBalance",
    "UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

assert required_nonclaims.issubset(set(artifact["does_not_prove"]))

forbidden = [
    "FiberMassBalance is proved",
    "UniversalFiberEntropyGap is proved",
    "Chronos-RR is proved",
    "H4.1/FGL is proved",
    "P vs NP is solved",
    "Clay problem is solved",
]

combined = status + "\n" + artifact_text

for token in forbidden:
    assert token.lower() not in combined.lower(), token

print("Decisive result lock verified.")

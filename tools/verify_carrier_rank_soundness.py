#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

lean_path = ROOT / "lean/Chronos/Frontier/CarrierRankSoundness.lean"
doc_path = ROOT / "docs/status/CARRIER_RANK_SOUNDNESS_2026_05_17.md"
artifact_path = ROOT / "artifacts/chronos/carrier_rank_soundness_2026_05_17.json"
chronos_path = ROOT / "lean/Chronos.lean"

lean = lean_path.read_text()
doc = doc_path.read_text()
artifact = json.loads(artifact_path.read_text())
chronos = chronos_path.read_text()

required = [
    "def CarrierRankSoundness",
    "theorem restrictedRankRateBridge",
    "theorem restrictedRankRateBridge_fromLowerBound",
    "RESTRICTED_POSITIVE_BRIDGE",
    "Does not prove unrestricted RankRateBridgeLaw",
    "Does not prove RateThickFiberCoercivity",
    "Does not prove unrestricted UniversalFiberEntropyGap",
]

combined = "\n".join([lean, doc, json.dumps(artifact)])

for token in required:
    assert token in combined, token

for token in ["sorry", "admit", "axiom "]:
    assert token not in lean, token

assert artifact["status"] == "RESTRICTED_POSITIVE_BRIDGE"
assert "import Chronos.Frontier.CarrierRankSoundness" in chronos
assert "import Chronos.Frontier.RateThickFrontierCounterexamples" not in chronos

for forbidden in [
    "proves unrestricted RankRateBridgeLaw",
    "proves RateThickFiberCoercivity",
    "proves unrestricted UniversalFiberEntropyGap",
    "proves P vs NP",
    "solves P vs NP",
    "solves a Clay problem",
]:
    assert forbidden.lower() not in combined.lower(), forbidden

print("CarrierRankSoundness verified.")

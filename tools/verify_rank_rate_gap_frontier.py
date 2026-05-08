#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/rank_rate_gap_frontier.json"
DOC = ROOT / "docs/status/CHRONOS_RANK_RATE_GAP_FRONTIER_2026_05_08.md"

data = json.loads(ART.read_text())
doc = DOC.read_text()

assert data["name"] == "RankRateGap"
assert data["status"] == "FRONTIER_OPEN"
assert data["weakest_sufficient_for"] == "CountingFiberSeparation"

required = [
    "Status: FRONTIER_OPEN",
    "Weakest sufficient object for CountingFiberSeparation",
    "\\operatorname{rank}(C_n)\\ge rn",
    "\\operatorname{rank}(F_n)\\le sn",
    "CountingFiberSeparation follows",
    "RankRateGap",
    "CountingFiberSeparation",
    "FiberMassBalance",
    "UniversalFiberEntropyGap",
    "This file does not prove RankRateGap.",
    "This file does not prove CountingFiberSeparation.",
    "This file does not prove FiberMassBalance.",
    "This file does not prove UniversalFiberEntropyGap.",
    "This file does not assert Depth Bridge proof.",
    "This file does not assert Chronos-RR closure.",
    "This file does not assert H4.1/FGL closure.",
    "This file does not assert P vs NP closure."
]

for phrase in required:
    assert phrase in doc, phrase

for forbidden in [
    "P vs NP is solved",
    "Chronos-RR is closed",
    "Depth Bridge proof is complete",
    "UniversalFiberEntropyGap is proved",
    "FiberMassBalance is proved",
    "CountingFiberSeparation is proved",
    "RankRateGap is proved"
]:
    assert forbidden not in doc
    assert forbidden not in json.dumps(data)

print("RankRateGap frontier verified: FRONTIER_OPEN")

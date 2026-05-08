#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/universal_fiber_entropy_gap_frontier.json"
DOC = ROOT / "docs/status/CHRONOS_UNIVERSAL_FIBER_ENTROPY_GAP_FRONTIER_2026_05_08.md"

data = json.loads(ART.read_text())
doc = DOC.read_text()

assert data["name"] == "UniversalFiberEntropyGap"
assert data["status"] == "FRONTIER_OPEN"
assert data["weakest_sufficient_object"] is True

required_doc_phrases = [
    "Status: FRONTIER_OPEN",
    "This file does not prove UniversalFiberEntropyGap.",
    "This file does not assert Depth Bridge proof.",
    "This file does not assert Chronos-RR closure.",
    "This file does not assert H4.1/FGL closure.",
    "This file does not assert P vs NP closure.",
]

for phrase in required_doc_phrases:
    assert phrase in doc, phrase

for forbidden in [
    "P vs NP is solved",
    "Chronos-RR is closed",
    "Depth Bridge proof is complete",
    "H4.1/FGL closure is proved",
]:
    assert forbidden not in doc
    assert forbidden not in json.dumps(data)

print("UniversalFiberEntropyGap frontier verified: FRONTIER_OPEN")

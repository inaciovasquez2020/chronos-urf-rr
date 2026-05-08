#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/fiber_mass_balance_frontier.json"
DOC = ROOT / "docs/status/CHRONOS_FIBER_MASS_BALANCE_FRONTIER_2026_05_08.md"

data = json.loads(ART.read_text())
doc = DOC.read_text()

assert data["name"] == "FiberMassBalance"
assert data["status"] == "FRONTIER_OPEN"
assert data["weakest_sufficient_for"] == "UniversalFiberEntropyGap"

required = [
    "Status: FRONTIER_OPEN",
    "Weakest sufficient object for UniversalFiberEntropyGap",
    "H(C_n\\mid F_n)=H(C_n)-I(C_n;F_n)",
    "UniversalFiberEntropyGap follows",
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
    "UniversalFiberEntropyGap is proved"
]:
    assert forbidden not in doc
    assert forbidden not in json.dumps(data)

print("FiberMassBalance frontier verified: FRONTIER_OPEN")

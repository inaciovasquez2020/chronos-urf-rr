#!/usr/bin/env python3
from pathlib import Path

p = Path("docs/status/THEOREM_LEVEL_FRONTIERS_2026_04_27.md")
text = p.read_text(encoding="utf-8")

required = [
    "Status: Conditional.",
    "General FGL row-separation",
    "R1 Long-Chord Exclusion",
    "R2 Diameter-Separation Filling Obstruction",
    "R3 Uniform Local-Type Capacity",
    "General H4.1.",
    "Unconditional Chronos/URF theorem-level closure.",
    "The following are not proved:",
]

for item in required:
    assert item in text, f"missing required frontier marker: {item}"

for forbidden in [
    "General H4.1: Proved",
    "General FGL row-separation: Proved",
    "R1 Long-Chord Exclusion: Proved",
    "R2 Diameter-Separation Filling Obstruction: Proved",
    "R3 Uniform Local-Type Capacity: Proved",
    "Unconditional Chronos/URF theorem-level closure: Proved",
]:
    assert forbidden not in text, f"forbidden overclaim: {forbidden}"

print("PASS: theorem-level frontiers remain explicitly conditional")

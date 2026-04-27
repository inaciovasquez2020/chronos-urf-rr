#!/usr/bin/env python3
from pathlib import Path

status = Path("docs/status/BALL_VOLUME_ACYCLICITY_STATUS_2026_04_27.md")
status_text = status.read_text(encoding="utf-8")

targets = [
    Path("lean/Oblivion/CycloneSignedLift.lean"),
    Path("lean/Oblivion/Cycle.lean"),
]

uses = []

for p in targets:
    if not p.exists():
        continue
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        if "ball_cycle_length_bound" in line or "cycle_length_le_twoR_of_subgraph_ball" in line:
            uses.append(f"{p}:{i}:{line.strip()}")

if uses:
    assert "`girth_gt_twoR_implies_ball_acyclic_quarantined` is Conditional/Quarantined" in status_text
    assert "depends on the quarantined `2R` cycle-length bound" in status_text
    assert "bounded-volume girth-radius acyclicity theorem" in status_text

print("PASS: dependent 2R cycle-length usage is quarantined")
for u in uses:
    print(u)

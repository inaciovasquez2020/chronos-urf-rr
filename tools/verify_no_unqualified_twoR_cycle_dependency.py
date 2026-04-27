#!/usr/bin/env python3
from pathlib import Path
import re

LEAN_FILES = [
    Path("lean/Oblivion/Cycle.lean"),
    Path("lean/Oblivion/CycloneSignedLift.lean"),
]

FORBIDDEN = [
    r"\bcycle_length_le_twoR_of_subgraph_ball\b",
    r"\bball_cycle_length_bound\b",
    r"\bgirth_gt_twoR_implies_ball_acyclic\b",
]

REQUIRED = [
    "cycle_length_le_twoR_of_subgraph_ball_quarantined",
    "ball_cycle_length_bound_quarantined",
    "girth_gt_twoR_implies_ball_acyclic_quarantined",
]

all_text = ""

for path in LEAN_FILES:
    text = path.read_text(encoding="utf-8")
    all_text += "\n" + text
    for pattern in FORBIDDEN:
        if re.search(pattern, text):
            raise SystemExit(f"unqualified quarantined dependency remains in {path}: {pattern}")

missing = [name for name in REQUIRED if name not in all_text]
if missing:
    raise SystemExit("missing quarantined identifiers: " + ", ".join(missing))

status = Path("docs/status/BALL_VOLUME_ACYCLICITY_STATUS_2026_04_27.md").read_text(encoding="utf-8")
assert "Conditional/Quarantined" in status
assert "bounded-volume girth-radius acyclicity theorem" in status

print("PASS: unqualified 2R cycle-length dependency removed")

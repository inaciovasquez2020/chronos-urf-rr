#!/usr/bin/env python3
from pathlib import Path

cycle = Path("lean/Oblivion/Cycle.lean")
status = Path("docs/status/BALL_VOLUME_ACYCLICITY_STATUS_2026_04_27.md")

cycle_text = cycle.read_text(encoding="utf-8")
status_text = status.read_text(encoding="utf-8")

bad = "axiom cycle_length_le_twoR_of_subgraph_ball"
if bad in cycle_text:
    assert "cycle_length_le_twoR_of_subgraph_ball_quarantined` is false for general graphs" in status_text
    assert "must remain quarantined" in status_text
    assert "must not be used as a theorem-level dependency" in status_text
else:
    assert "Replacement theorem:" in status_text
    assert "girth(G) > |B_G(v,R)|" in status_text

print("PASS: ball-cycle-length axiom is quarantined by status lock")

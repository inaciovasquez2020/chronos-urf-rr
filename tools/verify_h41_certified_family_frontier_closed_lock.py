from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/h41_certified_family_frontier_closed_2026_06_11.json"
DOC = ROOT / "docs/status/H41_CERTIFIED_FAMILY_FRONTIER_CLOSED_2026_06_11.md"

EXPECTED_ID = "H41_CERTIFIED_FAMILY_FRONTIER_CLOSED_2026_06_11"


def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["id"] == EXPECTED_ID
    assert data["main_commit"] == "489312d8"
    assert data["merged_pr"] == 693
    assert data["status"] == "closed_repository_surface"
    assert data["validation"]["axiom_count"] == 0
    assert data["validation"]["admit_count"] == 0
    assert data["validation"]["sorry_count"] == 0
    assert "does not claim an external mathematical proof of H4.1" in doc
    assert "structurally vacuous through empty admissible placements" in doc

    print("H41_CERTIFIED_FAMILY_FRONTIER_CLOSED_LOCK_OK")


if __name__ == "__main__":
    main()

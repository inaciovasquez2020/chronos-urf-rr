#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

INDEX = Path("artifacts/chronos/frontier-status.json")
LOCK = Path("artifacts/chronos/r1_width_threshold_alias_local_placeholder_closure_lock_2026_06_20.json")
DOC = Path("docs/status/R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_LOCK.md")
VERIFIER = Path("tools/verify_r1_width_threshold_alias_local_placeholder_closure_lock.py")

def main() -> None:
    data = json.loads(INDEX.read_text())

    assert isinstance(data, dict)
    assert isinstance(data.get("surfaces"), list)

    matches = [
        item for item in data["surfaces"]
        if isinstance(item, dict)
        and item.get("id") == "R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_LOCK"
    ]
    assert len(matches) == 1

    entry = matches[0]
    assert entry["status"] == "LOCAL_PLACEHOLDER_ALIAS_PRECONDITIONS_CLOSED_ONLY"
    assert entry["artifact"] == str(LOCK)
    assert entry["doc"] == str(DOC)
    assert entry["verifier"] == str(VERIFIER)
    assert entry["boundary"] == "BOUNDARY := ¬ unrestricted_Chronos_RR"

    assert LOCK.is_file()
    assert DOC.is_file()
    assert VERIFIER.is_file()

    print("R1_WIDTH_THRESHOLD_ALIAS_FRONTIER_STATUS_INDEX_BRIDGE_OK")

if __name__ == "__main__":
    main()

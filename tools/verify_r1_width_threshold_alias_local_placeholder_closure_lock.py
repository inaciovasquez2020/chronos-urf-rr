#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

LOCK = Path("artifacts/chronos/r1_width_threshold_alias_local_placeholder_closure_lock_2026_06_20.json")
ALIAS = Path("artifacts/chronos/r1_width_threshold_alias_surface_2026_06_20.json")

def main() -> None:
    lock = json.loads(LOCK.read_text())
    alias = json.loads(ALIAS.read_text())

    assert lock["artifact"] == "R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_LOCK"
    assert lock["status"] == "LOCAL_PLACEHOLDER_ALIAS_PRECONDITIONS_CLOSED_ONLY"
    assert lock["base_commit"] == "308a307f9e1d5cea67c2cf0f4a6d1fc2a2cbc0df"

    assert alias["artifact"] == "R1_WIDTH_THRESHOLD_ALIAS_SURFACE"
    assert lock["target_alias_surface"]["artifact_file"] == str(ALIAS)
    assert lock["target_alias_surface"]["artifact"] == alias["artifact"]

    bridges = lock["closed_local_placeholder_preconditions"]
    assert len(bridges) == 3

    names = {entry["precondition"] for entry in bridges}
    assert names == {
        "domain identity",
        "obstruction measure identity",
        "same local obstruction measure bounds",
    }

    for entry in bridges:
        bridge_path = Path(entry["bridge_artifact"])
        verifier_path = Path(entry["verifier"])
        assert bridge_path.is_file(), bridge_path
        assert verifier_path.is_file(), verifier_path
        subprocess.run([sys.executable, str(verifier_path)], check=True)

    blocked = set(lock["does_not_prove"])
    assert "native cross(gamma,L) semantics" in blocked
    assert "native SkeletonDistance_I(endpoints(c)) semantics" in blocked
    assert "native endpoint extraction semantics" in blocked
    assert "native obstruction measure semantics" in blocked
    assert "native w(P,L) semantics" in blocked
    assert "native LongChordThreshold(I) semantics" in blocked
    assert "unconditional w(P,L) = LongChordThreshold(I)" in blocked
    assert "native R1/R2/R3" in blocked
    assert "unrestricted Chronos-RR" in blocked
    assert lock["boundary"] == "BOUNDARY := \u00ac unrestricted_Chronos_RR"

    print("R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_LOCK_OK")

if __name__ == "__main__":
    main()

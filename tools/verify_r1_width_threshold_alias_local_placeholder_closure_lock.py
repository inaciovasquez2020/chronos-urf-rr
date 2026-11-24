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
    assert lock["status"] == "LOCAL_PLACEHOLDER_ALIAS_PRECONDITIONS_PARTIAL_ONLY"
    assert lock["base_commit"] == "308a307f9e1d5cea67c2cf0f4a6d1fc2a2cbc0df"

    assert alias["artifact"] == "R1_WIDTH_THRESHOLD_ALIAS_SURFACE"
    assert lock["target_alias_surface"]["artifact_file"] == str(ALIAS)
    assert lock["target_alias_surface"]["artifact"] == alias["artifact"]

    bridges = lock["closed_local_placeholder_preconditions"]
    assert len(bridges) == 2

    names = {entry["precondition"] for entry in bridges}
    assert names == {
        "obstruction measure identity",
        "same local obstruction measure bounds",
    }

    for entry in bridges:
        bridge_path = Path(entry["bridge_artifact"])
        verifier_path = Path(entry["verifier"])
        assert bridge_path.is_file(), bridge_path
        assert verifier_path.is_file(), verifier_path
        subprocess.run([sys.executable, str(verifier_path)], check=True)


    assert lock["lock_claim"].endswith("domain identity remains OPEN.")
    opened = lock["open_preconditions"]
    assert len(opened) == 1
    missing = opened[0]
    assert missing["precondition"] == "domain identity"
    assert missing["bridge_artifact"] == (
        "artifacts/chronos/"
        "r1_domain_identity_to_width_threshold_alias_bridge_2026_06_20.json"
    )
    assert missing["verifier"] == (
        "tools/verify_r1_domain_identity_to_width_threshold_alias_bridge.py"
    )
    assert "native domain identity is OPEN" in missing["reason"]

    domain_bridge = json.loads(Path(missing["bridge_artifact"]).read_text())
    claim = domain_bridge["bridge_claim"]
    assert claim["discharged_precondition"] == (
        "POINTWISE_PLACEHOLDER_EQUALITY_ON_ADJACENT_CHORD_SUBTYPE"
    )
    assert claim["remaining_precondition"] == alias["weakest_missing_assumption"]
    assert not any(x["precondition"] == "domain identity" for x in bridges)
    subprocess.run(
        [sys.executable, missing["verifier"]], check=True
    )

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
    assert "unrestricted marked-boundary/candidate-chord domain identity" in blocked
    assert lock["boundary"] == "BOUNDARY := \u00ac unrestricted_Chronos_RR"

    print("R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_LOCK_OK")

if __name__ == "__main__":
    main()

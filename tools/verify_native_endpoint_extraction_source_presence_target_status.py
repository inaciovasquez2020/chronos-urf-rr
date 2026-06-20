#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ARTIFACT = Path(
    "artifacts/chronos/native_endpoint_extraction_source_presence_target_status_2026_06_20.json"
)

def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "NATIVE_ENDPOINT_EXTRACTION_SOURCE_PRESENCE_TARGET_STATUS"
    assert data["status"] == "SOURCE_PRESENCE_TARGET_ONLY"
    assert data["base_commit"] == "6e905f30317c94f7fa9bab5c7e4a1ad8d82877a9"
    assert data["target"] == "native endpoint extraction semantics"

    candidates = data["candidate_source_files"]
    assert isinstance(candidates, list)
    assert candidates
    assert "lean/Chronos/Frontier/R1cNativeEndpointConfigurationWitnessTarget.lean" in candidates

    for candidate in candidates:
        assert Path(candidate).is_file(), candidate

    blocked = set(data["does_not_prove"])
    assert "native endpoint extraction semantics" in blocked
    assert "native SkeletonDistance_I(endpoints(c)) semantics" in blocked
    assert "native cross(gamma,L) semantics" in blocked
    assert "native obstruction measure semantics" in blocked
    assert "native R1/R2/R3" in blocked
    assert "unrestricted Chronos-RR" in blocked

    assert data["boundary"] == "BOUNDARY := ¬ native_endpoint_extraction_semantics"

    print("NATIVE_ENDPOINT_EXTRACTION_SOURCE_PRESENCE_TARGET_STATUS_OK")

if __name__ == "__main__":
    main()

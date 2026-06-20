#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ARTIFACT = Path("artifacts/chronos/native_endpoint_extraction_selected_semantic_source_target_2026_06_20.json")
SOURCE_PRESENCE = Path("artifacts/chronos/native_endpoint_extraction_source_presence_target_status_2026_06_20.json")
SELECTED = Path("lean/Chronos/Frontier/R1cNativeEndpointConfigurationWitnessTarget.lean")

def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "NATIVE_ENDPOINT_EXTRACTION_SELECTED_SEMANTIC_SOURCE_TARGET"
    assert data["status"] == "TARGET_SELECTION_ONLY"
    assert data["base_commit"] == "7fdf9f21f29ca1dd0a4d51b5f5997cecb63bf48d"

    assert data["source_presence_artifact"] == str(SOURCE_PRESENCE)
    assert data["selected_semantic_source"] == str(SELECTED)
    assert data["target"] == "bounded native endpoint extraction semantics source inspection"

    assert SOURCE_PRESENCE.is_file()
    assert SELECTED.is_file()
    assert SELECTED.suffix == ".lean"

    source_presence = json.loads(SOURCE_PRESENCE.read_text())
    assert str(SELECTED) in source_presence["candidate_source_files"]

    selected_hash = hashlib.sha256(SELECTED.read_bytes()).hexdigest()
    assert data["selected_source_sha256"] == selected_hash

    assert data["does_not_modify"] == [str(SELECTED)]

    blocked = set(data["does_not_prove"])
    assert "native endpoint extraction semantics" in blocked
    assert "native SkeletonDistance_I(endpoints(c)) semantics" in blocked
    assert "native cross(gamma,L) semantics" in blocked
    assert "native obstruction measure semantics" in blocked
    assert "native R1/R2/R3" in blocked
    assert "unrestricted Chronos-RR" in blocked

    assert data["boundary"] == "BOUNDARY := ¬ native_endpoint_extraction_semantics"

    print("NATIVE_ENDPOINT_EXTRACTION_SELECTED_SEMANTIC_SOURCE_TARGET_OK")

if __name__ == "__main__":
    main()

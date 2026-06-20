#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

BRIDGE = Path("artifacts/chronos/r1_obstruction_measure_bound_to_width_threshold_alias_bridge_2026_06_20.json")
ALIAS = Path("artifacts/chronos/r1_width_threshold_alias_surface_2026_06_20.json")
LEAN = Path("lean/Chronos/Frontier/R1ObstructionMeasureBoundSurface.lean")

def main() -> None:
    bridge = json.loads(BRIDGE.read_text())
    alias = json.loads(ALIAS.read_text())
    lean = LEAN.read_text()

    assert bridge["artifact"] == "R1_OBSTRUCTION_MEASURE_BOUND_TO_WIDTH_THRESHOLD_ALIAS_BRIDGE"
    assert bridge["status"] == "LOCAL_BRIDGE_SURFACE_ONLY"
    assert alias["artifact"] == "R1_WIDTH_THRESHOLD_ALIAS_SURFACE"

    required = "w(P,L) and LongChordThreshold(I) are both bounds for that same obstruction measure"
    assert required in alias["conditional_alias"]["allowed_only_if"]

    source = bridge["source_surface"]
    assert source["lean_file"] == str(LEAN)
    assert source["external_bound"] == "WidthBound"
    assert source["native_bound"] == "LongChordThreshold"
    assert source["local_measure"] == "LocalObstructionMeasure"
    assert source["bound_relation"] == "BoundsObstructionMeasure"
    assert source["same_measure_bounds_theorem"] == (
        "widthBound_longChordThreshold_same_local_obstruction_measure_bounds"
    )

    assert "def LocalObstructionMeasure" in lean
    assert "def WidthBound" in lean
    assert "def LongChordThreshold" in lean
    assert "def BoundsObstructionMeasure" in lean
    assert "theorem widthBound_longChordThreshold_same_local_obstruction_measure_bounds" in lean
    assert "BoundsObstructionMeasure (WidthBound I c) (LocalObstructionMeasure I c)" in lean
    assert "BoundsObstructionMeasure (LongChordThreshold I) (LocalObstructionMeasure I c)" in lean
    assert "Nat.zero_le" in lean

    target = bridge["target_surface"]
    assert target["artifact_file"] == str(ALIAS)
    assert target["artifact"] == alias["artifact"]
    assert target["required_precondition"] == required

    claim = bridge["bridge_claim"]
    assert claim["discharged_precondition"] == (
        "SAME_OBSTRUCTION_MEASURE_BOUNDS(w(P,L), LongChordThreshold(I))"
    )
    assert claim["discharge_method"] == "local Lean placeholder bound surface"

    blocked = set(bridge["does_not_prove"])
    assert "native w(P,L) semantics" in blocked
    assert "native LongChordThreshold(I) semantics" in blocked
    assert "native obstruction measure semantics" in blocked
    assert "native cross(gamma,L) semantics" in blocked
    assert "native SkeletonDistance_I(endpoints(c)) semantics" in blocked
    assert "native endpoint extraction semantics" in blocked
    assert "w(P,L) equals LongChordThreshold(I) unconditionally" in blocked
    assert "native R1/R2/R3 instance" in blocked
    assert "unrestricted Chronos-RR" in blocked
    assert bridge["boundary"] == "BOUNDARY := \u00ac unrestricted_Chronos_RR"

    print("R1_OBSTRUCTION_MEASURE_BOUND_TO_WIDTH_THRESHOLD_ALIAS_BRIDGE_OK")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

BRIDGE = Path("artifacts/chronos/r1_obstruction_measure_identity_to_width_threshold_alias_bridge_2026_06_20.json")
ALIAS = Path("artifacts/chronos/r1_width_threshold_alias_surface_2026_06_20.json")
LEAN = Path("lean/Chronos/Frontier/R1ObstructionMeasureIdentitySurface.lean")


def main() -> None:
    bridge = json.loads(BRIDGE.read_text())
    alias = json.loads(ALIAS.read_text())
    lean = LEAN.read_text()

    assert bridge["artifact"] == "R1_OBSTRUCTION_MEASURE_IDENTITY_TO_WIDTH_THRESHOLD_ALIAS_BRIDGE"
    assert bridge["status"] == "LOCAL_BRIDGE_SURFACE_ONLY"

    assert alias["artifact"] == "R1_WIDTH_THRESHOLD_ALIAS_SURFACE"
    required = (
        "cross(gamma,L) and SkeletonDistance_I(endpoints(c)) compute the identical finite obstruction measure on that domain"
    )
    assert required in alias["conditional_alias"]["allowed_only_if"]

    source = bridge["source_surface"]
    assert source["lean_file"] == str(LEAN)
    assert source["external_measure"] == "Cross"
    assert source["native_measure"] == "SkeletonDistanceEndpoints"
    assert source["identity_theorem"] == "cross_skeletonDistanceEndpoints_obstruction_measure_identity"

    assert "def Cross" in lean
    assert "def SkeletonDistanceEndpoints" in lean
    assert "theorem cross_skeletonDistanceEndpoints_obstruction_measure_identity" in lean
    assert "Cross I c = SkeletonDistanceEndpoints I c" in lean
    assert "rfl" in lean

    target = bridge["target_surface"]
    assert target["artifact_file"] == str(ALIAS)
    assert target["artifact"] == alias["artifact"]
    assert target["required_precondition"] == required

    claim = bridge["bridge_claim"]
    assert claim["discharged_precondition"] == (
        "OBSTRUCTION_MEASURE_IDENTITY(cross(gamma,L), SkeletonDistance_I(endpoints(c)))"
    )
    assert claim["discharge_method"] == "local Lean rfl identity surface"

    blocked = set(bridge["does_not_prove"])
    assert "native cross(gamma,L) semantics" in blocked
    assert "native SkeletonDistance_I(endpoints(c)) semantics" in blocked
    assert "native endpoint extraction semantics" in blocked
    assert "w(P,L) equals LongChordThreshold(I) unconditionally" in blocked
    assert "native R1/R2/R3 instance" in blocked
    assert "unrestricted Chronos-RR" in blocked

    assert bridge["boundary"] == "BOUNDARY := \u00ac unrestricted_Chronos_RR"

    print("R1_OBSTRUCTION_MEASURE_IDENTITY_TO_WIDTH_THRESHOLD_ALIAS_BRIDGE_OK")


if __name__ == "__main__":
    main()

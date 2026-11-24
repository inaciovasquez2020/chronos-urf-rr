#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

BRIDGE = Path("artifacts/chronos/r1_domain_identity_to_width_threshold_alias_bridge_2026_06_20.json")
ALIAS = Path("artifacts/chronos/r1_width_threshold_alias_surface_2026_06_20.json")
LEAN = Path("lean/Chronos/Frontier/R1DomainIdentitySurface.lean")


def main() -> None:
    bridge = json.loads(BRIDGE.read_text())
    alias = json.loads(ALIAS.read_text())
    lean = LEAN.read_text()

    assert bridge["artifact"] == "R1_DOMAIN_IDENTITY_TO_WIDTH_THRESHOLD_ALIAS_BRIDGE"
    assert bridge["status"] == "LOCAL_BRIDGE_SURFACE_ONLY"

    assert alias["artifact"] == "R1_WIDTH_THRESHOLD_ALIAS_SURFACE"
    assert alias["conditional_alias"]["alias_surface"] == "w(P,L) := LongChordThreshold(I)"
    assert alias["weakest_missing_assumption"] == (
        "DOMAIN_IDENTITY(MarkedBoundaryChord(P,M), CandidateChord(I,c))"
    )

    source = bridge["source_surface"]
    assert source["lean_file"] == str(LEAN)
    assert source["candidate_domain"] == "CandidateChord"
    assert source["marked_boundary_domain"] == "MarkedBoundaryChord"
    assert source["identity_theorem"] == "markedBoundaryChord_candidateChord_domain_identity"

    assert "def CandidateChord" in lean
    assert "def MarkedBoundaryChord" in lean
    assert "theorem markedBoundaryChord_candidateChord_domain_identity" in lean
    assert "(c : R1NativeCandidateChord G)" in lean
    assert "MarkedBoundaryChord G.Carrier (G.Carrier × G.Carrier) =" in lean
    assert "CandidateChord G c.1 := by" in lean
    assert "apply propext" in lean
    assert "simpa [CandidateChord] using c.2" in lean

    target = bridge["target_surface"]
    assert target["artifact_file"] == str(ALIAS)
    assert target["artifact"] == alias["artifact"]
    assert target["alias_surface"] == alias["conditional_alias"]["alias_surface"]

    claim = bridge["bridge_claim"]
    assert claim["discharged_precondition"] == (
        "POINTWISE_PLACEHOLDER_EQUALITY_ON_ADJACENT_CHORD_SUBTYPE"
    )
    assert claim["remaining_precondition"] == alias["weakest_missing_assumption"]
    assert claim["discharge_method"] == (
        "Lean propext using candidate-chord adjacency witness"
    )
    assert "not an unrestricted finite domain identity" in claim["bridge_result"]

    blocked = set(bridge["does_not_prove"])
    assert "full marked-boundary/candidate chord domain identity" in blocked
    assert "native CandidateChord semantics" in blocked
    assert "native MarkedBoundaryChord semantics" in blocked
    assert "cross(gamma,L) equals SkeletonDistance_I(endpoints(c))" in blocked
    assert "w(P,L) equals LongChordThreshold(I) unconditionally" in blocked
    assert "native R1/R2/R3 instance" in blocked
    assert "unrestricted Chronos-RR" in blocked

    assert bridge["boundary"] == "BOUNDARY := \u00ac unrestricted_Chronos_RR"

    print("R1_DOMAIN_IDENTITY_TO_WIDTH_THRESHOLD_ALIAS_BRIDGE_OK")


if __name__ == "__main__":
    main()

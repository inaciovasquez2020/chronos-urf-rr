#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/chronos/r1_width_threshold_alias_surface_2026_06_20.json")

def main() -> None:
    data = json.loads(ARTIFACT.read_text())

    assert data["artifact"] == "R1_WIDTH_THRESHOLD_ALIAS_SURFACE"
    assert data["status"] == "CONDITIONAL_ALIAS_SURFACE_ONLY"
    assert data["target"] == "R1LongChordWidthThresholdAlias"

    native = data["repository_native_objects"]
    assert native["candidate_chord_domain"] == "CandidateChord(I,c)"
    assert native["threshold_object"] == "LongChordThreshold(I)"
    assert native["distance_object"] == "SkeletonDistance_I(endpoints(c))"
    assert native["long_chord_predicate"] == (
        "SkeletonDistance_I(endpoints(c)) >= LongChordThreshold(I)"
    )

    external = data["external_notation"]
    assert external["width_notation"] == "w(P,L)"
    assert external["marked_boundary_chord_domain"] == "MarkedBoundaryChord(P,M)"

    conditional = data["conditional_alias"]
    assert conditional["alias_surface"] == "w(P,L) := LongChordThreshold(I)"
    assert conditional["allowed_only_if"] == [
        "MarkedBoundaryChord(P,M) and CandidateChord(I,c) quantify over the identical finite chord domain",
        "cross(gamma,L) and SkeletonDistance_I(endpoints(c)) compute the identical finite obstruction measure on that domain",
        "w(P,L) and LongChordThreshold(I) are both bounds for that same obstruction measure",
    ]

    assert data["weakest_missing_assumption"] == (
        "DOMAIN_IDENTITY(MarkedBoundaryChord(P,M), CandidateChord(I,c))"
    )

    blocked_claims = set(data["does_not_prove"])
    assert "domain identity" in blocked_claims
    assert "general LongChordExclusion" in blocked_claims
    assert "native R1/R2/R3 instance" in blocked_claims
    assert "unrestricted Chronos-RR" in blocked_claims
    assert "P vs NP" in blocked_claims
    assert "any Clay problem" in blocked_claims

    assert data["boundary"] == "BOUNDARY := \u00ac unrestricted_Chronos_RR"

    print("R1_WIDTH_THRESHOLD_ALIAS_SURFACE_OK")

if __name__ == "__main__":
    main()

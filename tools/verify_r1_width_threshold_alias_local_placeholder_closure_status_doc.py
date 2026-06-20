#!/usr/bin/env python3
from pathlib import Path

DOC = Path("docs/status/R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_LOCK.md")
LOCK = Path("artifacts/chronos/r1_width_threshold_alias_local_placeholder_closure_lock_2026_06_20.json")
LOCK_VERIFIER = Path("tools/verify_r1_width_threshold_alias_local_placeholder_closure_lock.py")

def main() -> None:
    text = DOC.read_text()

    assert LOCK.is_file()
    assert LOCK_VERIFIER.is_file()

    assert "Status: `LOCAL_PLACEHOLDER_ALIAS_PRECONDITIONS_CLOSED_ONLY`" in text
    assert str(LOCK) in text
    assert str(LOCK_VERIFIER) in text

    assert "domain identity" in text
    assert "obstruction measure identity" in text
    assert "same local obstruction measure bounds" in text
    assert "lean/Chronos/Frontier/R1ObstructionMeasureBoundSurface.lean" in text

    assert "BOUNDARY := ¬ unrestricted_Chronos_RR" in text
    assert "does not assert native `cross(gamma,L)` semantics" in text
    assert "native `SkeletonDistance_I(endpoints(c))` semantics" in text
    assert "endpoint extraction semantics" in text
    assert "unconditional `w(P,L) = LongChordThreshold(I)`" in text
    assert "native R1/R2/R3" in text
    assert "unrestricted Chronos-RR" in text

    print("R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_STATUS_DOC_OK")

if __name__ == "__main__":
    main()

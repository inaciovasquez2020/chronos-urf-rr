#!/usr/bin/env python3
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/R1ObstructionMeasureBoundSurface.lean")

def main() -> None:
    text = LEAN.read_text()
    assert "def LocalObstructionMeasure" in text
    assert "def WidthBound" in text
    assert "def LongChordThreshold" in text
    assert "def BoundsObstructionMeasure" in text
    assert "theorem widthBound_bounds_localObstructionMeasure" in text
    assert "theorem longChordThreshold_bounds_localObstructionMeasure" in text
    assert "theorem widthBound_longChordThreshold_same_local_obstruction_measure_bounds" in text
    assert "Nat.zero_le" in text
    assert "does not prove native `w(P,L)` semantics" in text
    assert "unconditional `w(P,L) = LongChordThreshold(I)`" in text
    assert "unrestricted RR" in text
    print("R1_OBSTRUCTION_MEASURE_BOUND_OK")

if __name__ == "__main__":
    main()

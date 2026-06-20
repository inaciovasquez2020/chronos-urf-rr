#!/usr/bin/env python3
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/R1ObstructionMeasureIdentitySurface.lean")


def main() -> None:
    text = LEAN.read_text()

    assert "def Cross" in text
    assert "def SkeletonDistanceEndpoints" in text
    assert "theorem cross_skeletonDistanceEndpoints_obstruction_measure_identity" in text
    assert "Cross I c = SkeletonDistanceEndpoints I c" in text
    assert "rfl" in text
    assert "does not prove native `cross(gamma,L)` semantics" in text
    assert "SkeletonDistance_I(endpoints(c))" in text

    print("R1_OBSTRUCTION_MEASURE_IDENTITY_OK")


if __name__ == "__main__":
    main()

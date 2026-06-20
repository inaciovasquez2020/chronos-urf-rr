#!/usr/bin/env python3
from pathlib import Path

DOC = Path("docs/status/NATIVE_ENDPOINT_EXTRACTION_SOURCE_PRESENCE_TARGET_STATUS_2026_06_20.md")
ARTIFACT = Path("artifacts/chronos/native_endpoint_extraction_source_presence_target_status_2026_06_20.json")
VERIFIER = Path("tools/verify_native_endpoint_extraction_source_presence_target_status.py")
SELECTED = Path("lean/Chronos/Frontier/R1cNativeEndpointConfigurationWitnessTarget.lean")

def main() -> None:
    text = DOC.read_text()

    assert ARTIFACT.is_file()
    assert VERIFIER.is_file()
    assert SELECTED.is_file()

    assert "Status: `SOURCE_PRESENCE_TARGET_ONLY`" in text
    assert str(ARTIFACT) in text
    assert str(VERIFIER) in text
    assert str(SELECTED) in text

    assert "Selected next bounded semantic source:" in text
    assert "BOUNDARY := ¬ native_endpoint_extraction_semantics" in text
    assert "does not assert native endpoint extraction semantics" in text
    assert "native `SkeletonDistance_I(endpoints(c))` semantics" in text
    assert "native `cross(gamma,L)` semantics" in text
    assert "native obstruction-measure semantics" in text
    assert "native R1/R2/R3" in text
    assert "unrestricted Chronos-RR" in text

    print("NATIVE_ENDPOINT_EXTRACTION_SOURCE_PRESENCE_STATUS_DOC_OK")

if __name__ == "__main__":
    main()

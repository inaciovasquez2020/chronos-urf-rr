#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ART = Path("artifacts/gravity/numeric_mascon_baseline_and_deficit_vector_payloads_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/NumericMASCONBaselineAndDeficitVectorPayloads.lean")
DOC = Path("docs/status/NUMERIC_MASCON_BASELINE_AND_DEFICIT_VECTOR_PAYLOADS_2026_05_29.md")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    assert ART.exists(), f"missing artifact: {ART}"
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert DOC.exists(), f"missing doc: {DOC}"

    artifact = json.loads(ART.read_text())
    assert artifact["id"] == "NUMERIC_MASCON_BASELINE_AND_DEFICIT_VECTOR_PAYLOADS_2026_05_29"
    assert artifact["status"] == "LOCAL_NUMERIC_PAYLOADS_GENERATED_NOT_COMMITTED"
    assert artifact["source_variable"] == "lwe_thickness"
    assert artifact["shape"] == [255, 360, 720]
    assert artifact["vector_length"] == 255 * 360 * 720
    assert artifact["boundary"]["no_model_comparison_execution"] is True
    assert artifact["boundary"]["no_empirical_gravity_result"] is True
    assert all(artifact["boundary"].values())

    baseline = Path(artifact["baseline_vector"])
    deficit = Path(artifact["deficit_vector"])

    if baseline.exists():
        assert sha256(baseline) == artifact["baseline_sha256"]
    if deficit.exists():
        assert sha256(deficit) == artifact["deficit_sha256"]

    print("NUMERIC_MASCON_BASELINE_AND_DEFICIT_VECTOR_PAYLOADS_OK")
    print(json.dumps({
        "status": artifact["status"],
        "source_variable": artifact["source_variable"],
        "vector_length": artifact["vector_length"],
        "baseline_vector_present": baseline.exists(),
        "deficit_vector_present": deficit.exists()
    }, indent=2))

if __name__ == "__main__":
    main()

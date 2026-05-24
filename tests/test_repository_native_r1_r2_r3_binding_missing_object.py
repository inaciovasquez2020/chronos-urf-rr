import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_repository_native_r1_r2_r3_binding_missing_object_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_repository_native_r1_r2_r3_binding_missing_object.py"],
        cwd=ROOT,
        check=True,
    )

def test_repository_native_r1_r2_r3_binding_missing_object_artifact() -> None:
    artifact = json.loads(
        (
            ROOT
            / "artifacts/chronos/repository_native_r1_r2_r3_binding_missing_object_2026_05_24.json"
        ).read_text()
    )
    assert artifact["status"] == "MISSING_OBJECT_RECORDED_NO_THEOREM_PROMOTION"
    assert artifact["missing_object"] == "RepositoryNativeR1R2R3BindingSpec"

def test_repository_native_r1_r2_r3_binding_missing_object_no_overclaim() -> None:
    combined = "\n".join(
        p.read_text()
        for p in [
            ROOT / "lean/Chronos/Frontier/RepositoryNativeR1R2R3BindingMissingObject.lean",
            ROOT / "docs/status/REPOSITORY_NATIVE_R1_R2_R3_BINDING_MISSING_OBJECT_2026_05_24.md",
            ROOT / "artifacts/chronos/repository_native_r1_r2_r3_binding_missing_object_2026_05_24.json",
        ]
    )
    for token in [
        "proved LongChordExclusion",
        "proved DiameterSeparationFillingObstruction",
        "proved UniformLocalTypeCapacity",
        "proved NON_FACTORISATION",
        "proved Chronos-RR",
        "proved H4.1/FGL",
        "P vs NP proved",
        "Clay problem solved",
    ]:
        assert token not in combined

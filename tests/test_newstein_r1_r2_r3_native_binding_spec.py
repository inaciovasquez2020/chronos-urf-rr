import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_newstein_r1_r2_r3_native_binding_spec_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_newstein_r1_r2_r3_native_binding_spec.py"],
        cwd=ROOT,
        check=True,
    )

def test_newstein_r1_r2_r3_native_binding_spec_artifact_status() -> None:
    artifact = json.loads(
        (
            ROOT
            / "artifacts/chronos/newstein_r1_r2_r3_native_binding_spec_2026_05_24.json"
        ).read_text()
    )
    assert artifact["status"] == "SPECIFICATION_ONLY_NO_NATIVE_INSTANCE"
    assert artifact["lean_object"] == "RepositoryNativeR1R2R3BindingSpec"
    assert "r1Correct" in artifact["required_correctness_fields"]
    assert "r2Correct" in artifact["required_correctness_fields"]
    assert "r3Correct" in artifact["required_correctness_fields"]

def test_newstein_r1_r2_r3_native_binding_spec_no_overclaim() -> None:
    combined = "\n".join(
        p.read_text()
        for p in [
            ROOT / "lean/Chronos/Frontier/NewsteinR1R2R3NativeBindingSpec.lean",
            ROOT / "docs/math/NEWSTEIN_R1_R2_R3_NATIVE_BINDING_SPEC.md",
            ROOT / "docs/status/NEWSTEIN_R1_R2_R3_NATIVE_BINDING_SPEC_2026_05_24.md",
            ROOT / "artifacts/chronos/newstein_r1_r2_r3_native_binding_spec_2026_05_24.json",
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

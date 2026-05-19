import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_uniform_temporal_relaxation_wave_target_verifier():
    subprocess.run(
        ["python3", "tools/verify_uniform_temporal_relaxation_wave_target.py"],
        cwd=ROOT,
        check=True,
    )


def test_uniform_temporal_relaxation_wave_target_boundary_doc():
    text = (
        ROOT / "docs/status/UNIFORM_TEMPORAL_RELAXATION_WAVE_TARGET_2026_05_19.md"
    ).read_text()
    assert "Status: `FRONTIER_OPEN`" in text
    assert "Target isolation only." in text
    assert "Does not prove:" in text
    assert "existence of UniformTemporalRelaxationWave" in text
    assert "unrestricted UniversalFiberEntropyGap" in text
    assert "unrestricted Chronos-RR" in text
    assert "P vs NP" in text

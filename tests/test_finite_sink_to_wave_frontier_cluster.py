import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_finite_sink_to_wave_frontier_cluster_verifier():
    subprocess.run(
        ["python3", "tools/verify_finite_sink_to_wave_frontier_cluster.py"],
        cwd=ROOT,
        check=True,
    )


def test_finite_sink_to_wave_frontier_cluster_boundary():
    text = (
        ROOT / "docs/status/FINITE_SINK_TO_WAVE_FRONTIER_CLUSTER_2026_05_19.md"
    ).read_text()
    assert "Status: `STATUS_LOCK_ONLY`" in text
    assert "UniformTemporalRelaxationWaveExistenceTarget" in text
    assert "Does not prove:" in text
    assert "unrestricted Chronos-RR" in text
    assert "P vs NP" in text

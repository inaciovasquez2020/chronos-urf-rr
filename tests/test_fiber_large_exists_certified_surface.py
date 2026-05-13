import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_fiber_large_exists_certified_surface_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_fiber_large_exists_certified_surface.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "FiberLargeExists certified surface status verified." in result.stdout


def test_fiber_large_exists_certified_surface_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/fiber_large_exists_certified_surface_2026_05_13.json").read_text()
    )
    assert data["status"] == "CERTIFIED_SURFACE_ONLY"
    assert data["frontier_open_preserved"] is True
    assert data["theorem_level_closure"] is False
    assert data["missing_object"] == "NonPropRankEntropyWitness"


def test_fiber_large_exists_certified_surface_boundary_doc():
    doc = (ROOT / "docs/status/CHRONOS_FIBER_LARGE_EXISTS_CERTIFIED_SURFACE_2026_05_13.md").read_text()
    assert "FRONTIER_OPEN is preserved." in doc
    assert "No unrestricted UniversalFiberEntropyGap theorem is claimed." in doc
    assert "No Chronos-RR theorem closure is claimed." in doc
    assert "No H4.1/FGL closure is claimed." in doc
    assert "No P vs NP closure is claimed." in doc
    assert "No Clay-problem closure is claimed." in doc

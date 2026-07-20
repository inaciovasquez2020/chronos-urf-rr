import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "artifacts/chronos/r2_cross_root_face_incidence_packet_2026_07_20.json"
TOOL = ROOT / "tools/verify_r2_cross_root_face_incidence_packet.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("r2_cross_root_verifier", TOOL)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cross_root_packet_verifier_passes():
    result = subprocess.run(
        [sys.executable, str(TOOL), str(PACKET)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "R2_CROSS_ROOT_FACE_INCIDENCE_PACKET_OK" in result.stdout


def test_matrices_and_local_quotients_are_computed_from_packet():
    verifier = load_verifier()
    packet = json.loads(PACKET.read_text())
    result = verifier.compute(packet)
    assert result["d1_d2_zero"] is True
    assert {root: data["quotient_dimension"] for root, data in result["local_results"].items()} == {
        "top": 1,
        "bottom": 1,
    }
    assert all(data["d2_rank"] == 0 for data in result["local_results"].values())


def test_every_nonzero_cross_root_system_is_solved_and_obstructed():
    verifier = load_verifier()
    packet = json.loads(PACKET.read_text())
    result = verifier.compute(packet)
    assert result["cross_root_system_count"] == 1
    assert result["solvable_cross_root_system_count"] == 1
    system = result["cross_root_systems"][0]
    assert len(system["solutions"]) == 1
    solution = system["solutions"][0]
    assert solution["support"] == ["f0a", "f0b", "f1a", "f1b", "f2a", "f2b"]
    assert solution["has_cross_root_component"] is True
    assert solution["components"] == [
        {
            "faces": ["f0a", "f0b", "f1a", "f1b", "f2a", "f2b"],
            "incident_roots": ["bottom", "top"],
        }
    ]
    assert result["replacement_theorem_holds"] is True
    assert result["nonvacuous"] is True


def test_rejects_non_chain_complex_packet(tmp_path):
    packet = json.loads(PACKET.read_text())
    packet["faces"][0]["boundary"] = ["t01", "v1", "v0"]
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(packet))
    result = subprocess.run(
        [sys.executable, str(TOOL), str(bad)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "boundary is not a triangle" in (result.stdout + result.stderr)

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "artifacts/chronos/r1_r2_r3_progressive_witness_packet_2026_05_24.json"

def run_cmd(args, check=False):
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )

def test_progressive_packet_open_frontier_verifier_passes():
    result = run_cmd(
        [sys.executable, "tools/verify_r1_r2_r3_progressive_witness_packet.py"],
        check=True,
    )
    assert "R1_R2_R3_PROGRESSIVE_WITNESS_PACKET_OPEN_FRONTIER_OK" in result.stdout

def test_progressive_packet_strict_mode_fails_until_data_is_filled():
    result = run_cmd(
        [sys.executable, "tools/verify_r1_r2_r3_progressive_witness_packet.py", "--strict"],
        check=False,
    )
    assert result.returncode != 0
    assert "strict mode requires closure_ready true" in (result.stdout + result.stderr)

def test_progressive_packet_rejects_premature_closure_ready(tmp_path):
    data = json.loads(PACKET.read_text())
    data["closure_ready"] = True
    data["strict_completion_status"] = "READY"
    bad = tmp_path / "premature_ready.json"
    bad.write_text(json.dumps(data, indent=2))

    result = run_cmd(
        [sys.executable, "tools/verify_r1_r2_r3_progressive_witness_packet.py", str(bad)],
        check=False,
    )

    assert result.returncode != 0
    assert "must be VERIFIED" in (result.stdout + result.stderr)

def test_progressive_packet_has_all_eleven_stages():
    data = json.loads(PACKET.read_text())
    assert len(data["piece_by_piece_order"]) == 11
    assert data["piece_by_piece_order"][0] == "R1_LONG_CHORD_EXCLUSION_DATA"
    assert data["piece_by_piece_order"][-1] == "REPOSITORY_NATIVE_R1_R2_R3_BINDING_CLOSURE"

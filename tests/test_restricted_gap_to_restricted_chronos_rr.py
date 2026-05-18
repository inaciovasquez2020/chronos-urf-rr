from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_restricted_gap_to_restricted_chronos_rr.py"],
        cwd=ROOT,
        check=True,
    )

def test_artifact_status_and_boundary():
    artifact = json.loads(
        (ROOT / "artifacts/chronos/restricted_universal_fiber_entropy_gap_to_restricted_chronos_rr_2026_05_18.json").read_text()
    )
    assert artifact["target"] == "RestrictedUniversalFiberEntropyGapToRestrictedChronosRR"
    assert artifact["status"] == "RESTRICTED_GAP_TO_RESTRICTED_CHRONOS_RR_CLOSED"
    boundary = "\n".join(artifact["boundary"])
    assert "restricted Chronos-RR witness only" in boundary
    assert "restricted-domain bridge only" in boundary
    assert "unrestricted Chronos-RR remains FRONTIER_OPEN" in boundary
    assert "no unrestricted Chronos-RR" in boundary
    assert "no Clay-problem closure" in boundary

def test_lean_surface_contains_restricted_chronos_rr_only():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedUniversalFiberEntropyGapToRestrictedChronosRR.lean").read_text()
    assert "structure RestrictedChronosRRWitness" in text
    assert "def RestrictedUniversalFiberEntropyGapToRestrictedChronosRR" in text
    assert "restricted_gap_to_restricted_chronos_rr_closed" in text
    assert "unrestricted_chronos_rr_frontier_open" in text
    assert "def ChronosRR" not in text
    assert "structure ChronosRR" not in text
    assert "theorem unrestricted_chronos_rr " not in text
    assert "admit" not in text
    assert "sorry" not in text
    assert "axiom" not in text

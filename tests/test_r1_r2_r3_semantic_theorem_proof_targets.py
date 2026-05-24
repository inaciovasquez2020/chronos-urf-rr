import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_r1_r2_r3_semantic_theorem_proof_targets_verifier() -> None:
    subprocess.run(
        ["python3", "tools/verify_r1_r2_r3_semantic_theorem_proof_targets.py"],
        cwd=ROOT,
        check=True,
    )

def test_r1_r2_r3_semantic_theorem_proof_targets_artifact_status() -> None:
    artifact = json.loads(
        (
            ROOT
            / "artifacts/chronos/r1_r2_r3_semantic_theorem_proof_targets_2026_05_24.json"
        ).read_text()
    )
    assert artifact["status"] == "CONDITIONAL_SEMANTIC_THEOREM_PROOF_ROUTE_ONLY"
    assert "R1_R2_R3_theorem_proof_targets_from_semantic_inputs" in artifact["closed_surfaces"]

def test_r1_r2_r3_semantic_theorem_proof_targets_no_overclaim() -> None:
    combined = "\n".join(
        p.read_text()
        for p in [
            ROOT / "lean/Chronos/Frontier/R1R2R3SemanticTheoremProofTargets.lean",
            ROOT / "docs/status/R1_R2_R3_SEMANTIC_THEOREM_PROOF_TARGETS_2026_05_24.md",
            ROOT / "artifacts/chronos/r1_r2_r3_semantic_theorem_proof_targets_2026_05_24.json",
        ]
    )
    forbidden = [
        "proved LongChordExclusion",
        "proved DiameterSeparationFillingObstruction",
        "proved UniformLocalTypeCapacity",
        "proved NON_FACTORISATION",
        "proved Chronos-RR",
        "proved H4.1/FGL",
        "P vs NP proved",
        "Clay problem solved",
    ]
    for token in forbidden:
        assert token not in combined

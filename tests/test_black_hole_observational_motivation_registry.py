import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/black_hole_observational_motivation_registry_2026_05_24.json"
LEAN = ROOT / "lean/Chronos/Frontier/BlackHoleObservationalMotivationRegistry.lean"
DOC = ROOT / "docs/status/BLACK_HOLE_OBSERVATIONAL_MOTIVATION_REGISTRY_2026_05_24.md"

def test_black_hole_observational_registry_artifact_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "OBSERVATIONAL_MOTIVATION_REGISTRY_ONLY_NO_THEOREM_PROMOTION"
    assert data["usable_as_proof_input"] is False
    assert len(data["records"]) == 5
    assert "no cosmic censorship" in data["does_not_prove"]
    assert "no hoop conjecture" in data["does_not_prove"]
    assert "no Clay problem" in data["does_not_prove"]

def test_black_hole_observational_registry_lean_not_proof_input():
    text = LEAN.read_text()
    assert "usableAsProofInput := false" in text
    assert "blackHoleObservationalMotivationRegistry_notProofInput" in text
    assert "OBSERVATIONAL_MOTIVATION_REGISTRY_ONLY_NO_THEOREM_PROMOTION" in text

def test_black_hole_observational_registry_doc_boundary():
    text = DOC.read_text()
    assert "These records are source-level motivation only." in text
    assert "They are not proof inputs." in text
    assert "no unrestricted black-hole formation theorem" in text
    assert "no P vs NP" in text

def test_black_hole_observational_registry_verifier_runs():
    subprocess.run(
        ["python3", "tools/verify_black_hole_observational_motivation_registry.py"],
        cwd=ROOT,
        check=True,
    )

import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/diameter_separation_filling_obstruction_proof_target_2026_06_01.json")
DOC = Path("docs/status/DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_TARGET_2026_06_01.md")
VERIFY = Path("tools/verify_diameter_separation_filling_obstruction_proof_target.py")

def test_artifact_is_target_open():
    data = json.loads(ART.read_text())
    assert data["object"] == "DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_TARGET"
    assert data["status"] == "TARGET_OPEN_OBSTRUCTION_PROOF_NOT_SUPPLIED"
    assert data["decision"] == "PASS"

def test_no_obstruction_proof_claimed():
    data = json.loads(ART.read_text())
    assert data["proof_supplied"] is False
    assert data["diameter_separation_filling_obstruction_closed"] is False

def test_required_inputs_are_missing():
    data = json.loads(ART.read_text())
    required = {
        "diameter_separation_domain",
        "filling_operation_definition",
        "separation_invariant_definition",
        "positive_invariant_binding",
        "diameter_bound_binding",
        "obstruction_statement",
        "lean_checked_obstruction_proof_or_explicit_missing_lemma",
    }
    assert required.issubset(set(data["missing_inputs"]))

def test_doc_records_next_admissible_object():
    doc = DOC.read_text()
    assert "DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_OR_EXPLICIT_MISSING_LEMMA" in doc
    assert "TARGET_OPEN_OBSTRUCTION_PROOF_NOT_SUPPLIED" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DIAMETER_SEPARATION_FILLING_OBSTRUCTION_PROOF_TARGET_OK" in result.stdout

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/external_strengthening_data_ledger_2026_05_24.json"
LEAN = ROOT / "lean/Chronos/Frontier/ExternalStrengtheningDataLedger.lean"
DOC = ROOT / "docs/status/EXTERNAL_STRENGTHENING_DATA_LEDGER_2026_05_24.md"

def test_external_strengthening_data_ledger_artifact_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "EXTERNAL_STRENGTHENING_DATA_LEDGER_ONLY_NO_THEOREM_PROMOTION"
    assert data["usable_as_proof_input"] is False
    assert len(data["records"]) == 6
    assert "no Chronos-RR" in data["does_not_prove"]
    assert "no H4.1/FGL" in data["does_not_prove"]
    assert "no P vs NP" in data["does_not_prove"]
    assert "no Clay problem" in data["does_not_prove"]

def test_external_strengthening_data_ledger_records_are_non_proof_inputs():
    data = json.loads(ART.read_text())
    assert all(record["usable_as_proof_input"] is False for record in data["records"])
    assert all(0 <= int(record["strength_score"]) <= 3 for record in data["records"])
    assert any(record["source_type"] == "verificationFramework" for record in data["records"])
    assert any(record["source_type"] == "institutionalResultsFramework" for record in data["records"])

def test_external_strengthening_data_ledger_lean_negative_control():
    text = LEAN.read_text()
    assert "externalStrengtheningDataNegativeControlRule" in text
    assert "usableAsProofInput := false" in text
    assert "externalStrengtheningDataLedger_notProofInput" in text

def test_external_strengthening_data_ledger_doc_boundary():
    text = DOC.read_text()
    assert "These records are source-level strengthening data only." in text
    assert "They are not proof inputs." in text
    assert "No external source may promote a theorem status" in text
    assert "no cosmic censorship" in text
    assert "no hoop conjecture" in text

def test_external_strengthening_data_ledger_verifier_runs():
    subprocess.run(
        ["python3", "tools/verify_external_strengthening_data_ledger.py"],
        cwd=ROOT,
        check=True,
    )

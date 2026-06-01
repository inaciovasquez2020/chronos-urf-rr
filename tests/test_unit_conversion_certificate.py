import json
import subprocess
from pathlib import Path

ART = Path("artifacts/chronos/unit_conversion_certificate_2026_06_01.json")
DOC = Path("docs/status/UNIT_CONVERSION_CERTIFICATE_2026_06_01.md")
VERIFY = Path("tools/verify_unit_conversion_certificate.py")

def test_artifact_records_unit_conversion_certificate():
    data = json.loads(ART.read_text())
    assert data["object"] == "UNIT_CONVERSION_CERTIFICATE"
    assert data["decision"] == "PASS"
    assert data["resolved_missing_input"] == "unit_conversion_certificate"

def test_conversion_rule_is_present():
    data = json.loads(ART.read_text())
    conv = data["unit_conversion"]
    assert conv["source_units_raw"]
    assert conv["canonical_unit"] == "meter liquid-water-equivalent thickness"
    assert conv["factor_to_canonical"] > 0
    assert "conversion_rule" in conv

def test_remaining_missing_inputs_are_two():
    data = json.loads(ART.read_text())
    assert data["remaining_missing_input_count"] == 2
    assert "predeclared_comparison_metric" in data["remaining_missing_inputs"]
    assert "reproducible_comparison_run_output" in data["remaining_missing_inputs"]

def test_doc_preserves_boundary():
    doc = DOC.read_text()
    assert "unit conversion certificate only" in doc
    assert "no empirical gravity result supplied" in doc
    assert "no Clay-problem claim" in doc

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFY)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "UNIT_CONVERSION_CERTIFICATE_OK" in result.stdout

from pathlib import Path
import yaml

def test_local_indistinguishability_note_exists():
    p = Path("local_certificate/LOCAL_INDISTINGUISHABILITY_CERTIFICATE.md")
    assert p.exists()
    s = p.read_text()
    assert "Certify that the witness pair" in s
    assert "Blocking Gap" in s

def test_local_indistinguishability_status_exists():
    p = Path("local_certificate/LOCAL_INDISTINGUISHABILITY_STATUS.yaml")
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    assert data["status"] == "scaffold"
    assert data["object"] == "local_indistinguishability_certificate"

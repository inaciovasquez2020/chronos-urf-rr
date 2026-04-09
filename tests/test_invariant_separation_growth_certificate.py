from pathlib import Path
import yaml

def test_invariant_separation_growth_note_exists():
    p = Path("growth_certificate/INVARIANT_SEPARATION_GROWTH_CERTIFICATE.md")
    assert p.exists()
    s = p.read_text()
    assert "Certify quantitative growth" in s
    assert "Blocking Gap" in s

def test_invariant_separation_growth_status_exists():
    p = Path("growth_certificate/INVARIANT_SEPARATION_GROWTH_STATUS.yaml")
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    assert data["status"] == "scaffold"
    assert data["object"] == "invariant_separation_growth_certificate"

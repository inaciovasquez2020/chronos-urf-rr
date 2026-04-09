from pathlib import Path
import yaml

def test_explicit_witness_constructor_note_exists():
    p = Path("witness_family/EXPLICIT_WITNESS_CONSTRUCTOR.md")
    assert p.exists()
    s = p.read_text()
    assert "Construct a finite witness family W(n)" in s
    assert "Blocking Gap" in s

def test_witness_family_status_exists():
    p = Path("witness_family/WITNESS_FAMILY_STATUS.yaml")
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    assert data["status"] == "scaffold"
    assert data["object"] == "explicit_witness_family"

from pathlib import Path
import yaml

def test_explicit_witness_instance_note_exists():
    p = Path("witness_instance/EXPLICIT_WITNESS_INSTANCE.md")
    assert p.exists()
    s = p.read_text()
    assert "Petersen graph" in s
    assert "I_URF" in s

def test_witness_instance_status_exists():
    p = Path("witness_instance/WITNESS_INSTANCE_STATUS.yaml")
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    assert data["status"] == "partial_compute"
    assert data["object"] == "explicit_witness_instance"
    assert data["lift_defined"] is True
    assert data["invariant_computed"] is True
    assert data["separation_verified"] is True

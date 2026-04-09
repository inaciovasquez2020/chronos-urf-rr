from pathlib import Path
import yaml

def test_computable_urf_invariant_note_exists():
    p = Path("invariant/COMPUTABLE_URF_INVARIANT.md")
    assert p.exists()
    s = p.read_text()
    assert "Define I_URF(G;R)" in s
    assert "Blocking Gap" in s

def test_urf_invariant_status_exists():
    p = Path("invariant/URF_INVARIANT_STATUS.yaml")
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    assert data["status"] == "scaffold"
    assert data["object"] == "computable_urf_invariant"

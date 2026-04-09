from pathlib import Path

def test_canonical_theorem_object_exists():
    p = Path("theorem_object/CANONICAL_THEOREM_OBJECT.md")
    assert p.exists()
    s = p.read_text()
    assert "Unconditional Core Statement" in s
    assert "Blocking Gap" in s

def test_independent_audit_checklist_exists():
    p = Path("theorem_object/INDEPENDENT_AUDIT_CHECKLIST.md")
    assert p.exists()
    s = p.read_text()
    assert "Exact theorem statement fixed" in s
    assert "Lean theorem shell matches theorem text exactly" in s

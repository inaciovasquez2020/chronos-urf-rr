from pathlib import Path

def test_reference_docs():
    assert Path("docs/REFERENCE_ROLE.md").exists()
    assert Path("examples/minimal_pipeline.md").exists()


def test_reference_registry_alignment():
    reference_role = Path("docs/REFERENCE_ROLE.md").read_text(encoding="utf-8")

    assert "Chronos–EntropyDepth" in reference_role
    assert "URF Core / URF Spine" in reference_role
    assert "reference implementation" in reference_role.lower()
    assert "non-normative" in reference_role.lower()

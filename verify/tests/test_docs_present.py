from pathlib import Path

def test_reference_docs():
    assert Path("docs/REFERENCE_ROLE.md").exists()
    assert Path("examples/minimal_pipeline.md").exists()

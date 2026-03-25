from pathlib import Path

def test_rr_invariants_doc_exists():
    assert Path("docs/RR_INVARIANTS.md").exists()

def test_examples_exist():
    assert Path("examples/minimal_run.md").exists()

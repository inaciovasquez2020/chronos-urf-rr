from pathlib import Path

README = Path("README.md").read_text()
STATUS = Path("STATUS.md").read_text()
SNAP = Path("STATUS_SNAPSHOT.md").read_text()

OPEN_ITEMS = [
    "(R1) Long-Chord Exclusion Lemma",
    "(R2) Diameter-Separation Filling Obstruction",
    "(R3) Uniform Local-Type Capacity Lemma",
]

def test_readme_marks_repo_conditional():
    assert "CONDITIONAL" in README

def test_snapshot_marks_repo_conditional():
    assert "CONDITIONAL" in SNAP

def test_open_items_match_between_readme_and_snapshot():
    for item in OPEN_ITEMS:
        assert item in README
        assert item in SNAP

def test_status_does_not_claim_final_closure():
    banned = [
        "Final State",
        "no active development planned",
    ]
    for token in banned:
        assert token not in README
        assert token not in STATUS

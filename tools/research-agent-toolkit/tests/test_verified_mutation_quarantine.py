"""No side effects from unrestricted callback API: deliberate contract migration.

All paths are inside disposable pytest tmp_path directories. No real repo writes.
"""
import pathlib
import sys
import pytest
from research_agent_toolkit.transaction import verified_mutation


def test_rejects_arbitrary_callback_before_execution(tmp_path: pathlib.Path):
    target=tmp_path / "x.txt"
    target.write_text("before")
    outside=tmp_path / "unique_research.txt"
    called=[]
    def attacker():
        called.append(True)
        target.write_text("mutated")
        outside.write_text("private unique research")
    with pytest.raises(PermissionError, match="disabled"):
        verified_mutation([target],attacker,[sys.executable,"-c","raise SystemExit(0)"],cwd=tmp_path)
    assert called==[]
    assert target.read_text()=="before"
    assert not outside.exists()


def test_denies_callback_even_on_verifier_failure(tmp_path: pathlib.Path):
    target=tmp_path / "x.txt"
    target.write_text("before")
    called=[]
    def attacker():
        called.append(1)
        target.write_text("changed")
    with pytest.raises(PermissionError, match="disabled"):
        verified_mutation([target],attacker,[sys.executable,"-c","raise SystemExit(7)"],cwd=tmp_path)
    assert not called and target.read_text()=="before"


def test_denies_exceptional_callback_without_running(tmp_path: pathlib.Path):
    target=tmp_path / "x.txt"
    target.write_text("before")
    def attacker():
        target.write_text("changed")
        raise RuntimeError("callback exploded")
    with pytest.raises(PermissionError, match="disabled"):
        verified_mutation([target],attacker,[sys.executable,"-c","raise SystemExit(0)"],cwd=tmp_path)
    assert target.read_text()=="before"


def test_denies_verifier_spawn_failure_without_mutation(tmp_path: pathlib.Path):
    target=tmp_path / "x.txt"
    target.write_text("before")
    with pytest.raises(PermissionError, match="disabled"):
        verified_mutation([target],lambda: target.write_text("changed"),["__no_verifier_exists__"],cwd=tmp_path)
    assert target.read_text()=="before"


def test_denies_symlink_escape_without_dereference(tmp_path: pathlib.Path):
    target=tmp_path / "sensitive.txt"
    target.write_text("keep")
    link=tmp_path / "link.txt"
    link.symlink_to(target)
    with pytest.raises(PermissionError, match="disabled"):
        verified_mutation([link],lambda:link.write_text("overwrite"),[sys.executable,"-c","pass"],cwd=tmp_path)
    assert target.read_text()=="keep"
    assert link.is_symlink()


def test_denies_invalid_targets_and_never_executes_callback(tmp_path: pathlib.Path):
    called=[]
    with pytest.raises(PermissionError, match="disabled"):
        verified_mutation([tmp_path/"not-present"],lambda:called.append(1),["missing"],cwd=tmp_path)
    assert called==[]

"""Adversarial exact-cleanliness tests; no authoritative checkout writes."""
import os
import stat
import subprocess
from pathlib import Path
import pytest
from urf_ai.guard import modified_paths


def git(root, *args):
    r = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)
    return r.stdout


def make_repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.invalid")
    return root


def test_clean_filter_cannot_hide_raw_research_bytes(tmp_path):
    root = make_repo(tmp_path)
    git(root, "config", "filter.first.clean", "head -n 1")
    (root / ".gitattributes").write_text("research.txt filter=first\n")
    (root / "research.txt").write_text("baseline\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "baseline")
    assert modified_paths(root) == set()
    (root / "research.txt").write_text("baseline\nPRIVATE_UNSAVED_RESEARCH\n")
    assert git(root, "diff", "--name-only") == ""  # adversarial control
    assert "research.txt" in modified_paths(root)
    assert (root / "research.txt").read_text().endswith("PRIVATE_UNSAVED_RESEARCH\n")


def test_filemode_false_cannot_hide_executable_change(tmp_path):
    root = make_repo(tmp_path)
    file = root / "research.txt"
    file.write_text("data\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "baseline")
    git(root, "config", "core.filemode", "false")
    file.chmod(file.stat().st_mode | stat.S_IXUSR)
    assert git(root, "status", "--porcelain") == ""  # adversarial control
    assert "research.txt" in modified_paths(root)


def test_symlink_changed_target_is_detected(tmp_path):
    if not hasattr(os, "symlink"):
        pytest.skip("requires symlink")
    root = make_repo(tmp_path)
    (root / "target_a").write_text("a\n")
    (root / "target_b").write_text("b\n")
    (root / "ln").symlink_to("target_a")
    git(root, "add", ".")
    git(root, "commit", "-qm", "baseline")
    assert modified_paths(root) == set()
    (root / "ln").unlink()
    (root / "ln").symlink_to("target_b")
    assert "ln" in modified_paths(root)


def test_regular_file_replaced_by_symlink_fails_closed(tmp_path):
    root = make_repo(tmp_path)
    (root / "a").write_text("a\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "baseline")
    (root / "a").unlink()
    (root / "a").symlink_to("/nonexistent/external/path")
    assert "a" in modified_paths(root)


def test_normal_tracked_files_are_clean(tmp_path):
    root = make_repo(tmp_path)
    (root / "alpha").write_bytes(b"abc\x00\xff")
    (root / "beta").write_text("some content\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "baseline")
    assert modified_paths(root) == set()

@pytest.mark.parametrize("attack", ["clean-filter", "filemode-disabled"])
def test_authorized_patch_refused_if_baseline_has_hidden_change(tmp_path, attack):
    from urf_ai.guard import issue_approval, run_mutation
    from urf_ai.approval_ledger import create_ledger

    root = make_repo(tmp_path)
    if attack == "clean-filter":
        git(root, "config", "filter.first.clean", "head -n 1")
        (root / ".gitattributes").write_text("research.txt filter=first\n")
    (root / "research.txt").write_text("baseline\n")
    (root / "target.txt").write_text("before\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "baseline")
    if attack == "clean-filter":
        (root / "research.txt").write_text("baseline\nUNSAVED_RESEARCH\n")
    else:
        git(root, "config", "core.filemode", "false")
        source = root / "research.txt"
        source.chmod(source.stat().st_mode | stat.S_IXUSR)
    patch = ("diff --git a/target.txt b/target.txt\n"
             "--- a/target.txt\n+++ b/target.txt\n"
             "@@ -1 +1 @@\n-before\n+after\n").encode()
    config = {
        "disposable_worktree_confirmed": True, "explicit_write_approval": True,
        "scope": {"allow": ["*.txt"], "deny": []},
        "gates": {"verify_actions": ["modify"], "deny_actions": []},
        "policy": {"forbidden_patterns": []},
        "budgets": {"mutations": 1, "max_verifier_seconds": 5},
        "verifier_commands": [["RAT_INTERNAL_DIFF_CHECK"]],
    }
    ledger = tmp_path / "trusted-ledger.db"
    create_ledger(ledger)
    key = b"test-only-controller-key" * 3
    approval = issue_approval(root, patch, {"target.txt"}, config,
                              ["RAT_INTERNAL_DIFF_CHECK"], key, approval_ledger=ledger)
    result = run_mutation(root, patch, {"target.txt"}, config,
                          ["RAT_INTERNAL_DIFF_CHECK"], approval=approval,
                          authorization_key=key, approval_ledger=ledger, timeout_seconds=2)
    assert (result.status, result.stage) == ("DENY", "preflight")
    assert (root / "target.txt").read_text() == "before\n"
    if attack == "clean-filter":
        assert (root / "research.txt").read_text().endswith("UNSAVED_RESEARCH\n")
    else:
        assert (root / "research.txt").stat().st_mode & stat.S_IXUSR

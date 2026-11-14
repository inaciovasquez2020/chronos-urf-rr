"""Adversarial Git index-flag regressions. Disposable tmp_path only."""
from pathlib import Path
import subprocess
import pytest
from urf_ai.guard import modified_paths, issue_approval, run_mutation
from urf_ai.approval_ledger import create_ledger

KEY=b"controlled-test-secret"*3
VERIFIER=["RAT_INTERNAL_DIFF_CHECK"]

def setup(root: Path):
    repo=root/"worktree";repo.mkdir()
    def cmd(*args):
        return subprocess.run(["git",*args],cwd=repo,check=True,capture_output=True,text=True).stdout
    cmd("init","-q");cmd("config","user.email","security@example.invalid");cmd("config","user.name","Security Test")
    (repo/"src").mkdir()
    (repo/"src"/"private.txt").write_text("precious research\n")
    (repo/"src"/"target.txt").write_text("before\n")
    cmd("add",".");cmd("commit","-qm","initial")
    config={"disposable_worktree_confirmed":True,"explicit_write_approval":True,
            "scope":{"allow":["src/**"],"deny":[".git/**"]},
            "gates":{"verify_actions":["modify"],"deny_actions":[]},
            "policy":{"forbidden_patterns":[]},
            "budgets":{"mutations":1,"max_verifier_seconds":5},
            "verifier_commands":[VERIFIER]}
    ledger=root/"spent.sqlite";create_ledger(ledger)
    patch=("diff --git a/src/target.txt b/src/target.txt\n"
           "--- a/src/target.txt\n+++ b/src/target.txt\n@@ -1 +1 @@\n-before\n+after\n").encode()
    return repo,cmd,config,ledger,patch

@pytest.mark.parametrize("flag,expected_marker",[("--skip-worktree","S"),("--assume-unchanged","h")])
def test_hidden_tracked_research_file_is_not_clean(tmp_path,flag,expected_marker):
    repo,cmd,cfg,ledger,patch=setup(tmp_path)
    cmd("update-index",flag,"src/private.txt")
    (repo/"src"/"private.txt").write_text("UNSAVED LOCAL RESEARCH\n")
    assert cmd("status","--porcelain=v1").strip()==""   # the adversarial control
    assert cmd("ls-files","-v","src/private.txt").startswith(expected_marker+" ")
    assert "src/private.txt" in modified_paths(repo)
    closure={"src/target.txt"}
    signed=issue_approval(repo,patch,closure,cfg,VERIFIER,KEY,approval_ledger=ledger)
    outcome=run_mutation(repo,patch,closure,cfg,VERIFIER,approval=signed,authorization_key=KEY,approval_ledger=ledger,timeout_seconds=2)
    assert outcome.status=="DENY" and outcome.stage=="preflight",outcome
    assert (repo/"src"/"private.txt").read_text()=="UNSAVED LOCAL RESEARCH\n"
    assert (repo/"src"/"target.txt").read_text()=="before\n"

@pytest.mark.parametrize("flag",["--skip-worktree","--assume-unchanged"])
def test_even_unchanged_masked_index_file_is_denied(tmp_path,flag):
    repo,cmd,cfg,ledger,patch=setup(tmp_path)
    cmd("update-index",flag,"src/private.txt")
    assert "src/private.txt" in modified_paths(repo)
    signed=issue_approval(repo,patch,{"src/target.txt"},cfg,VERIFIER,KEY,approval_ledger=ledger)
    outcome=run_mutation(repo,patch,{"src/target.txt"},cfg,VERIFIER,approval=signed,authorization_key=KEY,approval_ledger=ledger,timeout_seconds=2)
    assert outcome.status=="DENY" and outcome.stage=="preflight"
    assert (repo/"src"/"target.txt").read_text()=="before\n"

def test_normal_index_allows_structural_candidate(tmp_path):
    repo,cmd,cfg,ledger,patch=setup(tmp_path)
    assert modified_paths(repo)==set()
    signed=issue_approval(repo,patch,{"src/target.txt"},cfg,VERIFIER,KEY,approval_ledger=ledger)
    outcome=run_mutation(repo,patch,{"src/target.txt"},cfg,VERIFIER,approval=signed,authorization_key=KEY,approval_ledger=ledger,timeout_seconds=2)
    assert outcome.status=="STRUCTURAL_CANDIDATE_NOT_PROMOTED" and outcome.returncode==4,outcome
    assert (repo/"src"/"target.txt").read_text()=="after\n"

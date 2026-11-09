"""Independent adversarial ledger tests; all sources/sinks are in tmp_path."""
import json
import subprocess
import concurrent.futures
import sys
from pathlib import Path
import pytest
from urf_ai.guard import issue_approval, run_mutation
from urf_ai.approval_ledger import create_ledger, ledger_identity, consume_approval, LedgerError

KEY = b"synthetic-local-security-test-only" * 2
CHECK = ["RAT_INTERNAL_DIFF_CHECK"]
SYNTAX = ["RAT_INTERNAL_PYTHON_SYNTAX"]

def repo(tmp_path,*,python_file=True):
    root=tmp_path/'worktree';root.mkdir()
    def command(*args):return subprocess.run(['git',*args],cwd=root,check=True,capture_output=True).stdout
    command('init','-q');command('config','user.email','fixture@example.invalid');command('config','user.name','Fixture')
    (root/'src').mkdir();(root/'src/x.py').write_text('value = 1\n')
    command('add','.');command('commit','-qm','initial')
    config={'disposable_worktree_confirmed':True,'explicit_write_approval':True,
        'scope':{'allow':['src/**'],'deny':['.git/**']},
        'gates':{'verify_actions':['modify'],'deny_actions':[]},
        'policy':{'forbidden_patterns':[r'\bsorry\b']},
        'budgets':{'mutations':1,'max_verifier_seconds':5},
        'verifier_commands':[CHECK,SYNTAX]}
    patch=b'diff --git a/src/x.py b/src/x.py\n--- a/src/x.py\n+++ b/src/x.py\n@@ -1 +1 @@\n-value = 1\n+value = 2\n'
    ledger=tmp_path/'spent.sqlite';create_ledger(ledger)
    return root,config,patch,ledger

def authorize(root,cfg,patch,ledger,verifier=CHECK):
    return issue_approval(root,patch,{'src/x.py'},cfg,verifier,KEY,approval_ledger=ledger)

def execute(root,cfg,patch,ledger,token,verifier=CHECK):
    return run_mutation(root,patch,{'src/x.py'},cfg,verifier,approval=token,authorization_key=KEY,approval_ledger=ledger,timeout_seconds=2)

def test_spent_approval_survives_rollback_and_reopen(tmp_path):
    root,cfg,_,ledger=repo(tmp_path)
    bad=b'diff --git a/src/x.py b/src/x.py\n--- a/src/x.py\n+++ b/src/x.py\n@@ -1 +1 @@\n-value = 1\n+value = (\n'
    token=authorize(root,cfg,bad,ledger,SYNTAX)
    first=execute(root,cfg,bad,ledger,token,SYNTAX)
    assert first.status=='FAILED_ROLLED_BACK' and first.returncode==7,first
    assert (root/'src/x.py').read_text()=='value = 1\n'
    assert ledger_identity(ledger)==token['request']['ledger_id']
    # Second independent database connection must see spent token after rollback.
    second=execute(root,cfg,bad,ledger,token,SYNTAX)
    assert (second.status,second.stage)==('DENY','replay'),second
    assert (root/'src/x.py').read_text()=='value = 1\n'

def test_spent_approval_survives_success_and_revert(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    token=authorize(root,cfg,patch,ledger)
    assert execute(root,cfg,patch,ledger,token).status=='STRUCTURAL_CANDIDATE_NOT_PROMOTED'
    subprocess.run(['git','restore','--','src/x.py'],cwd=root,check=True)
    assert execute(root,cfg,patch,ledger,token).stage=='replay'

def test_atomic_concurrent_claim_one_winner(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    token=authorize(root,cfg,patch,ledger)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        got=list(pool.map(lambda _:consume_approval(ledger,token), range(12)))
    assert got.count(True)==1 and got.count(False)==11,got

def test_missing_ledger_is_denied(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    token=authorize(root,cfg,patch,ledger)
    assert execute(root,cfg,patch,ledger.parent/'missing.sqlite',token).status=='DENY'
    assert (root/'src/x.py').read_text()=='value = 1\n'

def test_different_ledger_identity_denied(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    alternate=tmp_path/'alternate.sqlite';create_ledger(alternate)
    token=authorize(root,cfg,patch,ledger)
    assert execute(root,cfg,patch,alternate,token).status=='DENY'
    assert execute(root,cfg,patch,ledger,token).status=='STRUCTURAL_CANDIDATE_NOT_PROMOTED'

def test_bogus_authentication_denied_and_not_spent(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    token=authorize(root,cfg,patch,ledger)
    forged=json.loads(json.dumps(token));forged['mac']='f'*64
    assert execute(root,cfg,patch,ledger,forged).status=='DENY'
    assert execute(root,cfg,patch,ledger,token).status=='STRUCTURAL_CANDIDATE_NOT_PROMOTED'

def test_user_subprocess_allowlist_is_not_a_sandbox(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    marker=tmp_path/'outside.txt'
    attacker=[sys.executable,'-c',f'from pathlib import Path;Path({str(marker)!r}).write_text("unauthorized")']
    cfg['verifier_commands'].append(attacker)
    token=authorize(root,cfg,patch,ledger,attacker)
    result=execute(root,cfg,patch,ledger,token,attacker)
    assert result.status=='DENY' and result.stage=='verifier',result
    assert not marker.exists()
    # Denial before consumption does not burn the independent controller's token.
    assert consume_approval(ledger,token)

def test_reject_symlinked_ledger(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    linked=tmp_path/'linked.sqlite';linked.symlink_to(ledger)
    with pytest.raises(LedgerError):ledger_identity(linked)

def test_reject_untrusted_mode(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    ledger.chmod(0o666)
    with pytest.raises(LedgerError):ledger_identity(ledger)

def test_no_automatic_ledger_creation_or_replacement(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    with pytest.raises(FileExistsError):create_ledger(ledger)
    with pytest.raises(LedgerError):ledger_identity(tmp_path/'unknown.sqlite')

def test_missing_ledger_in_guard_is_fail_closed(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    token=authorize(root,cfg,patch,ledger)
    result=run_mutation(root,patch,{'src/x.py'},cfg,CHECK,approval=token,authorization_key=KEY)
    assert result.status=='DENY' and (root/'src/x.py').read_text()=='value = 1\n'

def test_fresh_nonce_cannot_evade_session_budget(tmp_path):
    root,cfg,patch,ledger=repo(tmp_path)
    token1=authorize(root,cfg,patch,ledger)
    token2=authorize(root,cfg,patch,ledger)
    assert token1['request']['nonce']!=token2['request']['nonce']
    assert token1['request']['session_id']==token2['request']['session_id']
    assert consume_approval(ledger,token1)
    assert not consume_approval(ledger,token2)

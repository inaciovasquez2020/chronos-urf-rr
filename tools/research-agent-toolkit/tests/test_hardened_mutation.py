"""Security regression tests using the actual toolkit policy/provenance code.

Do not use production research repos as test roots: all mutation is confined to
pytest's expendable tmp_path Git repositories.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOLKIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLKIT / "src"))
sys.path.insert(0, str(TOOLKIT / "urf-ai"))

from research_agent_toolkit.hardened_mutation import governed_patch_mutation
from research_agent_toolkit.transaction import verified_dependency_subprocess
from research_agent_toolkit.agent_mutation import governed_patch_mutation as public_mutation
from urf_ai.guard import issue_approval


def cmd(root, *args):
    return subprocess.run(args, cwd=root, check=True, capture_output=True, text=True).stdout


@pytest.fixture
def repo(tmp_path):
    cmd(tmp_path, "git", "init", "-q")
    cmd(tmp_path, "git", "config", "user.email", "rat@invalid.example")
    cmd(tmp_path, "git", "config", "user.name", "RAT Security Test")
    (tmp_path / "src").mkdir()
    for rel, content in [("generator.py", "generate\n"), ("artifact.txt", "before\n"), ("test_result.py", "pass\n")]:
        (tmp_path / "src" / rel).write_text(content)
    manifest={"chains":[{"claim":"test.claim", "generator":"src/generator.py", "artifact":"src/artifact.txt", "test":"src/test_result.py"}]}
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    config={"disposable_worktree_confirmed":True,"explicit_write_approval":True,
            "scope":{"allow":["src/**"],"deny":[".git/**"]},
            "gates":{"verify_actions":["modify"],"deny_actions":[]},
            "policy":{"forbidden_patterns":[r"\b(?:sorry|admit|axiom|opaque)\b"]},
            "budgets":{"mutations":1,"max_verifier_seconds":5},
            "verifier_commands":[[sys.executable,"-c","pass"]]}
    (tmp_path / "policy.json").write_text(json.dumps(config))
    cmd(tmp_path,"git","add",".")
    cmd(tmp_path,"git","commit","-qm","initial")
    patch="""diff --git a/src/artifact.txt b/src/artifact.txt
--- a/src/artifact.txt
+++ b/src/artifact.txt
@@ -1 +1 @@
-before
+after
"""
    return tmp_path,config,patch


def call(r,config,patch,*,secret=None,sign=True,verifier=None,configfile='policy.json',manifest='manifest.json',changed='src/artifact.txt'):
    secret=secret or b'x'*32
    verifier=verifier or [sys.executable,'-c','pass']
    closure={'src/artifact.txt','src/test_result.py'}
    approval=issue_approval(r,patch.encode(),closure,config,verifier,secret) if sign else None
    return governed_patch_mutation(r,manifest,changed,patch,verifier,config_path=configfile,
                                   approval=approval,authorization_key=secret,timeout_seconds=5)


def test_no_approval_has_no_write(repo):
    r,c,p=repo
    out=call(r,c,p,sign=False)
    assert not out.preserved and out.phase=='authorization'
    assert (r/'src/artifact.txt').read_text()=='before\n'


def test_scoped_approved_candidate_succeeds_only_in_disposable_repo(repo):
    r,c,p=repo
    out=call(r,c,p)
    assert out.preserved and out.stdout=='VERIFIED_CANDIDATE_NOT_PROMOTED'
    assert (r/'src/artifact.txt').read_text()=='after\n'


def test_existing_public_entrypoint_fails_closed(repo):
    r,c,p=repo
    out=public_mutation(r,'manifest.json','src/artifact.txt',p,[sys.executable,'-c','pass'])
    assert not out.preserved and out.phase=='authorization'
    assert (r/'src/artifact.txt').read_text()=='before\n'


def test_direct_subprocess_bypass_refused(repo):
    r,c,p=repo
    out=verified_dependency_subprocess(r,['src/artifact.txt'],[sys.executable,'-c',"open('src/artifact.txt','w').write('danger')"],[sys.executable,'-c','pass'])
    assert not out.preserved and out.phase=='LEGACY_MUTATION_DISABLED'
    assert (r/'src/artifact.txt').read_text()=='before\n'


def test_forbidden_proof_placeholder_rejected(repo):
    r,c,p=repo
    out=call(r,c,p.replace('+after','+sorry'))
    assert not out.preserved and out.phase=='policy'
    assert (r/'src/artifact.txt').read_text()=='before\n'


def test_missing_verify_gate_rejected(repo):
    r,c,p=repo
    c['gates']['verify_actions']=[]
    (r/'policy.json').write_text(json.dumps(c))
    cmd(r,'git','add','policy.json');cmd(r,'git','commit','-qm','policy')
    out=call(r,c,p)
    assert not out.preserved and out.phase=='policy'


def test_zero_mutation_budget_rejected(repo):
    r,c,p=repo
    c['budgets']['mutations']=0
    (r/'policy.json').write_text(json.dumps(c))
    cmd(r,'git','add','policy.json');cmd(r,'git','commit','-qm','budget')
    out=call(r,c,p)
    assert not out.preserved and out.phase=='policy'


def test_bad_provenance_and_config_paths_rejected(repo):
    r,c,p=repo
    assert call(r,c,p,manifest='../outside.json').phase=='provenance'
    assert call(r,c,p,configfile='../outside.json').phase=='policy'


def test_verifier_fail_restores_exact_patch_target(repo):
    r,c,p=repo
    verifier=[sys.executable,'-c','raise SystemExit(7)']
    c['verifier_commands'].append(verifier)
    (r/'policy.json').write_text(json.dumps(c))
    cmd(r,'git','add','policy.json');cmd(r,'git','commit','-qm','verifier')
    out=call(r,c,p,verifier=verifier)
    assert not out.preserved and out.returncode==7
    assert out.stdout=='FAILED_ROLLED_BACK',out
    assert (r/'src/artifact.txt').read_text()=='before\n'
    assert cmd(r,'git','status','--porcelain')==''


def test_preexisting_ignored_research_file_survives(repo):
    r,c,p=repo
    (r/'.gitignore').write_text('ignored/\n')
    cmd(r,'git','add','.gitignore');cmd(r,'git','commit','-qm','ignore')
    (r/'ignored').mkdir();(r/'ignored/unique.txt').write_text('PRESERVE')
    out=call(r,c,p)
    assert not out.preserved
    assert (r/'ignored/unique.txt').read_text()=='PRESERVE'
    assert (r/'src/artifact.txt').read_text()=='before\n'


def test_ignored_verifier_side_effect_not_accepted_or_deleted(repo):
    r,c,p=repo
    (r/'.gitignore').write_text('ignored/\n')
    cmd(r,'git','add','.gitignore');cmd(r,'git','commit','-qm','ignore')
    verifier=[sys.executable,'-c',"from pathlib import Path; Path('ignored').mkdir(); Path('ignored/unique.txt').write_text('PRESERVE')"]
    c['verifier_commands'].append(verifier)
    (r/'policy.json').write_text(json.dumps(c))
    cmd(r,'git','add','policy.json');cmd(r,'git','commit','-qm','verifier')
    out=call(r,c,p,verifier=verifier)
    assert not out.preserved and out.stdout=='INCOMPLETE_UNAUTHORIZED_RESIDUE',out
    assert (r/'ignored/unique.txt').read_text()=='PRESERVE'
    assert (r/'src/artifact.txt').read_text()=='before\n'


def test_scoped_mac_rejects_altered_key(repo):
    r,c,p=repo
    v=[sys.executable,'-c','pass']
    approval=issue_approval(r,p.encode(),{'src/artifact.txt','src/test_result.py'},c,v,b'x'*32)
    out=governed_patch_mutation(r,'manifest.json','src/artifact.txt',p,v,
                                 config_path='policy.json',approval=approval,authorization_key=b'z'*32)
    assert not out.preserved and out.stdout=='DENY' and (r/'src/artifact.txt').read_text()=='before\n'


def test_unsafe_patch_target_rejected(repo):
    r,c,p=repo
    bad=p.replace('src/artifact.txt','src/generator.py').replace('-before','-generate')
    out=call(r,c,bad)
    assert not out.preserved and out.phase=='closure'
    assert (r/'src/generator.py').read_text()=='generate\n'


def test_tracked_symlink_policy_and_manifest_denied(repo):
    r,c,p=repo
    (r/'policy-link.json').symlink_to('policy.json')
    (r/'manifest-link.json').symlink_to('manifest.json')
    assert call(r,c,p,configfile='policy-link.json').phase=='policy'
    assert call(r,c,p,manifest='manifest-link.json').phase=='provenance'
    assert (r/'src/artifact.txt').read_text()=='before\n'

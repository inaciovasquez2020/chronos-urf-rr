from __future__ import annotations
import ast, json, subprocess, sys
from pathlib import Path
from unittest.mock import patch
import pytest
from urf_ai import guard, classifier, sat_query_boundary

def test_classification_refuses_active_proof_boundary():
    claim={'claim_id':'x','kind':'THEOREM','scope':{'domain':'finite test'},
           'objects':{k:'present' for k in classifier.REQUIRED},
           'assumptions':[],'frontier':[],
           'boundaries':[{'active':True,'blocks_proved':True}]}
    with patch.object(classifier,'validated_receipt',return_value=(True,'test authenticated')):
        c=classifier.classify(claim,{},b'X'*32,{}, {})
    assert c['classification']=='INCOMPLETE_LEDGER',c

def test_optimized_python_does_not_bypass_finite_sat_checks():
    # The checker must execute its actual finite checks under -O.
    # This subprocess probe uses explicit conditional failure: an assert here
    # would itself be erased by -O and make the regression vacuous.
    code='from urf_ai.sat_query_boundary import sat_family_receipt; r=sat_family_receipt(5); print("PROBE_OK") if r["deterministic_query_lower_bound"]==5 else (_ for _ in ()).throw(RuntimeError("BAD_BOUND"))'
    p=subprocess.run([sys.executable,'-B','-O','-c',code],capture_output=True,text=True)
    assert p.returncode==0 and 'PROBE_OK' in p.stdout,(p.stdout,p.stderr)

def test_audit_critical_functions_use_no_disabled_asserts():
    root=Path(__file__).resolve().parents[1]
    for rel, funcs in {
        'urf_ai/sat_query_boundary.py': {'sat_family_receipt','eager_read_entropy','copy_machine_entropy_regression'},
        'tools/run_universality_bridge_audit.py': {'run'},
        'tools/run_sat_query_boundary_audit.py': {'run'},
    }.items():
        tree=ast.parse((root/rel).read_text())
        for fn in ast.walk(tree):
            if isinstance(fn,(ast.FunctionDef,ast.AsyncFunctionDef)) and fn.name in funcs:
                assert not any(isinstance(node,ast.Assert) for node in ast.walk(fn)),f'{rel}:{fn.name} still uses assert'

def test_rollback_on_post_apply_inventory_error(tmp_path):
    from test_approval_ledger import repo, authorize, execute
    root,cfg,patch_bytes,ledger=repo(tmp_path)
    token=authorize(root,cfg,patch_bytes,ledger)
    original=guard.modified_paths
    calls=[0]
    def intermittent_inventory(root):
        calls[0]+=1
        if calls[0]==2: raise RuntimeError('injected post-apply Git inventory error')
        return original(root)
    with patch.object(guard,'modified_paths',side_effect=intermittent_inventory):
        result=execute(root,cfg,patch_bytes,ledger,token)
    assert result.status=='FAILED_ROLLED_BACK',result
    assert (root/'src/x.py').read_text()=='value = 1\n'
    assert not guard.modified_paths(root)

def test_rollback_on_prerestore_inventory_error_is_incomplete(tmp_path):
    from test_approval_ledger import repo, authorize, execute, SYNTAX
    root,cfg,_,ledger=repo(tmp_path)
    patch_bytes=(b'diff --git a/src/x.py b/src/x.py\n'
                 b'--- a/src/x.py\n+++ b/src/x.py\n'
                 b'@@ -1 +1 @@\n-value = 1\n+value = (\n')
    token=authorize(root,cfg,patch_bytes,ledger,SYNTAX)
    original=guard.modified_paths
    calls=[0]
    def intermittent_inventory(root):
        calls[0]+=1
        if calls[0]==3: raise RuntimeError('injected pre-restore Git inventory error')
        return original(root)
    with patch.object(guard,'modified_paths',side_effect=intermittent_inventory):
        result=execute(root,cfg,patch_bytes,ledger,token,SYNTAX)
    assert result.status=='INCOMPLETE_ROLLBACK',result
    assert (root/'src/x.py').read_text()=='value = 1\n'
    assert not guard.modified_paths(root)

def test_optimized_runtime_detects_tampered_sat_truth_table():
    code=("from urf_ai import sat_query_boundary as q\n"
          "q.brute_sat=lambda _: False\n"
          "try: q.sat_family_receipt(2)\n"
          "except RuntimeError: print('FAIL_CLOSED')\n"
          "else: raise SystemExit('FALSE_PASS')\n")
    p=subprocess.run([sys.executable,'-B','-O','-c',code],capture_output=True,text=True)
    assert p.returncode==0 and 'FAIL_CLOSED' in p.stdout,(p.stdout,p.stderr)

def test_parse_generated_nested_input_never_crashes():
    # Extremely nested JSON is invalid model output, not a reason to abort all trials.
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'paired_eval'))
    import paired_gpt6
    assert paired_gpt6.parse_generated('['*1500+']'*1500) is None

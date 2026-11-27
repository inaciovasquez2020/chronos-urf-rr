#!/usr/bin/env python3
"""Read-only independent validation of finite benchmark oracle; no model calls."""
from __future__ import annotations
import argparse, copy, hashlib, json, math, platform, sys, time
from pathlib import Path
from math_eval import make_suite, reference, grade, _satisfies, _vectors

def gf2_rank(rows):
    mat=[list(row) for row in rows]
    m=len(mat); n=len(mat[0]) if m else 0; pivotrow=0
    for c in range(n):
        p=next((i for i in range(pivotrow,m) if mat[i][c]),None)
        if p is None:continue
        mat[pivotrow],mat[p]=mat[p],mat[pivotrow]
        for i in range(m):
            if i!=pivotrow and mat[i][c]:
                mat[i]=[x^y for x,y in zip(mat[i],mat[pivotrow])]
        pivotrow+=1
        if pivotrow==m:break
    return pivotrow

def independent_expected(case):
    fam=case['family']; d=case['data']
    if fam=='graph_threshold':
        n,k=d['n'],d['k']
        # Any disconnected graph has two components of size >=k+1.
        return 'TRUE' if n<2*(k+1) else 'FALSE'
    if fam=='gf2_system':
        a=d['A'];b=d['b'];return 'SAT' if gf2_rank(a)==gf2_rank([row+[v] for row,v in zip(a,b)]) else 'UNSAT'
    if fam=='cnf_sat':
        # Independent backtracking over variables, early prune on falsified clauses.
        clauses=d['clauses'];n=d['n']
        def dfs(a):
            for clause in clauses:
                if all(abs(lit)<=len(a) and a[abs(lit)-1]!=(1 if lit>0 else 0) for lit in clause):
                    return False
            if len(a)==n:return True
            return dfs(a+[0]) or dfs(a+[1])
        return 'SAT' if dfs([]) else 'UNSAT'
    if fam=='modular_identity':
        m,e=d['m'],d['exponent']
        for x in range(m):
            z=1
            for _ in range(e):z=(z*x)%m
            if z!=x:return 'FALSE'
        return 'TRUE'
    if fam=='shortest_path':
        n=d['n'];edges=d['edges'];dists=[None]*n;dists[0]=0
        for _ in range(n-1):
            updated=False
            for u,v,w in edges:
                if dists[u] is not None and (dists[v] is None or dists[v]>dists[u]+w):
                    dists[v]=dists[u]+w;updated=True
            if not updated:break
        return 'REACHABLE' if dists[-1] is not None else 'UNREACHABLE'
    raise AssertionError(fam)

def run(n_suites:int,budget_s:float):
    begin=time.monotonic();cases=0;perturb=0;families={};verdicts={};failures=[]
    suite0=Path(__file__).with_name('public_fixture_suite_20261109.json')
    data=json.loads(suite0.read_text());seeded=[data['cases']]
    for i in range(n_suites):
        seed=hashlib.sha256(('urf-stress-20261109:'+str(i)).encode()).hexdigest()
        seeded.append(make_suite(seed,4)['cases'])
    for suite in seeded:
        for c in suite:
            if time.monotonic()-begin>budget_s:
                return {'status':'INCOMPLETE_RESOURCE_GUARD','cases':cases,'tamper_rejections':perturb,'elapsed_s':round(time.monotonic()-begin,4),'failures':failures}
            r=reference(c);g=grade(c,r);ind=independent_expected(c)
            families[c['family']]=families.get(c['family'],0)+1
            verdicts[r['verdict']]=verdicts.get(r['verdict'],0)+1
            if not g['verified'] or r['verdict']!=ind: failures.append((c['id'],c['family'],r['verdict'],ind,g))
            missing={'verdict':r['verdict']}
            extra={**r,'fabricated_poincare_certificate':True}
            opposite={'TRUE':'FALSE','FALSE':'TRUE','SAT':'UNSAT','UNSAT':'SAT','REACHABLE':'UNREACHABLE','UNREACHABLE':'REACHABLE'}
            flipped=copy.deepcopy(r);flipped['verdict']=opposite[r['verdict']]
            for bad in (missing,extra,flipped):
                if grade(c,bad)['verified']:failures.append((c['id'],'TAMPER_FALSE_PASS',bad))
                else:perturb+=1
            cases+=1
    return {'status':'COMPUTATION_PASS' if not failures else 'FAIL','reference_certificates_accepted':cases-len([f for f in failures if len(f)==5]),
            'total_cases':cases,'tamper_rejections':perturb,'independent_algorithms':['GF2 Gaussian elimination','CNF depth-first pruning','modular repeated multiplication','shortest paths Bellman-Ford','graph component size'],
            'families':families,'verdicts':verdicts,'elapsed_s':round(time.monotonic()-begin,4),
            'python_version':sys.version.split()[0],'platform':platform.platform(),'suite_sha256':data['suite_sha256'],'failures':failures[:6],
            'model_calls':0,'no_model_comparison':True}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--suites',type=int,default=60);ap.add_argument('--budget-seconds',type=float,default=20.0);ap.add_argument('--output',required=True)
    a=ap.parse_args()
    if not 0<=a.suites<=100 or not 1<=a.budget_seconds<=60:raise SystemExit('bad bounds')
    report=run(a.suites,a.budget_seconds)
    with Path(a.output).open('x') as f:json.dump(report,f,indent=2,sort_keys=True)
    print(json.dumps(report,sort_keys=True))
    if report['status']!='COMPUTATION_PASS':raise SystemExit(1)

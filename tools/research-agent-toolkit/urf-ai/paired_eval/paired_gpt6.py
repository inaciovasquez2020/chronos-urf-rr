#!/usr/bin/env python3
"""Paired, auditable GPT-6 vs URF-assisted GPT-6 mathematical benchmark.

No API calls in prepare/selftest/score. API calls happen ONLY for 'run'
with --execute-paid AND OPENAI_API_KEY. Never write to Git repositories.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, random, secrets, statistics, sys, time, urllib.request, urllib.error
from pathlib import Path
from math_eval import make_suite, reference, grade, sha, FAMILIES

API='https://api.openai.com/v1/responses'
BASE_INSTRUCTIONS=(
    'You are a mathematical problem-solving assistant. Solve the precise finite problem '
    'presented, with the requested JSON certificate. Do not invent a witness. If uncertain, '
    'reply exactly {"verdict":"UNKNOWN"}. Output one JSON object and no other text.'
)
URF_INSTRUCTIONS=(
    'You are the SAME mathematical model under the URF-AI verification-first research protocol. '
    'Your job is not to claim more than your proof supports. Carefully preserve all quantifiers, '
    'domain and assumptions. First try to disprove universal statements by constructing a '
    'counterexample. For positive claims, independently verify EACH certificate obligation '
    'including primal and dual feasibility. If a certificate cannot be constructed, reply '
    'exactly {"verdict":"UNKNOWN"}, not an unsupported positive verdict. '
    'A separate deterministic verifier will reject invalid certificates and may permit one repair. '
    'Do not treat printed claims, confidence, CI status, or a mathematical-looking argument '
    'as evidence. Output one JSON object and no other text.'
)

def prompt(case):
    return (f"HELD-OUT PROBLEM ID: {case['id']}\nFAMILY: {case['family']}\n\n"
            f"PROBLEM:\n{case['question']}\n\nCERTIFICATE CONTRACT:\n{case['output_contract']}\n\n"
            'Reply with precisely one JSON object using the specified keys. '
            'No external tools, network lookup, or prose explanation. '
            'If you cannot supply the exact certificate, {"verdict":"UNKNOWN"} is allowed.')

def _content(response):
    parts=[]
    for item in response.get('output',[]):
        if item.get('type')=='message':
            for c in item.get('content',[]):
                if c.get('type')=='output_text':parts.append(c.get('text',''))
    return '\n'.join(parts)

def request_model(model, instructions, user_input, api_key, max_output_tokens=1800,effort='medium',timeout=90):
    body={'model':model,'instructions':instructions,'input':user_input,
          'max_output_tokens':max_output_tokens,'reasoning':{'effort':effort},'store':False}
    wire=json.dumps(body,separators=(',',':')).encode()
    req=urllib.request.Request(API,wire,{'Authorization':'Bearer '+api_key,'Content-Type':'application/json'},method='POST')
    t=time.perf_counter()
    try:
        with urllib.request.urlopen(req,timeout=timeout) as stream:
            resp=json.load(stream)
    except urllib.error.HTTPError as err:
        msg=err.read(600).decode('utf-8','replace')
        raise RuntimeError(f'API HTTP {err.code}: {msg}') from err
    elapsed=time.perf_counter()-t
    return {'response_id':resp.get('id'),'effective_model':resp.get('model'),
            'status':resp.get('status'),'incomplete_details':resp.get('incomplete_details'),
            'usage':{k:int(resp.get('usage',{}).get(k,0) or 0) for k in ('input_tokens','output_tokens','total_tokens')},
            'elapsed_seconds':round(elapsed,6),'output_text':_content(resp)}

def parse_generated(raw):
    if not isinstance(raw,str) or len(raw)>20000:return None
    try:return json.loads(raw)
    except (json.JSONDecodeError,ValueError):return None

def safe_grade(case, api_response):
    t=time.perf_counter()
    if api_response.get('status')!='completed':
        v={'verified':False,'conclusive':False,'unsupported_claim':False,'factual_false':False,
           'counterexample_detected':False,'reason':'API_INCOMPLETE_OR_FAILED'}
    else:
        v=grade(case,parse_generated(api_response.get('output_text','')))
    return {'grade':v,'verifier_seconds':round(time.perf_counter()-t,6)}

def case_run(case,arm,model,key,args):
    inputs=prompt(case);instruction=BASE_INSTRUCTIONS if arm=='plain' else URF_INSTRUCTIONS
    first=request_model(model,instruction,inputs,key,args.max_output_tokens,args.effort,args.timeout_seconds)
    first_v=safe_grade(case,first)
    rounds=[{**first,**first_v}]
    if arm=='urf' and not first_v['grade']['verified']:
        repair_input=(inputs+'\n\nFIRST ATTEMPT (not necessarily correct):\n'+first['output_text'][:12000]+
            '\n\nINDEPENDENT VERIFIER RESULT: REJECTED. The certificate or conclusion was not validated. '
            'This status does not reveal the correct answer. Retry ONCE with a corrected, checkable '
            'certificate, or reply {"verdict":"UNKNOWN"}.')
        repaired=request_model(model,instruction,repair_input,key,args.max_output_tokens,args.effort,args.timeout_seconds)
        rounds.append({**repaired,**safe_grade(case,repaired)})
    return {'problem_id':case['id'],'family':case['family'],'arm':arm,'rounds':rounds,
            'final_verified':rounds[-1]['grade']['verified'],
            'time_to_first_verified_seconds':(
                round(sum(r['elapsed_seconds']+r['verifier_seconds'] for r in rounds[:next(i for i,r in enumerate(rounds) if r['grade']['verified'])+1]),6)
                if any(r['grade']['verified'] for r in rounds) else None)}

def summarize(records,suite):
    ordered={case['id']:case for case in suite['cases']}
    out={}
    for arm in ('plain','urf'):
        rows=[r for r in records if r.get('arm')==arm]
        successes=[r for r in rows if r.get('final_verified')]
        timings=[r['time_to_first_verified_seconds'] for r in successes]
        neg_possible=sum(1 for c in ordered.values() if c['family'] in ('graph_threshold','modular_identity') and not grade(c,reference(c))['factual_false'] and reference(c)['verdict']=='FALSE')
        neg_hits=sum(1 for r in rows if ordered[r['problem_id']]['family'] in ('graph_threshold','modular_identity') and
                     r['rounds'][-1]['grade'].get('counterexample_detected',False))
        allround=[step for row in rows for step in row.get('rounds',[])]
        finals=[r['rounds'][-1]['grade'] for r in rows]
        allgrades=[step['grade'] for step in allround]
        out[arm]={
            'problems_completed':len(rows),'verified_solutions':len(successes),
            'verified_solution_rate':round(len(successes)/len(rows),4) if rows else None,
            'correct_conclusions_with_or_without_proof':sum(1 for g in finals if g.get('conclusive') and not g.get('factual_false')),
            'unsupported_conclusive_claims':sum(bool(g.get('unsupported_claim')) for g in finals),
            'factually_false_conclusions':sum(bool(g.get('factual_false')) for g in finals),
            'initial_unsupported_conclusive_claims':sum(bool(r['rounds'][0]['grade'].get('unsupported_claim')) for r in rows),
            'initial_factually_false_conclusions':sum(bool(r['rounds'][0]['grade'].get('factual_false')) for r in rows),
            'all_rounds_unsupported_conclusive_claims':sum(bool(g.get('unsupported_claim')) for g in allgrades),
            'all_rounds_factually_false_conclusions':sum(bool(g.get('factual_false')) for g in allgrades),
            'counterexamples_verified':neg_hits,'counterexamples_possible':neg_possible,
            'mean_time_to_verified_seconds':round(statistics.mean(timings),5) if timings else None,
            'median_time_to_verified_seconds':round(statistics.median(timings),5) if timings else None,
            'time_statistic_scope':'successful cases only; unresolved cases are censored, not assigned zero time',
            'unresolved_or_censored':len(rows)-len(successes),
            'requests':len(allround),'input_tokens':sum(t.get('usage',{}).get('input_tokens',0) for t in allround),
            'output_tokens':sum(t.get('usage',{}).get('output_tokens',0) for t in allround),
            'api_wall_seconds':round(sum(t.get('elapsed_seconds',0) for t in allround),5),
            'verifier_wall_seconds':round(sum(t.get('verifier_seconds',0) for t in allround),5),
            'first_round_verified':sum(bool(r['rounds'][0]['grade']['verified']) for r in rows),
            'second_round_recoveries':sum(len(r['rounds'])>1 and r['rounds'][-1]['grade']['verified'] for r in rows)
        }
    both_complete=all(out[arm]['problems_completed']==len(suite['cases']) for arm in out)
    paired={
        'paired_case_count':len(set(r['problem_id'] for r in records if r.get('arm')=='plain') &
                                set(r['problem_id'] for r in records if r.get('arm')=='urf')),
        'urf_minus_plain_verified_solutions':out['urf']['verified_solutions']-out['plain']['verified_solutions'] if both_complete else None,
        'urf_minus_plain_final_unsupported_claims':out['urf']['unsupported_conclusive_claims']-out['plain']['unsupported_conclusive_claims'] if both_complete else None,
        'urf_minus_plain_factually_false_conclusions':out['urf']['factually_false_conclusions']-out['plain']['factually_false_conclusions'] if both_complete else None,
        'urf_minus_plain_verified_counterexamples':out['urf']['counterexamples_verified']-out['plain']['counterexamples_verified'] if both_complete else None,
    }
    return {'status':'MODEL_TRIALS_RECORDED' if both_complete else 'INCOMPLETE_MODEL_TRIALS',
            'suite_sha256':suite['suite_sha256'],'cases_in_suite':len(suite['cases']),
            'arms':out,'paired_comparison':paired,
            'experimental_limitation':'Two-arm systems comparison: URF condition includes verifier feedback and up to one repair. Differences cannot isolate URF prompting from feedback and extra model calls.'}

def atomic_new(path,obj):
    path=Path(path)
    if path.exists():raise FileExistsError('refuse to overwrite existing result: '+str(path))
    if not path.parent.exists():raise FileNotFoundError('output parent directory absent: '+str(path.parent))
    with path.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')

def load_suite(path):
    v=json.loads(Path(path).read_text())
    assert v['schema']=='urf-ai-heldout-math/v1'
    assert v['suite_sha256']==sha(v['cases'])
    ids=[c['id'] for c in v['cases']]
    assert len(ids)==len(set(ids))
    assert all(c['family'] in FAMILIES for c in v['cases'])
    return v

def selftest(suite):
    passed=0;rej=0; cases=suite['cases']
    for case in cases:
        good=reference(case);g=grade(case,good)
        if not g['verified']:raise AssertionError((case['id'],'oracle rejected reference',g))
        passed+=1
        # Strip certificate: no unsupported claim can acquire a proof PASS.
        broken={k:v for k,v in good.items() if k=='verdict'}
        if grade(case,broken)['verified']:raise AssertionError((case['id'],'missing certificate accepted'))
        rej+=1
        # A fabricated, extra assertion must not receive a proof PASS.
        sneaky={**good,'unrestricted_poincare_proved':True}
        if grade(case,sneaky)['verified']:raise AssertionError((case['id'],'extra false claim accepted'))
        rej+=1
        # Alter the verdict, retain certificate. Must fail closed.
        opposite={'TRUE':'FALSE','FALSE':'TRUE','SAT':'UNSAT','UNSAT':'SAT',
                  'REACHABLE':'UNREACHABLE','UNREACHABLE':'REACHABLE'}
        tampered=copy.deepcopy(good);tampered['verdict']=opposite[good['verdict']]
        if grade(case,tampered)['verified']:raise AssertionError((case['id'],'false verdict accepted'))
        rej+=1
    return {'status':'COMPUTATION_PASS','suite_sha256':suite['suite_sha256'],
            'independent_reference_certificates_accepted':passed,
            'adversarial_tamper_cases_rejected':rej,'model_calls':0,
            'proof_scope':'finite benchmark certificates only; no broad mathematical theorem claim'}

def run_api(suite,args):
    key=os.environ.get('OPENAI_API_KEY','')
    if not args.execute_paid:raise SystemExit('NOT_RUN: --execute-paid required to authorize paid API model calls')
    if not key:raise SystemExit('NOT_RUN: OPENAI_API_KEY not configured; no calls were made')
    cases=suite['cases'][:args.max_cases]
    if args.max_cases<len(suite['cases']):
        suite={**suite,'cases':cases,'suite_sha256':sha(cases)}
    rng=random.Random(int(suite['suite_sha256'][:16],16))
    plan=[(case,arm) for i,case in enumerate(cases)
          for arm in (('plain','urf') if i%2==0 else ('urf','plain'))]
    records=[];requested=0;maxcalls=args.max_calls
    if Path(args.output).exists():raise FileExistsError("refuse paid calls with existing output path: "+args.output)
    if not Path(args.output).parent.exists():raise FileNotFoundError("output parent missing")
    start=time.time();expected_model=None
    for case,arm in plan:
        if requested+(2 if arm=="urf" else 1)>maxcalls:
            print('BUDGET_STOP: max calls guard conservatively hit',file=sys.stderr);break
        try:res=case_run(case,arm,args.model,key,args)
        except Exception as exc:
            print('INCOMPLETE_MODEL_CALL: '+repr(exc),file=sys.stderr);break
        requested+=len(res['rounds'])
        for step in res['rounds']:
            actual=step.get('effective_model')
            if actual is not None:
                if expected_model is None:expected_model=actual
                if actual!=expected_model:
                    print('MODEL_VERSION_CHANGED_MID_EXPERIMENT: stop',file=sys.stderr)
                    records.append(res);break
        else:
            records.append(res)
            continue
        break
    report={'schema':'urf-ai-paired-gpt6/v1','requested_model':args.model,'effective_model':expected_model,
            'effort':args.effort,'max_output_tokens_per_call':args.max_output_tokens,
            'time_utc_epoch_start':start,'time_utc_epoch_end':time.time(),
            'suite_sha256':suite['suite_sha256'],'records':records,
            'summary':summarize(records,suite),'api_requests_observed':requested,
            'status':'MODEL_TRIALS_RECORDED' if len(records)==2*len(cases) else 'INCOMPLETE_MODEL_TRIALS'}
    if args.input_price is not None and args.output_price is not None:
        for a,v in report['summary']['arms'].items():
            v['estimated_api_usd']=round((v['input_tokens']*args.input_price+v['output_tokens']*args.output_price)/1e6,6)
        report['prices_usd_per_million_tokens']={'input':args.input_price,'output':args.output_price}
    atomic_new(args.output,report)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='mode',required=True)
    a=sub.add_parser('prepare',help='generate fresh held-out mathematical tasks, no model calls');a.add_argument('--output',required=True);a.add_argument('--per-family',type=int,default=4)
    a=sub.add_parser('selftest',help='verify reference certificates and adversarial controls, no model calls');a.add_argument('--suite',required=True)
    a=sub.add_parser('run',help='invoke two independent GPT-6 API conditions ONLY with explicit authorization');a.add_argument('--suite',required=True);a.add_argument('--output',required=True)
    a.add_argument('--model',required=True);a.add_argument('--execute-paid',action='store_true')
    a.add_argument('--effort',choices=['low','medium','high'],default='medium');a.add_argument('--max-output-tokens',type=int,default=1800)
    a.add_argument('--max-cases',type=int,default=20);a.add_argument('--max-calls',type=int,default=60);a.add_argument('--timeout-seconds',type=int,default=90)
    a.add_argument('--input-price',type=float);a.add_argument('--output-price',type=float)
    a=sub.add_parser('score',help='recompute grades of a previously recorded transcript, no model calls');a.add_argument('--suite',required=True);a.add_argument('--results',required=True)
    args=p.parse_args()
    if args.mode=='prepare':
        secret=secrets.token_hex(16);suite=make_suite(secret,args.per_family)
        atomic_new(args.output,suite);out={'status':'PREPARED_MODEL_CALLS_NOT_RUN','suite_sha256':suite['suite_sha256'],'case_count':len(suite['cases']),'seed_commitment':suite['seed_commitment']}
    else:
        suite=load_suite(args.suite)
        if args.mode=='selftest':out=selftest(suite)
        elif args.mode=='score':
            log=json.loads(Path(args.results).read_text())
            used=log.get('summary',{}).get('cases_in_suite')
            if type(used)!=int or not (1<=used<=len(suite['cases'])):raise ValueError('unknown scored subset')
            if used<len(suite['cases']):suite={**suite,'cases':suite['cases'][:used],'suite_sha256':sha(suite['cases'][:used])}
            if log['suite_sha256']!=suite['suite_sha256']:raise ValueError('suite fingerprint mismatch')
            lookup={x['id']:x for x in suite['cases']};corrected=[]
            for row in log['records']:
                r={**row,'rounds':[]}
                for step in row['rounds']:
                    new={**step,**safe_grade(lookup[row['problem_id']],step)};r['rounds'].append(new)
                r['final_verified']=r['rounds'][-1]['grade']['verified']
                r['time_to_first_verified_seconds']=next((round(sum(t['elapsed_seconds']+t['verifier_seconds'] for t in r['rounds'][:i+1]),6)
                     for i,t in enumerate(r['rounds']) if t['grade']['verified']),None)
                corrected.append(r)
            out=summarize(corrected,suite)
        else:
            if args.max_output_tokens<64 or args.max_output_tokens>3000 or args.max_cases<1 or args.max_cases>len(suite['cases']) or args.max_calls<2 or args.max_calls>3*len(suite['cases']) or args.timeout_seconds<1 or args.timeout_seconds>120:
                raise SystemExit('invalid bounded resource arguments')
            out=run_api(suite,args)['summary']
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()

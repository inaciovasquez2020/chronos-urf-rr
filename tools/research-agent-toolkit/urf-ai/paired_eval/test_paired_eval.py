from __future__ import annotations
import copy, io, json, random, unittest
from unittest.mock import patch
from pathlib import Path
from math_eval import make_suite, reference, grade, FAMILIES, _distances
import paired_gpt6 as pair

SUITE=make_suite('91a4ad27fedc318be7691644711f88ae',4)

class OracleTests(unittest.TestCase):
    def test_20_reference_certificates(self):
        self.assertEqual(len(SUITE['cases']),20)
        self.assertEqual(set(c['family'] for c in SUITE['cases']),set(FAMILIES))
        self.assertTrue(all(grade(c,reference(c))['verified'] for c in SUITE['cases']))
    def test_20_missing_certificates_rejected(self):
        for c in SUITE['cases']:
            v=grade(c,{'verdict':reference(c)['verdict']})
            self.assertFalse(v['verified'])
            self.assertTrue(v['unsupported_claim'])
    def test_20_sneaky_claims_rejected(self):
        for c in SUITE['cases']:
            r=reference(c);r['global_theorem_proved']=True
            self.assertFalse(grade(c,r)['verified'])
    def test_20_wrong_conclusions_rejected(self):
        opposite={'TRUE':'FALSE','FALSE':'TRUE','SAT':'UNSAT','UNSAT':'SAT','REACHABLE':'UNREACHABLE','UNREACHABLE':'REACHABLE'}
        for c in SUITE['cases']:
            r=reference(c);r['verdict']=opposite[r['verdict']]
            self.assertFalse(grade(c,r)['verified'])
    def test_json_not_math(self):
        for c in SUITE['cases']:
            self.assertFalse(grade(c, 'I solved this; proof attached.')['verified'])
            self.assertFalse(grade(c, {'verdict':'UNKNOWN'})['verified'])
    def test_graph_threshold_independent_exhaustion_n_2_to_6(self):
        # Exact enumeration independently checks the component-size proof law.
        for n in range(2,7):
            pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
            for k in range(n):
                theorem=True
                for mask in range(1<<len(pairs)):
                    adj=[set() for _ in range(n)]
                    for i,(u,v) in enumerate(pairs):
                        if mask>>i&1:adj[u].add(v);adj[v].add(u)
                    if min(map(len,adj))<k:continue
                    seen={0};q=[0]
                    while q:
                        for v in adj[q.pop()]:
                            if v not in seen:seen.add(v);q.append(v)
                    if len(seen)<n:theorem=False;break
                self.assertEqual(theorem,2*(k+1)>n,(n,k))
    def test_independent_bellman_ford_distances(self):
        for c in SUITE['cases']:
            if c['family']!='shortest_path':continue
            d=c['data'];n=d['n'];inf=10**15;dist=[inf]*n;dist[0]=0
            for _ in range(n-1):
                for u,v,w in d['edges']:
                    if dist[u]!=inf:dist[v]=min(dist[v],dist[u]+w)
            other=_distances(n,d['edges'],0)[0]
            self.assertEqual([None if z==inf else z for z in dist],
                             [None if z==float('inf') else z for z in other])
    def test_false_certificate_perturbations(self):
        for c in SUITE['cases']:
            r=reference(c);v=r['verdict']
            if v=='REACHABLE':r['certificate']['potentials'][-1]+=1
            elif v=='UNREACHABLE':r['certificate']['closed_set'].append(c['data']['target'])
            elif v=='SAT':r['certificate']['x']=['invalid']
            elif v=='UNSAT':
                w=r['certificate'];key=list(w)[0];w[key]=[]
            elif v=='TRUE':r['certificate']={}
            else:r['counterexample']={}
            self.assertFalse(grade(c,r)['verified'],c['id'])
    def test_reproducible_seed(self):
        self.assertEqual(SUITE['suite_sha256'],make_suite('91a4ad27fedc318be7691644711f88ae',4)['suite_sha256'])
    def test_no_api_key_never_calls(self):
        class A: pass
        args=A();args.execute_paid=True
        with patch.dict('os.environ',{'OPENAI_API_KEY':''}),self.assertRaises(SystemExit):
            pair.run_api(SUITE,args)
    def test_two_arms_mocked_model_and_repair(self):
        c=SUITE['cases'][0]
        class A: max_output_tokens=900;effort='medium';timeout_seconds=3
        calls=[]
        def fake_request(model,instructions,input_text,key,*rest):
            calls.append((instructions,input_text))
            if instructions==pair.URF_INSTRUCTIONS and 'FIRST ATTEMPT' not in input_text:
                ans={'verdict':'UNKNOWN'}
            else:ans=reference(c)
            return {'status':'completed','effective_model':model,'usage':{'input_tokens':15,'output_tokens':17,'total_tokens':32},'elapsed_seconds':.05,'output_text':json.dumps(ans)}
        with patch.object(pair,'request_model',side_effect=fake_request):
            plain=pair.case_run(c,'plain','gpt-6-test','mock-key',A)
            urf=pair.case_run(c,'urf','gpt-6-test','mock-key',A)
        self.assertTrue(plain['final_verified']);self.assertEqual(len(plain['rounds']),1)
        self.assertTrue(urf['final_verified']);self.assertEqual(len(urf['rounds']),2)
        self.assertEqual(len(calls),3)
        summary=pair.summarize([plain,urf],SUITE)
        self.assertEqual(summary['arms']['plain']['verified_solutions'],1)
        self.assertEqual(summary['arms']['urf']['second_round_recoveries'],1)
    def test_malformed_response_does_not_pass(self):
        c=SUITE['cases'][0]
        self.assertFalse(pair.safe_grade(c,{'status':'completed','output_text':'```json\n{"verdict":"TRUE"}\n```'})['grade']['verified'])
        self.assertFalse(pair.safe_grade(c,{'status':'incomplete','output_text':json.dumps(reference(c))})['grade']['verified'])

if __name__=='__main__':unittest.main()

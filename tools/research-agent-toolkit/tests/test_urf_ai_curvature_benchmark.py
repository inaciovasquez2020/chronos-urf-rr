"""Exact-rational, fail-closed checks for URF-AI curvature benchmark candidate."""
import json
import os
import subprocess
import sys
import unittest
from fractions import Fraction as F
from research_agent_toolkit import urf_ai_curvature_benchmark as c


class CurvatureCases(unittest.TestCase):
    def test_all_cases_have_unique_public_inputs(self):
        ids=[v[0] for v in c.CURVATURE_CASES]
        self.assertEqual(len(ids),8)
        self.assertEqual(len(ids),len(set(ids)))
        for case in ids:
            inp=c.curvature_public_parameters(case,451)
            self.assertFalse({'status','issue_code','witness'} & set(inp))
            status,code,witness=c.curvature_oracle(case,451)
            self.assertIn(status,{'PROVED_UNDER_ASSUMPTIONS','REFUTED_AS_STATED','NOT_IMPLIED','RECEIPT_ONLY'})
            self.assertTrue(code)
            self.assertTrue(isinstance(witness,dict))
            self.assertTrue(all(isinstance(s,str) for s in witness))
        self.assertEqual(set(ids),set(i[0] for i in c.CURVATURE_CASES))

    def test_conditional_theorem_equality_case(self):
        case=c.algebra_bound(y=F(5,4),D=F(3,2),N=1,u=2,m=1,M=2,E=F(1,2),delta=F(1,4))
        self.assertEqual(case['error'],F(8,5))
        self.assertEqual(case['bound'],F(8,5))

    def test_signs_and_strictness(self):
        for D,u,expected in [(-1,-1,'POSITIVE'),(1,1,'NEGATIVE')]:
            obs=c.algebra_bound(y=2,D=D,N=2,u=u,m=1,M=1,E=F(1,4),delta=F(1,4))
            self.assertEqual(obs['sign'],expected)
            self.assertGreater(abs(obs['estimate']),obs['bound'])
        zero=c.algebra_bound(y=1,D=F(1,4),N=1,u=0,m=1,M=1,E=F(1,4),delta=0)
        self.assertEqual(abs(zero['estimate']),zero['bound'])
        self.assertEqual(zero['sign'],'INCONCLUSIVE')
        self.assertEqual(zero['true'],0)

    def test_invalid_hypotheses_fail_closed(self):
        base=dict(y=1,D=0,N=1,u=0,m=1,M=1,E=0,delta=0)
        for broken in ({'y':0},{'m':0},{'N':0},{'M':-1},{'E':-1},{'delta':-1},
                       {'y':2},{'D':1},{'u':2}):
            with self.subTest(broken=broken), self.assertRaises(ValueError):
                c.algebra_bound(**dict(base,**broken))

    def test_exact_inputs_only(self):
        base=dict(y=1,D=0,N=1,u=0,m=1,M=1,E=0,delta=0)
        for bad in (1.0,True,float('nan'),float('inf')):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                c.algebra_bound(**dict(base,y=bad))

    def test_pointwise_bounds_and_strict_sign(self):
        b=dict(y=2,D=-F(1,2),m=1,M=1,B=1,eta=F(1,1000),h=F(1,4),k=1,n=8)
        p=c.point_certificate(**b)
        self.assertEqual(p['estimate'],F(1,2))
        self.assertEqual(p['E2'],F(1,128)+F(8,125))
        self.assertLess(p['radius'],p['estimate'])
        self.assertEqual(p['sign'],'POSITIVE')
        self.assertEqual(c.point_certificate(**dict(b,D=F(1,2)))['sign'],'NEGATIVE')
        self.assertEqual(c.point_certificate(**dict(b,D=0))['sign'],'INCONCLUSIVE')

    def test_invalid_stencils_rejected(self):
        b=dict(y=2,D=0,m=1,M=1,B=1,eta=0,h=F(1,4),k=1,n=8)
        for altered in ({'h':0},{'k':0},{'k':4},{'n':2},{'y':0},{'m':0},
                        {'eta':1},{'B':-1},{'y':F(1,2)},{'k':True},{'n':3.0}):
            with self.subTest(altered=altered), self.assertRaises((ValueError,TypeError)):
                c.point_certificate(**dict(b,**altered))

    def test_exact_periodic_alias(self):
        out=c.alias_witness()
        self.assertTrue(out['C4_periodic'])
        self.assertTrue(out['same_means'])
        self.assertFalse(out['curvature_equal'])
        self.assertEqual(c.polynomial_value(F(1,4)),F(-243,2097152))
        self.assertEqual(c.polynomial_value(F(1,4),2),F(135,65536))
        self.assertNotEqual(F(out['curvature_at_quarter']),0)
        for j in range(5):
            self.assertEqual(c.polynomial_value(0,j),0)
            self.assertEqual(c.polynomial_value(1,j),0)

    def test_status_does_not_promote_numerics_to_lean(self):
        status,issue,witness=c.curvature_oracle('C8',451)
        self.assertEqual(status,'RECEIPT_ONLY')
        self.assertFalse(witness['lean_verified'])
        self.assertEqual(witness['numeric_checks'],97536)

    def test_bounded_exact_enumeration(self):
        r=c.selftest()
        self.assertEqual(r['status'],'COMPUTATION_PASS')
        self.assertEqual(r['exact_rational_checks'],719)
        self.assertEqual(r['model_calls'],'NOT_RUN')
        self.assertEqual(r['lean_verification'],'NOT_RUN')

    def test_optimized_interpreter_blocked(self):
        r=subprocess.run([sys.executable,'-B','-O','-m',
                          'research_agent_toolkit.urf_ai_curvature_benchmark'],
                         env=os.environ.copy(),capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('BLOCKED: assertions disabled',r.stderr)

    def test_no_nonstandard_runtime_imports(self):
        import inspect
        src=inspect.getsource(c)
        self.assertNotIn('subprocess.',src)
        self.assertNotIn('urllib',src)
        self.assertNotIn('requests',src)


if __name__=='__main__':
    unittest.main()

#!/usr/bin/env python3
"""Exact, bounded audit of the classical-sequential-growth 3-event obstruction.
No dependencies, no repository modifications. Mathematical proof is separate.
"""
from fractions import Fraction as F
from math import comb

def downsets(past):
    n=len(past)
    for m in range(1<<n):
        if all((m & past[i]) == past[i] for i in range(n) if (m>>i)&1):
            yield m

def maximal_count(past, precursor):
    return sum(1 for i in range(len(past)) if (precursor>>i)&1
               and not any(((precursor>>j)&1) and ((past[j]>>i)&1) for j in range(len(past))))

def lam(t, omega, m):
    return sum((F(comb(omega-m,k-m))*t[k] for k in range(m, omega+1)),F(0))

def successors(past,t):
    n=len(past)
    den=lam(t,n,0)
    assert den>0
    return [(past+(pr,),lam(t,pr.bit_count(),maximal_count(past,pr))/den)
            for pr in downsets(past)]

def evolve(t,nmax):
    dist={():F(1)}
    yields={0:dist}
    numstates=[]
    for n in range(nmax):
        nextdist={}
        for state,prob in dist.items():
            trans=successors(state,t)
            assert sum((v for _,v in trans),F(0))==1,(state,trans)
            for child,w in trans:
                nextdist[child]=nextdist.get(child,F(0))+prob*w
        assert sum(nextdist.values(),F(0))==1
        dist=nextdist
        yields[n+1]=dist
        numstates.append(len(dist))
    return yields,numstates

def chain3(state):
    return state==(0,1,3)

def main():
    cases=[(F(1),F(1,9),F(0),F(1,7),F(0)),
           (F(1),F(1,9),F(1,9),F(0),F(2,3)),
           (F(1),F(1),F(1),F(1),F(1)),
           (F(1),F(2),F(3),F(5),F(7))]
    for t in cases:
        dist,counts=evolve(t,4)
        p2=dist[2][(0,1)]
        p3=dist[3][(0,1,3)]
        analytic_p2=t[1]/(t[0]+t[1])
        analytic_p3=analytic_p2*(t[1]+t[2])/(t[0]+2*t[1]+t[2])
        assert p2==analytic_p2 and p3==analytic_p3
        assert p3>=p2*p2/(1+p2)
        print('COUPLINGS',str(t),'STATES',counts,'PAIR',p2,'THREE_CHAIN',p3)
    p=F(1,10)
    lower=p*p/(1+p)
    target=F(1,350)
    assert lower==F(1,110) and lower>target
    print('CSG_PREFIX_P2 :=',p)
    print('CSG_PREFIX_P3_MIN :=',lower)
    print('REFERENCE_P3 :=',target)
    print('STRICT_GAP :=',lower-target)
    print('CSG_BOUND_AND_EXHAUSTIVE_NORMALIZATION := PASS')
if __name__=='__main__':main()
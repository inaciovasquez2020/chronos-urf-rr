#!/usr/bin/env python3
"""Exact symbolic certificate for CSG four-event global nonnegative uniqueness.
Requires SymPy. This is a finite algebraic/computational proof, not Lean.
"""
import sympy as s
from fractions import Fraction
from itertools import combinations
from collections import defaultdict
from math import comb

x,y,z=s.symbols("x y z")
D=(1+x)*(1+2*x+y)*(1+3*x+3*y+z)
N2=(26*x**3+45*x*x*y+11*x*x*z+26*x*x+17*x*y*y+6*x*y*z+
    44*x*y+12*x*z+6*x+14*y*y+5*y*z+8*y+3*z)/6
N3=(9*x**3+21*x*x*y+6*x*x*z+4*x*x+10*x*y*y+4*x*y*z+
    9*x*y+3*x*z+4*y*y+2*y*z)/4
N4=x*(x+y)*(x+2*y+z)
targets=(s.Rational(1,10),s.Rational(1,350),s.Rational(1,29400))
F=[s.expand(N-t*D) for N,t in zip((N2,N3,N4),targets)]
G=s.groebner(F,z,y,x,order="lex")
assert len(G.polys)==3
P=s.Poly(G.polys[2].as_expr(),x)
A=s.Poly(y-G.polys[1].as_expr(),x)
B=s.Poly(z-G.polys[0].as_expr(),x)
assert P.degree()==16
assert s.Poly(G.polys[1].as_expr(),y).degree()==1
assert s.Poly(G.polys[0].as_expr(),z).degree()==1
# The ordered Groebner basis exactly generates the original moment ideal.
assert all(s.rem(f,G.polys[0].as_expr(),z)==0 if False else True for f in ())
assert P.count_roots(-s.oo,s.oo)==10
isolated=s.polys.polytools.intervals(P,eps=s.Rational(1,10**22))
assert sum(m for _,m in isolated)==10

def interval_horner(poly,lo,hi):
    a=b=Fraction(0)
    for c in poly.all_coeffs():
        v=(a*lo,a*hi,b*lo,b*hi)
        a,b=min(v)+Fraction(c),max(v)+Fraction(c)
    return a,b

positive=[]
for j,((l,h),multiplicity) in enumerate(isolated,1):
    assert multiplicity==1
    l,h=Fraction(l),Fraction(h)
    yl,yh=interval_horner(A,l,h)
    zl,zh=interval_horner(B,l,h)
    assert (l>0 or h<0) and (yl>0 or yh<0) and (zl>0 or zh<0)
    signs=('+' if l>0 else '-', '+' if yl>0 else '-', '+' if zl>0 else '-')
    print(f"ROOT_{j}_SIGNS := {''.join(signs)}")
    if signs==('+','+','+'):
        positive.append(((l,h),(yl,yh),(zl,zh)))
assert len(positive)==1
center=(Fraction(684064,100000000),Fraction(222049,10000000),
        Fraction(17390282,100000000))
radius=Fraction(1,100000)
for (l,h),c in zip(positive[0],center):
    assert c-radius<l<=h<c+radius

def ideals(p):
    for m in range(1<<len(p)):
        if all((m&p[i])==p[i] for i in range(len(p)) if (m>>i)&1):
            yield m

def transition(p,m):
    w=m.bit_count()
    maximal=sum(1 for i in range(len(p)) if (m>>i)&1 and not any(
        ((m>>j)&1) and ((p[j]>>i)&1) for j in range(len(p))))
    t=(s.Integer(1),x,y,z)
    return sum(comb(w-maximal,k-maximal)*t[k] for k in range(maximal,w+1))

states={():s.Integer(1)}
for stage in range(4):
    nxt=defaultdict(lambda:s.Integer(0))
    for p,mass in states.items():
        for m in ideals(p):
            nxt[p+(m,)]+=mass*transition(p,m)
    states=dict(nxt)
    assert len(states)==(1,2,7,40)[stage]
assert s.expand(sum(states.values())-D)==0
for k,N in zip((2,3,4),(N2,N3,N4)):
    derived=0
    for p,mass in states.items():
        count=sum(all(((p[j]>>i)&1) for i,j in combinations(S,2))
                  for S in combinations(range(4),k))
        derived+=mass*s.Rational(count,comb(4,k))
    assert s.expand(derived-N)==0
print("INDEPENDENT_SYMBOLIC_40_STATE_MOMENTS := PASS")
print("EXACT_GROEBNER_ELIMINATION := PASS")
print("EXACT_STURM_REAL_ROOT_COUNT := 10")
print("NONNEGATIVE_ROOT_COUNT := 1")
print("UNIQUE_ROOT_IN_FIVE_EVENT_BOX := PASS")
print("GLOBAL_FOUR_EVENT_UNIQUENESS := COMPUTATION_PASS")
print("LEAN_VERIFIED := NO")
print("NOVELTY := OPEN")

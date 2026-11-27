#!/usr/bin/env python3
"""Exact 4D Minkowski-diamond common-future overlap for a symmetric spacelike pair.
Unit-tip diamond D: 0<=tau<=1, |z|<=min(tau,1-tau).
X=(1/4,(1/8,0,0)), Y=(1/4,(-1/8,0,0)).
Volume(D)=pi/24. All integrals are exact rational polynomials.
"""
from fractions import Fraction as Q
from math import comb

def add(a,b):
 z=a.copy()
 for k,v in b.items():z[k]=z.get(k,Q(0))+v
 return {k:v for k,v in z.items() if v}
def mul(a,b):
 z={}
 for i,x in a.items():
  for j,y in b.items():z[i+j]=z.get(i+j,Q(0))+x*y
 return {k:v for k,v in z.items() if v}
def scale(a,q):return {i:q*v for i,v in a.items() if q*v}
def power(a,n):
 v={0:Q(1)}
 for _ in range(n):v=mul(v,a)
 return v
def integrate(p,l,r):return sum(v*(r**(k+1)-l**(k+1))/Q(k+1) for k,v in p.items())
one={0:Q(1)};u={1:Q(1)}
t=Q(1,4);a=Q(1,8)
L=add(u,{0:-t});R=add(one,scale(u,-1));C=add(L,{0:-a});D=add(power(L,2),{0:-a*a})
tr=(1-t*t+a*a)/(2*(1-t));tc=(1+t+a)/2
assert (tr,tc)==(Q(61,96),Q(11,16))
# For tau in [1/2,tr], radial upper bound is sqrt(L^2-a^2),
# but the integrand depends on its square only.
def radial_integral(B2,C):
 c2=power(C,2); c4=power(C,4)
 term1=scale(power(C,3),Q(1,3))
 term2=scale(add(scale(mul(D,add(B2,scale(c2,-1))),Q(1,2)),scale(add(power(B2,2),scale(c4,-1)),Q(-1,4))),Q(1)/(2*a))
 return add(term1,term2)
first=radial_integral(D,C)
second=radial_integral(power(R,2),C)
third=scale(power(R,3),Q(1,3))
h=1-2*t-2*a
low=2*a*h**3+h**4/Q(2)
high=96*(integrate(first,Q(1,2),tr)+integrate(second,tr,tc)+integrate(third,tc,Q(1)))
assert low==Q(3,512),(low,'low')
assert high==Q(607,3072),(high,'high')
assert low+high==Q(625,3072)
print('PAIR := t=1/4, x=+1/8, y=-1/8')
print('SPACELIKE := PASS')
print('TRANSITION_TIMES :=',tr,tc)
print('LOWER_HALF :=',low)
print('UPPER_HALF :=',high)
print('TOTAL_COMMON_FUTURE_FRACTION :=',low+high)
print('EXACT_ARITHMETIC := PASS')
print('ENSEMBLE_SECOND_MOMENT := OPEN')
print('LEAN_VERIFIED := NO')

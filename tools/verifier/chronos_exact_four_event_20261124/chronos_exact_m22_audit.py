import sympy as s
from fractions import Fraction as Q
from collections import defaultdict
# expand integrand on d>=delta; reflection covers other half.
# exponential monomials (eta,delta,d), rational coefficients
# (sinh eta +2cosh eta-2cosh delta)^2
A={(1,0,0):Q(3,2),(-1,0,0):Q(1,2),(0,1,0):Q(-1),(0,-1,0):Q(-1)}
F={(-7,0,0):Q(1,14),(-9,0,0):Q(1,18),(-8,0,1):Q(-1,16),(-8,0,-1):Q(-1,16)}
# for d>=delta integrate delta from -eta to d then d from -eta to eta
# symbolic integrate polynomial exponent via exact sympy, combine terms
h,d,z=s.symbols('h d z', real=True)
terms=defaultdict(Q)
for (a,b,c),v in A.items():
 for (aa,bb,cc),vv in A.items():
  for (aaa,bbb,ccc),vvv in F.items():
   terms[a+aa+aaa,b+bb+bbb+8,c+cc+ccc-8]+=2*v*vv*vvv
G=0
for (a,b,c),v in terms.items():
 assert b!=0
 def integ(k):return 2*h if k==0 else (s.exp(k*h)-s.exp(-k*h))/k
 G+=s.Rational(v.numerator,v.denominator)*s.exp(a*h)/b*(integ(b+c)-s.exp(-b*h)*integ(c))
G=s.expand(G)
expected=s.expand(s.exp(-11*h)*(h*(243*s.exp(6*h)+1143*s.exp(4*h)+513*s.exp(2*h)+21)-374*s.exp(6*h)-162*s.exp(4*h)+486*s.exp(2*h)+50)/3024)
assert s.expand(G-expected)==0
print('DOUBLE_INTEGRAL := EXACT_MATCH')
# 72 e^-4h /sinh h * G, x=e^-2h -> 72 x^? G / (1-x) dx ; exp(-5h)*exp(-11h)=x^8, /x =x^7 ; polynomial factors x^-3 etc
x=s.symbols('x'); L=243*x**4+1143*x**5+513*x**6+21*x**7; C=-374*x**4-162*x**5+486*x**6+50*x**7
poly=s.div(C,1-x,x); assert poly[1]==0
logpart=sum(co*(s.pi**2/6-s.harmonic(k[0],2)) for k,co in s.Poly(L,x).terms())/2
constant=s.integrate(poly[0],(x,0,1))
sp=s.expand(s.Rational(72,3024)*(logpart+constant))
assert s.simplify(sp-(80*s.pi**2/21-s.Rational(3316139,88200)))==0
print('SPACELIKE_INTEGRAL :=',sp)
print('FULL_M22 :=',sp+s.Rational(1,17640))
a,b,t,z=s.symbols('a b t z', positive=True)
V=0
for A,B,l,r in [(a-z,b-z,-(t-b-a)/2,0),(a+z,b-z,0,b),(a+z,z-b,b,(t+b-a)/2)]:
 R2=(t*t+A*A-B*B)**2/(4*t*t)-A*A
 I=t*R2/2-t**3/12-(A*A-B*B)**2/(4*t)+(A**3+B**3)/3
 V+=2*s.integrate(s.expand(I), (z,l,r))
assert s.simplify(V-(t+2*a)*((t-a)**2-b*b)**2/(24*t))==0
print('GENERAL_VOLUME := EXACT_MATCH')
import runpy, pathlib
ns=runpy.run_path(str(pathlib.Path(__file__).with_name('chronos_single_moment_certificate.py')))
assert 2*ns['avg'](ns['A']**2*ns['B']**4)==Q(1,17640)
print('COMPARABLE_MOMENT := EXACT_MATCH')
M=sp+s.Rational(1,17640)
p=s.expand(s.Rational(3557,42000)+s.Rational(6,5)*M)
assert p==32*s.pi**2/7-s.Rational(13239637,294000)
hparam=6*(M-s.Rational(19,176400))
probs=[s.expand(a+b*hparam) for a,b in zip(ns['u'],ns['w'])]
assert s.simplify(sum(probs)-1)==0
# rational pi bounds from classical Archimedean refinement via Machin alternating series
def atan_bounds(x,n=20):
 v=sum(((-1)**k*x**(2*k+1)/ (2*k+1) for k in range(n)),Q(0)); w=v+(-1)**n*x**(2*n+1)/(2*n+1); return min(v,w),max(v,w)
l1,h1=atan_bounds(Q(1,5));l2,h2=atan_bounds(Q(1,239));pl=16*l1-4*h2;ph=16*h1-4*l2
for v in probs:
 co=v.coeff(s.pi,2); const=v-co*s.pi**2
 assert min(const+co*pl**2,const+co*ph**2)>0
for row,rhs in zip(ns['rows']+[ns['m']],ns['rhs']+[M]):
 assert s.expand(sum(a*b for a,b in zip(row,probs))-rhs)==0
assert s.expand(sum(a*b for a,b in zip(ns['c'],probs))-p)==0
print('ALL_16_PROBABILITIES := EXACT_MATCH_POSITIVE')
for i,(e,v) in enumerate(zip(ns['E'],probs)): print(i, sorted(e),v, v.evalf(12))
print('P42 :=',p)

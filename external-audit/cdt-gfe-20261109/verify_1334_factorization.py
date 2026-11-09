"""Exact structural identity and rational nonvanishing bound; not physics review.
Requires SymPy. Source coefficients independently extracted in prior isolated audit.
"""
from fractions import Fraction as Q
import sympy as s
M,beta,r,lam,omega=s.symbols("M beta r lam omega")
C=-beta*lam*(r-2*M)*(8*M*beta+5*r**3)/(12*r**4)
D=-2*C
G=C
F=beta*lam*(r-2*M)**2*(lam-2)*(5*r**3-16*M*beta)/(12*r**7)
assert s.cancel(D+2*C)==0
assert s.cancel(G-C)==0
c4=2*C
a3=d3=2*s.I*omega*C
b2=-2*(F+omega**2*G)
det=s.factor(a3*(a3*d3-c4*b2))
expected=s.I*beta**3*lam**3*omega*(r-2*M)**4*(lam-2)*(5*r**3-16*M*beta)*(8*M*beta+5*r**3)**2/(216*r**15)
assert s.cancel(det-expected)==0
spec=s.factor(det.subs({r:3,lam:6,omega:s.I/4})/beta**3)
target=(2*M-3)**4*(8*M*beta+135)**2*(16*M*beta-135)/3**15
assert s.cancel(spec-target)==0
Mmax=Q(101,100)
xmax=8*Mmax*Q(1,100)
K=Q(51,50)**4*(405+2*xmax)*(8*Mmax)**2/Q(3**15)
c0=Q(125,729)*Q(49,50)**4
lower=c0-K*Q(1,10000)
assert 0<K<Q(1,100) and lower>0
assert 135-xmax>0 and 135-2*xmax>0
print("GENERAL_EXACT_FACTOR := PASS")
print("SPECIALIZED_EXACT_FACTOR := PASS")
print("NORMALIZED_LOWER_BOUND :=",lower)
print("DOMAIN := real M,beta; |M-1|<=1/100, |beta|<=1/100, beta != 0")
print("BETA_ZERO := DESCRIPTOR_SINGULAR")
print("INDEPENDENT_PHYSICAL_REVIEW := OPEN")

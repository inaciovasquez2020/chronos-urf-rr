#!/usr/bin/env python3
"""Exact first 5 higher angular HS masses and rigorous 4D Minkowski p_(4,2) upper bound.

No floating-point arithmetic is used for the proof certificate. π² is bounded
by rational Machin-arctangent alternating series. The exact finite angular-moment
formulas are verified by rational partial fractions and Legendre recurrences.
The full E[J_+²] and infinite-growth sampling stability remain OPEN.
"""
from collections import Counter
from fractions import Fraction as Q
from math import factorial,prod,comb

# Finite positive-term series from the 4D causal-pair angular eigenvalues:
# M_(p,2) = (18/7) * sum_n c_(p,n), p>=2, where
# c_(p,n) = 2p *prod_{k=1}^{p-1}(n+k)/
#             (prod_{k=4}^{p+4}(n+k) *prod_{k=p+1}^{p+3}(n+k)).
# Its exact partial fractions use first and second order poles only;
# ∑_n(n+a)^-2= ζ(2)-H_(a-1)^(2), and ∑ A_a=0.

def harmonic(n,order=1):return sum((Q(1,k**order) for k in range(1,n+1)),Q())

def moment(p):
    poles=Counter(list(range(4,p+5))+list(range(p+1,p+4)))
    A={};B={}
    for a,m in poles.items():
        N0=2*p*prod(k-a for k in range(1,p))
        N1=2*p*sum(prod(k-a for k in range(1,p) if k!=j) for j in range(1,p))
        D=prod((k-a)**m_k for k,m_k in poles.items() if k!=a)
        val=Q(N0,D)
        B[a]=val if m==2 else Q()
        A[a]=Q(N1,D)-val*sum((Q(m_k,k-a) for k,m_k in poles.items() if k!=a),Q()) if m==2 else val
    assert sum(A.values(),Q())==0
    for n in range(12):
        term=Q(2*p*prod(n+k for k in range(1,p)),
               prod(n+k for k in range(4,p+5))*prod(n+k for k in range(p+1,p+4)))
        apart=sum((A[a]*Q(1,n+a)+B[a]*Q(1,(n+a)**2) for a in poles),Q())
        assert term==apart,(p,n,term,apart)
    rat=Q(18,7)*sum((-A[a]*harmonic(a-1)-B[a]*harmonic(a-1,2) for a in poles),Q())
    pi2_coeff=Q(18,7)*sum(B.values(),Q())/6
    return rat,pi2_coeff

# Polynomial arithmetic in f; P_l(1-2f) via Legendre recurrence.
def add(x,y):return [a+b for a,b in __import__('itertools').zip_longest(x,y,fillvalue=Q())]
def scale(x,a):return [a*v for v in x]
def mul_linear(x):
    out=[Q()]*(len(x)+1)
    for k,v in enumerate(x):out[k]+=v;out[k+1]-=2*v
    return out
P0=[Q(1)];P1=[Q(1),Q(-2)];Ps={0:P0,1:P1}
for ell in range(1,6):
    Ps[ell+1]=scale(add(scale(mul_linear(Ps[ell]),2*ell+1),scale(Ps[ell-1],-ell)),Q(1,ell+1))

moments={p:moment(p) for p in range(2,11)}
expected=[(Q(-829,14),Q(6)),(Q(-35649,14),Q(258)),
          (Q(-32925),Q(3336)),(Q(-8083206,35),Q(23400)),
          (Q(-155653531,140),Q(112650))]
B=[]
for ell in range(1,6):
    deriv=[k*Ps[ell][k] for k in range(1,len(Ps[ell]))]
    R=scale(deriv,Q(-1,ell*(ell+1)))
    square=[Q()]*(2*len(R)-1)
    for i,a in enumerate(R):
        for j,b in enumerate(R):square[i+j]+=a*b
    br=sum((co*moments[k+2][0] for k,co in enumerate(square)),Q())
    bc=sum((co*moments[k+2][1] for k,co in enumerate(square)),Q())
    B.append((br,bc))
    assert B[-1]==expected[ell-1],(ell,B[-1],expected[ell-1])

# Rigorous bounding rational interval for pi using Machin's identity.
def atan_interval(inverse,terms=36):
    partial=sum((Q((-1)**k,(2*k+1)*inverse**(2*k+1)) for k in range(terms)),Q())
    next_term=Q((-1)**terms,(2*terms+1)*inverse**(2*terms+1))
    return min(partial,partial+next_term),max(partial,partial+next_term)
a5lo,a5hi=atan_interval(5);a239lo,a239hi=atan_interval(239)
pi_lo=16*a5lo-4*a239hi
pi_hi=16*a5hi-4*a239lo
assert Q(3)<pi_lo<pi_hi<Q(22,7)
pi2lo,pi2hi=pi_lo**2,pi_hi**2

intervals=[]
for d,c in B:
    assert c>=0
    lo=d+c*pi2lo;hi=d+c*pi2hi
    assert 0<lo<=hi
    intervals.append((lo,hi))
S=Q(3,140)
Rlo=S-sum((2*l+1)*hi for l,(lo,hi) in enumerate(intervals,1))
Rhi=S-sum((2*l+1)*lo for l,(lo,hi) in enumerate(intervals,1))
assert 0<Rlo<Rhi
A0=Q(513,875875)
# Positivity and HS/trace inequality:
# E[J²]=A0+∑_{l>=1} A_l, 0<=A_l<=(2l+1)*b_l².
# For l>=6, ∑ A_l <= [sum_(l>=6)(2l+1)b_l]^2 /13.
J_upper=A0+sum((2*l+1)*hi**2 for l,(lo,hi) in enumerate(intervals,1))+Rhi**2/13
p_lower=Q(3557,42000)+Q(6,5)*A0
p_upper=Q(3557,42000)+Q(6,5)*J_upper
assert p_lower==Q(17950529,210210000)
assert p_upper<Q(8543935,100000000) # strict rigorous decimal threshold 0.08543935
assert Q(8543933,100000000) < p_upper

print('PARTIAL_FRACTION_IDENTITIES := PASS (p=2..10, 12 exact samples each)')
print('LEGENDRE_COEFFICIENT_IDENTITIES := PASS (ell=1..5)')
print('RIGOROUS_PI_INTERVAL := Machin alternating arctan, terms=36')
print('ANGULAR_MODE_MASSES_exact_d_plus_c_pi2 :=')
for l,(d,c) in enumerate(B,1):print('ell',l,'b_l =',d,'+',c,'*pi^2')
print('HIGHER_MODE_HS_REMAINDER_LOWER_POSITIVE := PASS')
print('EXACT_J_LOWER :=',A0)
print('RIGOROUS_J_UPPER_LT :=',Q(8543935,100000000)*Q(5,6)-Q(3557,42000)*Q(5,6))
print('P42_LOWER_EXACT :=',p_lower)
print('P42_UPPER_STRICT := 0.08543935')
print('P42_UPPER_RATIO_WITH_THRESHOLD :=',p_upper < Q(8543935,100000000))
print('FULL_E_J2 := OPEN')
print('INFINITE_GROWTH_STABILITY := OPEN')
print('LEAN_VERIFIED := NOT_RUN')

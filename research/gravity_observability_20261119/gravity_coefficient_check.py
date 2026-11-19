"""Exact arithmetic checks; not a proof of the geometric input formulas."""
from fractions import Fraction as Q
from math import prod, factorial


def moment(m):
    return Q(120*m, prod(range(2*m, 2*m+4)))


def c(k):
    return (1-moment(k+1))/180

# Dirichlet(2,...,2) fourth moments from the simplex beta integral.
for m in range(2, 65):
    direct = m*Q(factorial(5)*factorial(2*m-1), factorial(2*m+3))
    assert direct == moment(m)
    assert 0 < moment(m) < 1
assert c(1) == Q(1,252)
assert c(2) == Q(37,7560)
assert c(2)-2*c(1) == -Q(23,7560)
# Wang arXiv:1904.01034v2, eq. (79), d=4; H^2=2 B^2, D^2=4 E^2.
d=4
factor=Q(d*(d-1), 2*16*90*(d-1)*(d+1)*(d+2)*(d+3)*(d+4))
e=factor*(7*d**3+58*d**2+146*d+108-6*(d+2))
b=factor*12*(d+2)*(d+6)
assert (e,b)==(Q(127,75600),Q(1,1680))
assert e+b==Q(43,18900)
assert c(1)/2==Q(1,504)
assert e+b-c(1)/2==Q(11,37800)
# Conditional reassembly: input boundary and density coefficients, not derived here.
ce=Q(3,8)*(Q(1,216)-Q(1,7560))
cb=Q(3,8)*(Q(1,1350)+Q(1,18900))
assert (ce,cb)==(Q(17,10080),Q(1,3360))
assert ce+cb==c(1)/2
# Chain Jacobian and its inverse.
a=lambda k:-Q(4*k,12*(4*k+2)*(4*(k+1)+2))
beta=lambda k:Q(4*k,12*(4*(k+1)+2))
j=[[a(k)-k*a(1),beta(k)-k*beta(1)] for k in (2,3)]
assert j==[[Q(2,315),-Q(2,105)],[Q(4,315),-Q(2,45)]]
w=[[Q(2205,2),-Q(945,2)],[Q(315),-Q(315,2)]]
assert [[sum(w[i][k]*j[k][l] for k in range(2)) for l in range(2)] for i in range(2)]==[[1,0],[0,1]]
# Algebraic optimization of nested-diamond detector: p(1-p)=1/4-(p-1/2)^2.
for i in range(101):
    p=Q(i,100)
    assert p*(1-p)==Q(1,4)-(p-Q(1,2))**2
print('DIRICHLET_MOMENTS := PASS (m=2..64)')
print('EXACT_PLANE_WAVE_COEFFICIENTS :=', c(1), c(2)-2*c(1))
print('ARXIV_V2_COEFFICIENT_GAP :=', e+b-c(1)/2)
print('CONDITIONAL_REASSEMBLY_ARITHMETIC := PASS')
print('CHAIN_JACOBIAN_INVERSE := PASS')
print('NESTED_DESIGN_IDENTITY := PASS')
print('GEOMETRIC_INPUTS_AND_LEAN := NOT_VERIFIED_BY_THIS_SCRIPT')

#!/usr/bin/env python3
"""Exact rational certificate for a quantitative local inverse of chain probabilities.

The mathematical Hessian bound follows from the density score identity
documented in docs/math/CAUSAL_CHAIN_LOCAL_INVERSE_CONFIDENCE_2026_11_12.md.
This script verifies the exact linear-algebra and inequality constants.
It does NOT numerically integrate the nonlinear response F away from zero.
"""
from fractions import Fraction as Q

if not __debug__:
    raise SystemExit("INCOMPLETE: assertions disabled")

J11, J12 = Q(1,25), Q(0)
J21, J22 = Q(9,3500), Q(16,165375)
assert J11 * J22 - J12 * J21 == Q(16,4134375)
inv11, inv12 = 1 / J11, Q(0)
inv21, inv22 = -J21 / (J11 * J22), 1 / J22
assert inv11 == 25 and inv21 == -Q(42525,64) and inv22 == Q(165375,16)
M = max(abs(inv11) + abs(inv12), abs(inv21) + abs(inv22))
assert M == Q(704025,64)

# For 0<=f_i<=1, u=1+a*f_1+b*f_2 >= L=1-2r.
# The density log-score has |score_i|<=2/L, and
# |d_j score_i|<=3/L^2, giving each kth probability Hessian
# entry a bound (4*k*k+3*k)/L^2. The largest is k=3.
assert 4*2*2 + 3*2 == 22
assert 4*3*3 + 3*3 == 45
r = Q(1,4_000_000)
L = 1 - 2*r
H = Q(45,1) / L**2
# Each Jacobian entry varies by at most 2*r*H;
# matrix infinity norm sums two columns.
delta = 4*r*H
kappa = M*delta
assert 0 < kappa < Q(1,2), kappa
# The inverse Lipschitz constant M/(1-kappa) is <=2*M.
assert M/(1-kappa) < 2*M
assert 2*M == Q(704025,32)
# For theta,eta in the cube, ||F(theta)-F(eta)||_inf
# >= (1-kappa)/M ||theta-eta||_inf.
# For confidence-set members both within eps of the observed
# statistic, the diameter bound is 2*M/(1-kappa)*eps <=4*M*eps.
assert Q(2)*M/(1-kappa) < 4*M

# Transparent conservative fixed sample size: for alpha=1/20,
# ln(4/alpha)=ln(80)<5, so epsilon_3^2 < 45/(2*N)
# (and epsilon_3 >= epsilon_2 for every alpha).
# To make 4*M*epsilon_3 <= r, use a sufficient exact integer N.
N_required = ( (4*M/r)**2 * Q(45,2) )
N_ceiling = (N_required.numerator + N_required.denominator - 1)//N_required.denominator
assert Q(4*M)**2*Q(45,2)/N_ceiling <= r*r
assert N_ceiling > 10**20

# A second, independent discrete iid check of bounded differences:
# for every N in [3,7], a single input-coordinate replacement
# changes an unordered k-chain U-statistic by <=k/N.
# Enumerating three-atom chains (0<1<2) tests the generic index bound,
# not the continuum model.
from itertools import product, combinations
for n in range(3,8):
    for k in (2,3):
        def U(x):
            return Q(sum(len({x[t] for t in ids}) == k
                         for ids in combinations(range(n), k)),
                     __import__("math").comb(n,k))
        for x in product(range(3),repeat=n):
            original=U(x)
            for i in range(n):
                y=x[:i]+((x[i]+1)%3,)+x[i+1:]
                assert abs(original-U(y)) <= Q(k,n), (n,k,x,i)

print("INVERSE_JACOBIAN_RATIONAL := PASS", M)
print("HESSIAN_BOUND_CONSTANT := PASS 45")
print("CERTIFIED_CUBE_RADIUS := 1/4000000")
print("CONTRACTION_FACTOR := ", kappa)
print("CONTRACTION_LT_HALF := PASS")
print("NONASYMPTOTIC_CONFIDENCE_DIAMETER_BOUND := PASS")
print("CONSERVATIVE_N_ALPHA_005_FOR_DIAMETER_AT_MOST_R :=",N_ceiling)
print("FINITE_DISCRETE_BOUNDED_DIFFERENCES := PASS")
print("NONLINEAR_RESPONSE_NUMERICAL_INTEGRATION := NOT_RUN")
print("LEAN_VERIFIED := NOT_RUN")
print("RESULT := COMPUTATION_PASS")

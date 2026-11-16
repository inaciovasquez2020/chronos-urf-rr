#!/usr/bin/env python3
"""Exact arithmetic check of conditioning on causality for common-future volume.
Inputs are separately derived Minkowski diamond mixed moments. This script tests
logical consequences of those inputs, not their geometric derivation and not Lean.
"""
from fractions import Fraction as F
p = F(1,10)                 # Pr(X and Y comparable)
M20 = F(1,105)              # E[W_plus(X)^2] = E[J_+(X,Y)]
M11 = F(1,2100)             # E[W_minus W_plus]
M12 = F(1,35280)            # E[W_minus W_plus^2]
EJ_C = 2*M11               # comparable X<Y or Y<X
EJ2_C = 2*M12
EJ_I = M20-EJ_C
mu_C,mu_I = EJ_C/p,EJ_I/(1-p)
var_C = EJ2_C/p-mu_C**2
lb = EJ2_C+(1-p)*mu_I**2
assert EJ_C == p*M20
assert mu_C == mu_I == M20 == F(1,105)
assert var_C == F(1,2100)
assert lb == F(61,441000)
assert 6*lb == F(61,73500)
print('EXACT_INPUTS: p(C)=',p,'EJ=',M20,'M11=',M11,'M12=',M12)
print('E[J | comparable] :=',mu_C)
print('E[J | incomparable] :=',mu_I)
print('Cov(J, 1_comparable) :=',EJ_C-p*M20)
print('Var(J | comparable) :=',var_C)
print('E[J^2] >=',lb)
print('EXACT_RATIONAL_CHECK := PASS')
print('GEOMETRIC_INPUT_DERIVATIONS := ASSUMED_FROM_PRIOR_AUDIT')
print('FULL_SECOND_MOMENT := OPEN')
print('MINKOWSKI_PREFIX_UNIQUENESS := OPEN')
print('LEAN_VERIFIED := NO')

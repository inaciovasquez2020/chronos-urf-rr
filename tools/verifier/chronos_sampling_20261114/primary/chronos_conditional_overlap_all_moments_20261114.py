#!/usr/bin/env python3
"""Exact paper-certificate checks for J_+(X,Y) conditional on X,Y comparable.
No Minkowski sampling, numerical inference, Lean, or repository edits.
Geometry assumption: unit height 4D Minkowski diamond, normalized null-coordinate
measure 12(b-a)^2 da db, 0<=a<=b<=1, and W_-=a²b², W_+=(1-a)²(1-b)².
"""
from fractions import Fraction as F
from math import comb

def one_dim(p):  # integral_0^1 x^p (1-x)^2 dx
    return F(1,p+1)-F(2,p+2)+F(1,p+3)

def closed(k):
    return F(180,(k+1)**2*(k+2)**2*(2*k+1)*(2*k+3)**2*(2*k+5))

def factored(k):
    I0,I1,I2 = (one_dim(2*k+i) for i in range(3))
    return 240*(I0*I2-I1*I1)

def direct(k):
    # 240 * integral_{0<=A<=B<=1}(B-A)^2 (1-A)^2(1-B)^2 A^(2k) B^(2k)
    # binomial-expand (1-A)^2 and (1-B)^2 and integrate A then B
    result=F(0)
    for i in range(3):
      for j in range(3):
        coef = F((-1)**(i+j)*comb(2,i)*comb(2,j))
        # integrate A^(m)B^n(B² - 2AB + A²) over 0<=A<=B<=1
        m,n=2*k+i,2*k+j
        result+=coef*(F(1,(m+1)*(m+n+4))-F(2,(m+2)*(m+n+4))+F(1,(m+3)*(m+n+4)))
    return 240*result

a=(F(1),F(1),F(2),F(2),F(1,2),F(3,2),F(3,2),F(5,2))
def beta_product(k):
    v=F(1)
    for alpha in a: v*=alpha/(alpha+k)
    return v

for k in range(81):
    x=closed(k)
    assert factored(k)==x,(k,'factored')
    assert direct(k)==x,(k,'direct')
    assert beta_product(k)==x,(k,'beta-product')
assert closed(0)==1
assert closed(1)==F(1,105)
assert closed(2)==F(1,1764)
print('GEOMETRIC_ASSUMPTIONS := normalized Minkowski-diamond null-coordinate measure')
print('COMPARABLE_CONDITIONAL_MOMENT := 180/((k+1)^2(k+2)^2(2k+1)(2k+3)^2(2k+5))')
print('EQUIVALENT_DISTRIBUTION := product of independent Beta(a,1), a=1,1,2,2,1/2,3/2,3/2,5/2')
print('EXACT_RATIONAL_CHECKS := 81 moments, 3 independent algebraic representations, PASS')
print('UNCONDITIONAL_E_J_SQUARED := OPEN (incomparable component)')
print('INFINITE_GROWTH_PREFIX_STABILITY := OPEN')
print('LEAN_VERIFIED := NO')

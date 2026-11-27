#!/usr/bin/env python3
"""Exact mixed causal-volume moments in a normalized 4D Minkowski diamond.

RESULT (analytic, conditional on the stated geometric model):
For nonnegative integers r,s, let a=t-radial, b=t+radial with
0 <= a <= b <= 1. The normalized density is 12(b-a)^2 da db,
W_past=a^2*b^2, W_future=(1-a)^2*(1-b)^2. Then

  E[W_past^r W_future^s]
    = 12*A*B / ((A+B)^2*(A+B+1)) * Beta(A,B)^2,
      A=2*r+1, B=2*s+1,
      Beta(A,B)=(A-1)!*(B-1)!/(A+B-1)!.

PROOF: The integrand is symmetric in (a,b), so integration on the
ordered triangle equals half the integral on [0,1]^2. After expanding
(b-a)^2=b^2+a^2-2ab, the square integral factors:
  12 * (Beta(A+2,B)*Beta(A,B) - Beta(A+1,B)^2).
Use Beta(A+1,B)=A/(A+B)*Beta(A,B) and
Beta(A+2,B)=A(A+1)/((A+B)*(A+B+1))*Beta(A,B).
Taking the difference gives A*B/((A+B)^2*(A+B+1))*Beta(A,B)^2.
This proof uses elementary beta-integral identities, not Lean.

A second test routine integrates an expanded polynomial directly over
0<=a<=b<=1 using exact rational arithmetic; no float or third-party
packages. Exhaustive tests verify the identity for 0<=r,s<=12.
"""

from fractions import Fraction
from math import comb, factorial


def beta_integer(a: int, b: int) -> Fraction:
    if not (isinstance(a, int) and isinstance(b, int) and a >= 1 and b >= 1):
        raise ValueError('beta_integer requires positive integer arguments')
    return Fraction(factorial(a - 1) * factorial(b - 1), factorial(a + b - 1))


def mixed_moment_closed(r: int, s: int) -> Fraction:
    if not (isinstance(r, int) and isinstance(s, int) and r >= 0 and s >= 0):
        raise ValueError('moments require nonnegative integer powers')
    a, b = 2 * r + 1, 2 * s + 1
    return Fraction(12 * a * b, (a + b) ** 2 * (a + b + 1)) * beta_integer(a, b) ** 2


def mixed_moment_direct(r: int, s: int) -> Fraction:
    """Independent exact integration of expanded (b-a)^2 polynomial."""
    if not (isinstance(r, int) and isinstance(s, int) and r >= 0 and s >= 0):
        raise ValueError('moments require nonnegative integer powers')
    acc = Fraction(0)
    for i in range(2 * s + 1):
        for j in range(2 * s + 1):
            coeff = (-1) ** (i + j) * comb(2 * s, i) * comb(2 * s, j)
            # a^(2r+i) b^(2r+j) * (b^2 - 2ab + a^2), on 0<=a<=b<=1
            for da, db, sign in ((0, 2, 1), (1, 1, -2), (2, 0, 1)):
                pa = 2 * r + i + da
                pb = 2 * r + j + db
                acc += Fraction(12 * coeff * sign, (pa + 1) * (pa + pb + 2))
    return acc


def verify() -> None:
    assert mixed_moment_closed(0, 0) == 1
    assert mixed_moment_closed(1, 0) == Fraction(1, 20)
    assert mixed_moment_closed(2, 0) == Fraction(1, 105)
    assert mixed_moment_closed(3, 0) == Fraction(1, 336)
    assert mixed_moment_closed(1, 1) == Fraction(1, 2100)
    assert mixed_moment_closed(2, 1) == Fraction(1, 35280)
    assert mixed_moment_closed(2, 1) == mixed_moment_closed(1, 2)
    count = 0
    for r in range(13):
        for s in range(13):
            assert mixed_moment_closed(r, s) == mixed_moment_direct(r, s), (r, s)
            assert mixed_moment_closed(r, s) == mixed_moment_closed(s, r), (r, s)
            count += 1
    for bad in ((-1, 0), (0, -1), (1.5, 2)):
        try:
            mixed_moment_closed(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f'invalid powers accepted: {bad}')
    print('MODEL := NORMALIZED_4D_MINKOWSKI_CAUSAL_DIAMOND')
    print('ANALYTIC_IDENTITY := PROVED_ON_PAPER')
    print('EXACT_INDEPENDENT_POLYNOMIAL_CHECKS :=', count)
    print('MIXED_MOMENT_2_1 :=', mixed_moment_closed(2, 1))
    print('VALIDATION := COMPUTATION_PASS')
    print('LEAN := NOT_RUN')
    print('GENERAL_SPACETIME_RECONSTRUCTION := OPEN')
    print('ACTUAL_MINKOWSKI_P_4_2 := OPEN')


if __name__ == '__main__':
    verify()

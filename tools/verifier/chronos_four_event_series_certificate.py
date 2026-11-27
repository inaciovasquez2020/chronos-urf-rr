#!/usr/bin/env python3
"""Dependency-free exact arithmetic audit of the proposed four-event series.

Scope: rational partial fractions, infinite-sum reduction to zeta(2),
reported affine probability identity and bounded numerical comparison.
NOT a verification of the geometric continuum integral or a Lean proof.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as Q

SHIFTS = (5, 6, 7, 8)
A = {5: Q(-374, 7), 6: Q(-162, 7), 7: Q(486, 7), 8: Q(50, 7)}
B = {5: Q(243, 14), 6: Q(1143, 14), 7: Q(513, 14), 8: Q(3, 2)}
ZETA2_COEFFICIENT = Q(960, 7)
RATIONAL_PART = Q(-3316139, 14700)
K22_CONSTANT = Q(-6632287, 29400)
AFFINE_OFFSET = Q(24937, 294000)
P42_CONSTANT = Q(-13239637, 294000)


def mul(x, y):
    out = [Q(0)] * (len(x) + len(y) - 1)
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i + j] += a * b
    return out


def add(x, y):
    return [((x[i] if i < len(x) else Q(0)) +
             (y[i] if i < len(y) else Q(0)))
            for i in range(max(len(x), len(y)))]


def scale(x, c):
    return [c * a for a in x]


def harmonic(k, degree):
    return sum((Q(1, j ** degree) for j in range(1, k + 1)), Q(0))


def term(n):
    return Q(18 * (2 * n**3 + 59 * n**2 + 583 * n + 1933),
             7 * ((n + 5)*(n + 6)*(n + 7)*(n + 8))**2)


def decimal_fraction(x):
    return Decimal(x.numerator) / Decimal(x.denominator)


def arctan_inverse(q):
    """Alternating arctan(1/q) series, used only for a numerical cross-check."""
    z = Decimal(1) / Decimal(q)
    z2 = z * z
    power = z
    ans = Decimal(0)
    threshold = Decimal('1e-78')
    for n in range(240):
        addend = power / Decimal(2*n + 1)
        ans += addend if n % 2 == 0 else -addend
        if abs(addend) < threshold:
            return ans
        power *= z2
    raise RuntimeError('arctan series did not converge within guard')



def arctan_bracket(q, count=80):
    """Exact rational enclosure from alternating-series remainder, q > 1."""
    assert q > 1 and 1 <= count <= 240
    partial = sum((Q(1 if k % 2 == 0 else -1,
                     (2*k + 1) * q ** (2*k + 1))
                   for k in range(count)), Q(0))
    next_magnitude = Q(1, (2*count + 1) * q ** (2*count + 1))
    if count % 2 == 0:
        return partial, partial + next_magnitude
    return partial - next_magnitude, partial

def main():
    # Polynomial equality in Q[n]: no symbolic CAS, interpolation, or sampling.
    # Multiply both sides by prod_(j=5)^8 (n+j)^2.
    rhs = [Q(0)]
    for j in SHIFTS:
        others = [Q(1)]
        for k in SHIFTS:
            if k != j:
                others = mul(others, mul([Q(k), Q(1)], [Q(k), Q(1)]))
        rhs = add(rhs, scale(mul(others, [Q(j), Q(1)]), A[j]))
        rhs = add(rhs, scale(others, B[j]))
    target = [Q(18 * 1933, 7), Q(18 * 583, 7),
              Q(18 * 59, 7), Q(18 * 2, 7)]
    assert rhs[:4] == target and all(v == 0 for v in rhs[4:]), 'rational identity'

    assert sum(A.values(), Q(0)) == 0, 'simple poles must cancel'
    assert sum(B.values(), Q(0)) == ZETA2_COEFFICIENT, 'zeta(2) coefficient'
    rational = sum((-A[j]*harmonic(j-1, 1) - B[j]*harmonic(j-1, 2)
                    for j in SHIFTS), Q(0))
    assert rational == RATIONAL_PART, 'summation rational term'

    # If zeta(2)=pi^2/6, the sum is 160*pi^2/7 + RATIONAL_PART.
    # In the claimed K22 series there is an additive correction +3/9800.
    assert RATIONAL_PART - Q(3, 9800) == K22_CONSTANT, 'K22 offset'
    assert ZETA2_COEFFICIENT / 6 == Q(160, 7), 'pi^2 coefficient'
    assert Q(160, 7)/5 == Q(32, 7), 'p42 pi^2 coefficient'
    assert K22_CONSTANT/5 + AFFINE_OFFSET == P42_CONSTANT, 'p42 affine identity'

    # Independent finite rational checks of the decomposition.
    for n in range(128):
        apart = sum((A[j]/(n+j) + B[j]/(n+j)**2 for j in SHIFTS), Q(0))
        assert term(n) == apart, f'finite exact instance n={n}'

    # Independently enclose pi via the exact Machin formula and alternating
    # rational arctangent bounds; this uses no floating-point arithmetic.
    a5_lo, a5_hi = arctan_bracket(5)
    a239_lo, a239_hi = arctan_bracket(239)
    pi_lo = 16*a5_lo - 4*a239_hi
    pi_hi = 16*a5_hi - 4*a239_lo
    assert 3 < pi_lo < pi_hi < 4
    assert pi_hi - pi_lo < Q(1, 10**100)
    closed_lo = Q(160, 7)*pi_lo*pi_lo + RATIONAL_PART
    closed_hi = Q(160, 7)*pi_hi*pi_hi + RATIONAL_PART
    k_lo = closed_lo - Q(3, 9800)
    k_hi = closed_hi - Q(3, 9800)
    p_lo = k_lo/5 + AFFINE_OFFSET
    p_hi = k_hi/5 + AFFINE_OFFSET
    assert 0 < k_lo < k_hi < 1
    assert 0 < p_lo < p_hi < 1
    assert p_hi - p_lo < Q(1, 10**100)

    # For n>=0, 2n^3+59n^2+583n+1933 <= 16(n+5)^3.
    # Consequently term(n) <= (288/7)*(n+5)^(-5), and the integral test
    # bounds sum_(n>=N) term(n) by (288/7)*((N+5)^(-5)+1/(4(N+5)^4)).
    assert (14, 181, 617, 67) == (16-2, 240-59, 1200-583, 2000-1933)
    # Cross-check the closed-form rational interval against a finite exact
    # partial sum and an independent rigorous (though loose) tail bound.
    N_exact = 50
    exact_partial = sum((term(n) for n in range(N_exact)), Q(0))
    exact_tail = Q(288, 7) * (Q(1, (N_exact+5)**5) +
                               Q(1, 4*(N_exact+5)**4))
    assert exact_partial < closed_lo <= closed_hi < exact_partial + exact_tail
    N = 2000
    tail_bound = Q(288, 7) * (Q(1, (N+5)**5) + Q(1, 4*(N+5)**4))
    with localcontext() as ctx:
        ctx.prec = 70
        pi = 16 * arctan_inverse(5) - 4 * arctan_inverse(239)
        full_sum = Decimal(160)/Decimal(7)*pi*pi + decimal_fraction(RATIONAL_PART)
        partial_sum = sum((decimal_fraction(term(n)) for n in range(N)), Decimal(0))
        diff = full_sum - partial_sum
        assert Decimal(0) < diff < decimal_fraction(tail_bound), 'numerical tail enclosure'
        k22 = Decimal(160)/Decimal(7)*pi*pi + decimal_fraction(K22_CONSTANT)
        p42 = Decimal(32)/Decimal(7)*pi*pi + decimal_fraction(P42_CONSTANT)
        assert abs(p42 - (k22/Decimal(5) + decimal_fraction(AFFINE_OFFSET))) < Decimal('1e-65'), 'numeric affine rounding'
        print('RATIONAL_PARTIAL_FRACTIONS := PASS')
        print('SIMPLE_POLE_CANCELLATION := PASS')
        print('ZETA2_COEFFICIENT :=', ZETA2_COEFFICIENT)
        print('RATIONAL_SUM :=', RATIONAL_PART)
        print('CLOSED_SERIES := (160/7)*pi^2 - 3316139/14700')
        print('K22_FROM_CLAIMED_SERIES := (160/7)*pi^2 - 6632287/29400')
        print('P42_AFFINE_REDUCTION := K22/5 + 24937/294000')
        print('FINITE_EXACT_INSTANCES := 128/128 PASS')
        print('RATIONAL_PI_INTERVAL := PASS (Machin / alternating remainder)')
        print('PROBABILITY_FORMULA_INTERVALS := SUBSET_OF_(0,1)')
        print('EXACT_PARTIAL_SUM_TAIL_ENCLOSURE := PASS (N=50)')
        print('DECIMAL_PI_METHOD := Machin arctangent, 70-digit arithmetic')
        print('FINITE_DECIMAL_TERMS :=', N)
        print('TAIL_BOUND :=', tail_bound)
        print('TAIL_ENCLOSURE := PASS')
        print('K22_DECIMAL :=', k22)
        print('P42_DECIMAL :=', p42)
    print('CONTINUUM_INTEGRAL_IDENTITY := NOT_VERIFIED')
    print('LEAN_COMPILATION_AND_AXIOMS := NOT_RUN')
    print('REPOSITORY_PYTEST_SUITE := NOT_RUN')
    print('RESULT := EXACT_ALGEBRA_AND_BOUNDED_NUMERIC_PASS')


if __name__ == '__main__':
    main()

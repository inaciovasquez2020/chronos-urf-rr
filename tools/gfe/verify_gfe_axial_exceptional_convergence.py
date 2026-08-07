#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import runpy
import sys
from pathlib import Path

import sympy as s

if len(sys.argv) != 3:
    raise SystemExit(
        "MISSING_OBJECT := formal verifier and canonical source arguments"
    )

formal = Path(sys.argv[1])
source = Path(sys.argv[2])

if not formal.is_file():
    raise SystemExit(f"MISSING_OBJECT := {formal}")
if not source.is_file():
    raise SystemExit(f"MISSING_OBJECT := {source}")

old_argv = sys.argv[:]
formal_stdout = io.StringIO()
try:
    sys.argv = [str(formal), str(source)]
    with contextlib.redirect_stdout(formal_stdout):
        ns = runpy.run_path(str(formal), run_name="gfe_exceptional_formal_verifier")
finally:
    sys.argv = old_argv

formal_text = formal_stdout.getvalue()
if (
    "RESULT := the current canonical GfE source certifies a formal "
    "exceptional logarithmic Frobenius solution to every Laurent order"
    not in formal_text
):
    print(formal_text, end="")
    raise SystemExit(
        "MISSING_OBJECT := passing exceptional all-orders formal theorem"
    )

required = [
    "x", "p", "n", "a", "b", "M", "beta", "alpha", "q0", "q1",
]
missing = [name for name in required if name not in ns]
if missing:
    raise SystemExit(
        "MISSING_OBJECT := formal-verifier symbols: " + ", ".join(missing)
    )

x = ns["x"]
p = ns["p"]
n = ns["n"]
a = ns["a"]
b = ns["b"]
M = ns["M"]
beta = ns["beta"]
alpha = ns["alpha"]
q0 = ns["q0"]
q1 = ns["q1"]

def simp(z):
    return s.factor(s.cancel(s.together(z)))

# The verifier uses H0=x^p*a and H1=x^(p-1)*b after dividing by x^p.
# Multiplying the two field equations by x^3 and x^2 respectively
# produces the Euler/Frobenius symbol whose Taylor coefficients give
# the exact lower-triangular recurrence blocks.
F = s.Matrix([
    [
        s.diff(simp(x**3*q0), a),
        s.diff(simp(x**3*q0), b),
    ],
    [
        s.diff(simp(x**2*q1), a),
        s.diff(simp(x**2*q1), b),
    ],
]).applyfunc(simp)

# Build the least common x-denominator, ignoring nonzero coefficient
# factors.  Its value at x=0 must be nonzero; otherwise the claimed
# row scaling has not actually produced an analytic Frobenius symbol.
den_polys = []
for entry in F:
    _, den = s.fraction(simp(entry))
    poly = s.Poly(den, x, domain="EX")
    den_polys.append(poly.monic())

Dpoly = s.Poly(1, x, domain="EX")
for poly in den_polys:
    Dpoly = s.lcm(Dpoly, poly)

D = s.factor(Dpoly.as_expr())
D0 = simp(D.subs(x, 0))
if D0 == 0:
    raise SystemExit(
        "BOUNDARY := row-scaled exceptional symbol still has a horizon pole"
    )

D = simp(D / D0)
assert simp(D.subs(x, 0) - 1) == 0

C = (D*F).applyfunc(simp)

entry_polys = []
for entry in C:
    _, den = s.fraction(entry)
    if x in den.free_symbols:
        raise SystemExit(
            "BOUNDARY := common denominator did not clear the x dependence"
        )
    entry_polys.append(s.Poly(entry, x, domain="EX"))

J = max(poly.degree() for poly in entry_polys)
if J < 1:
    raise SystemExit(
        "BOUNDARY := no lower-triangular lag was found"
    )

Cj = []
for j in range(J + 1):
    Cj.append(
        s.Matrix([
            [
                s.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j)
                for col in range(2)
            ]
            for row in range(2)
        ]).applyfunc(simp)
    )

max_p_degree = -1
for block in Cj:
    for entry in block:
        poly = s.Poly(entry, p, domain="EX")
        max_p_degree = max(max_p_degree, poly.degree())

if max_p_degree > 4:
    raise SystemExit(
        "BOUNDARY := exceptional Euler symbol has derivative degree above four"
    )

A = Cj[0].subs(p, alpha + n).applyfunc(simp)
A_saved = ns["A_derived"]
if any(
    simp(A[row, col] - A_saved[row, col]) != 0
    for row in range(2)
    for col in range(2)
):
    print("CLEARED_A_nn :=", A)
    print("SAVED_A_nn :=", A_saved)
    raise SystemExit(
        "BOUNDARY := denominator clearing changed the certified leading block"
    )

E = s.Matrix([1, 0])

def rvec(k):
    return s.Matrix([1, 2*M*(2*k + 1)])

def lvec(k):
    return s.Matrix([1, 2*M*(2*k - 3)])

A00 = simp(A[0, 0])
if A00 == 0:
    raise SystemExit(
        "BOUNDARY := chosen rank-one complement has zero leading coefficient"
    )

# xi_n is the particular amplitude in the fixed complement E:
# v_n = xi_n E + kappa_n r_n.
X_xi = {}
X_kap = {}
for j in range(1, J + 1):
    block = Cj[j].subs(p, alpha + n - j).applyfunc(simp)
    X_xi[j] = simp(-block[0, 0] / A00)
    X_kap[j] = simp(
        -(s.Matrix([[block[0, 0], block[0, 1]]])*rvec(n - j))[0]
        / A00
    )

# The order-(n+1) compatibility condition fixes kappa_n.
ell_next = lvec(n + 1)
C1n = Cj[1].subs(p, alpha + n).applyfunc(simp)
gamma_next = simp((ell_next.T*C1n*rvec(n))[0])
gamma_saved_next = simp(ns["gamma_expected"].subs(ns["n"], n + 1))
if simp(gamma_next - gamma_saved_next) != 0:
    print("DERIVED_GAMMA_n_PLUS_1 :=", gamma_next)
    print("SAVED_GAMMA_n_PLUS_1 :=", gamma_saved_next)
    raise SystemExit(
        "BOUNDARY := finite-lag compatibility coupling disagrees with formal theorem"
    )

cxi = simp((ell_next.T*C1n*E)[0])

K_xi = {
    j: simp(-cxi*X_xi[j]/gamma_next)
    for j in range(1, J + 1)
}
K_kap = {
    j: simp(-cxi*X_kap[j]/gamma_next)
    for j in range(1, J + 1)
}

for j in range(2, J + 1):
    lag = j - 1
    block = Cj[j].subs(p, alpha + n + 1 - j).applyfunc(simp)
    K_xi[lag] = simp(
        K_xi.get(lag, 0)
        - (ell_next.T*block*E)[0]/gamma_next
    )
    K_kap[lag] = simp(
        K_kap.get(lag, 0)
        - (ell_next.T*block*rvec(n + 1 - j))[0]/gamma_next
    )

def degree_at_infinity(expr):
    expr = simp(expr)
    if expr == 0:
        return -10**6
    num, den = s.fraction(expr)
    num_poly = s.Poly(num, n, domain="EX")
    den_poly = s.Poly(den, n, domain="EX")
    return num_poly.degree() - den_poly.degree()

def assert_no_integer_poles(expr):
    expr = simp(expr)
    if expr == 0:
        return
    _, den = s.fraction(expr)
    den_poly = s.Poly(den, n, domain="EX")
    monic = s.factor(den_poly.monic().as_expr())
    extras = monic.free_symbols - {n}
    if extras:
        raise SystemExit(
            "BOUNDARY := n-dependent transfer denominator depends on "
            "physical parameters: " + s.sstr(monic)
        )
    qpoly = s.Poly(monic, n, domain=s.QQ)
    for root, multiplicity in s.polys.polytools.ground_roots(qpoly).items():
        if root.is_integer and root >= 3:
            raise SystemExit(
                "BOUNDARY := transfer coefficient has an integer pole "
                f"at n={root}"
            )

degree_rows = []
max_transfer_degree = -10**6
for j in range(1, J + 1):
    row = [
        degree_at_infinity(X_xi.get(j, 0)),
        degree_at_infinity(X_kap.get(j, 0)),
        degree_at_infinity(K_xi.get(j, 0)),
        degree_at_infinity(K_kap.get(j, 0)),
    ]
    for expr in (
        X_xi.get(j, 0),
        X_kap.get(j, 0),
        K_xi.get(j, 0),
        K_kap.get(j, 0),
    ):
        assert_no_integer_poles(expr)
    degree_rows.append((j, row))
    max_transfer_degree = max(max_transfer_degree, *row)

# The non-log homogeneous recurrence is identical to the log recurrence.
# Its extra source is obtained by differentiating the Euler symbol in p.
# A finite p-degree bound therefore gives at most polynomial forcing
# coefficients. Polynomial times a geometric log majorant is geometric
# after an arbitrarily small enlargement of the exponential base.
Dpj = [
    block.diff(p).applyfunc(simp)
    for block in Cj
]
max_derivative_degree = -1
for block in Dpj:
    for entry in block:
        if entry == 0:
            continue
        max_derivative_degree = max(
            max_derivative_degree,
            s.Poly(entry, p, domain="EX").degree(),
        )

assert max_derivative_degree <= 3

print("EXCEPTIONAL_CONVERGENCE_STRUCTURE")
print("BASE_FORMAL_THEOREM := certified")
print("COMMON_ANALYTIC_DENOMINATOR :=", s.sstr(D))
print("COMMON_DENOMINATOR_AT_HORIZON := 1")
print("FINITE_LAG := ", J, sep="")
print("EULER_SYMBOL_MAX_P_DEGREE := ", max_p_degree, sep="")
print(
    "NONLOG_EXPONENT_DERIVATIVE_MAX_P_DEGREE := ",
    max_derivative_degree,
    sep="",
)
for lag, degrees in degree_rows:
    print(
        "LOG_TRANSFER_DEGREES_LAG_"
        + str(lag)
        + " := xi<-xi "
        + str(degrees[0])
        + "; xi<-kappa "
        + str(degrees[1])
        + "; kappa<-xi "
        + str(degrees[2])
        + "; kappa<-kappa "
        + str(degrees[3])
    )
print("MAX_LOG_TRANSFER_DEGREE := ", max_transfer_degree, sep="")

if max_transfer_degree <= 0:
    print("BOUNDED_LOG_TRANSFER := certified for integer n>=3")
    print(
        "LOG_MAJORANT_THEOREM := because the lag set is finite and every "
        "rational transfer coefficient is pole-free on integer n>=3 with "
        "degree at infinity <=0, there is B<infinity bounding all "
        "homogeneous transfer matrices; choosing Q so that "
        "sum_{j=1}^J B*Q^(-j)<1 closes a geometric induction"
    )
    print(
        "NONLOG_FORCING_THEOREM := the exponent-derivative source has "
        "finite lag and polynomial degree <=3; polynomial times Q0^n is "
        "bounded by C*Q1^n for every Q1>Q0, so the same contraction "
        "majorant closes for the ordinary coefficients after enlarging Q"
    )
    print(
        "COEFFICIENT_BOUND := exists C,Q>0 such that "
        "||u_n||+||v_n|| <= C*Q^n for all n"
    )
    print(
        "CONVERGENCE_THEOREM := for every fixed M>0 and beta!=0 in the "
        "certified exceptional branch, there exists rho>0 such that the "
        "two coefficient series converge absolutely for |x|<rho; on any "
        "fixed branch of log(x), the Frobenius expression is a genuine "
        "local solution on 0<|x|<rho"
    )
    print(
        "RESULT := exceptional logarithmic Frobenius convergence proved"
    )
    print(
        "BOUNDARY := no explicit optimal convergence radius is claimed; "
        "analytic continuation beyond the local punctured neighborhood, "
        "global boundary conditions, and physical instability remain unproved"
    )
    print(
        "NEXT_ACTIONS := no additional finite-order or convergence probe is needed"
    )
else:
    print(
        "BOUNDARY := unscaled kernel-coordinate transfer has positive "
        "polynomial growth and the geometric majorant is not yet closed"
    )
    print(
        "NEXT_ACTIONS := rescale only the kernel coordinate by the "
        "displayed maximal polynomial degree and recompute the transfer"
    )
    raise SystemExit(3)

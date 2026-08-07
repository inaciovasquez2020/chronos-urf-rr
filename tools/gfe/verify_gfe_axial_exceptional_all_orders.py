#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import sympy as s

if len(sys.argv) != 2:
    raise SystemExit(
        "MISSING_OBJECT := canonical GfE source argument"
    )

source = Path(sys.argv[1])
if not source.is_file():
    raise SystemExit(f"MISSING_OBJECT := {source}")

text = source.read_text()
match = re.search(
    r'''cat >"\$tmp_py" <<'PY_CORE'\n(.*?)\nPY_CORE\n''',
    text,
    re.S,
)
if match is None:
    raise SystemExit(
        "MISSING_OBJECT := PY_CORE in canonical GfE source"
    )

core = match.group(1)
sentinel = "\nH1_220_LEADING ="
cut = core.find(sentinel)
if cut < 0:
    raise SystemExit(
        "MISSING_OBJECT := H1_220_LEADING source sentinel"
    )

prefix = core[:cut]
ns: dict[str, object] = {}
exec(
    compile(prefix, str(source) + ":PY_CORE_PREFIX", "exec"),
    ns,
)

required = [
    "r",
    "M",
    "beta",
    "omega",
    "H0_radial",
    "H1_radial_beta2",
    "E0_CORR_FOURIER",
    "E1_CORR_FOURIER",
]
missing = [name for name in required if name not in ns]
if missing:
    raise SystemExit(
        "MISSING_OBJECT := current GfE operator symbols: "
        + ", ".join(missing)
    )

r = ns["r"]
M = ns["M"]
beta = ns["beta"]
omega = ns["omega"]
H0 = ns["H0_radial"]
H1 = ns["H1_radial_beta2"]
E0_corr = ns["E0_CORR_FOURIER"]
E1_corr = ns["E1_CORR_FOURIER"]

x = s.symbols("x", positive=True)
p = s.symbols("p")
n = s.symbols("n", integer=True, positive=True)
a, b = s.symbols("a b")
I = s.I

f = 1 - 2*M/r
Q = -I*omega*H1 - s.diff(H0, r) + 2*H0/r
A0 = s.diff(Q, r) + 2*Q/r + 4*H0/(f*r**2)
A1 = I*omega*Q - 4*f*H1/r**2

E0 = s.expand(6*A0 + beta**2*E0_corr)
E1 = s.expand(6*A1 + beta**2*E1_corr)

def falling(q, k: int):
    out = s.Integer(1)
    for j in range(k):
        out *= q - j
    return s.expand(out)

def quotient_trial(expr, aa, bb, q):
    derivative_replacements = {}
    for derivative in expr.atoms(s.Derivative):
        if any(variable != r for variable in derivative.variables):
            continue
        order = len(derivative.variables)
        if derivative.expr == H0:
            derivative_replacements[derivative] = (
                aa * falling(q, order) / x**order
            )
        elif derivative.expr == H1:
            derivative_replacements[derivative] = (
                bb * falling(q - 1, order) / x**(order + 1)
            )

    out = expr.xreplace(derivative_replacements)
    out = out.xreplace({
        H0: aa,
        H1: bb / x,
    })
    out = out.subs({
        r: 2*M + x,
        omega: I/(4*M),
    })
    return s.cancel(s.together(out))

q0 = quotient_trial(E0, a, b, p)
q1 = quotient_trial(E1, a, b, p)

def laurent_coeff(expr, power: int):
    return s.factor(
        s.cancel(
            s.residue(
                s.together(expr / x**(power + 1)),
                x,
                0,
            )
        )
    )

def block(lag: int):
    row0 = laurent_coeff(q0, -3 + lag)
    row1 = laurent_coeff(q1, -2 + lag)
    matrix = s.Matrix([
        [s.diff(row0, a), s.diff(row0, b)],
        [s.diff(row1, a), s.diff(row1, b)],
    ])
    return matrix.applyfunc(
        lambda z: s.factor(s.cancel(s.together(z)))
    )

B0 = block(0)
B1 = block(1)
B2 = block(2)

alpha = s.Rational(1, 2)
pn = alpha + n

A_expected = s.Matrix([
    [
        -beta**2*n*(n - 1)*(2*n - 3)*(2*n + 1)/(8*M**3),
        beta**2*n*(n - 1)*(2*n - 3)/(16*M**4),
    ],
    [
        beta**2*n*(n - 1)*(2*n + 1)/(16*M**4),
        -beta**2*n*(n - 1)/(32*M**5),
    ],
])

A_derived = B0.subs(p, pn).applyfunc(
    lambda z: s.factor(s.cancel(s.together(z)))
)

if any(
    s.factor(s.cancel(s.together(A_derived[i, j] - A_expected[i, j]))) != 0
    for i in range(2)
    for j in range(2)
):
    print("DERIVED_A_nn :=", A_derived)
    print("EXPECTED_A_nn :=", A_expected)
    raise SystemExit(
        "BOUNDARY := current canonical GfE source does not reproduce "
        "the saved all-orders leading block"
    )

l_n = s.Matrix([1, 2*M*(2*n - 3)])
r_n = s.Matrix([1, 2*M*(2*n + 1)])
r_prev = s.Matrix([1, 2*M*(2*n - 1)])

right_residual = (A_derived*r_n).applyfunc(
    lambda z: s.factor(s.cancel(s.together(z)))
)
left_residual = (l_n.T*A_derived).applyfunc(
    lambda z: s.factor(s.cancel(s.together(z)))
)
assert right_residual == s.zeros(2, 1)
assert left_residual == s.zeros(1, 2)

adjacent = B1.subs(p, alpha + n - 1)
gamma_derived = s.factor(
    s.cancel(
        s.together(
            (l_n.T * adjacent * r_prev)[0]
        )
    )
)
gamma_expected = (
    2*beta**2*(n - 1)**2
    *(12*n**2 - 24*n - 5)
    /(3*M**4)
)
assert s.factor(
    s.cancel(s.together(gamma_derived - gamma_expected))
) == 0

D_nn = s.diff(B0, p).subs(p, pn)
log_kernel_decoupling = s.factor(
    s.cancel(
        s.together(
            (l_n.T * D_nn * r_n)[0]
        )
    )
)
assert log_kernel_decoupling == 0

p0 = alpha
p1 = alpha + 1
p2 = alpha + 2

B0_p0 = B0.subs(p, p0).applyfunc(s.simplify)
B0_p1 = B0.subs(p, p1).applyfunc(s.simplify)
B0_p2 = B0.subs(p, p2).applyfunc(s.simplify)

assert B0_p0 == s.zeros(2)
assert B0_p1 == s.zeros(2)
assert s.factor(B0_p2.det()) == 0
assert B0_p2.rank() == 1

c1 = s.symbols("c1")
a1 = s.symbols("a1")

v1 = c1*s.Matrix([1, -2*M])
u0 = c1*s.Matrix([
    s.Rational(3, 5)*M,
    s.Rational(6, 5)*M**2,
])

seed_order1 = (
    B1.subs(p, p0)*u0
    + s.diff(B0, p).subs(p, p1)*v1
).applyfunc(lambda z: s.factor(s.cancel(s.together(z))))
assert seed_order1 == s.zeros(2, 1)

l2 = s.Matrix([1, 2*M])
log2_source = B1.subs(p, p1)*v1
assert s.factor(
    s.cancel(s.together((l2.T*log2_source)[0]))
) == 0

v2_part = s.Matrix([
    -2*c1*(36*M**4 - 19*beta**2)/(15*M*beta**2),
    0,
])
log2_residual = (
    B0_p2*v2_part + log2_source
).applyfunc(lambda z: s.factor(s.cancel(s.together(z))))
assert log2_residual == s.zeros(2, 1)

u1 = s.Matrix([
    a1,
    -2*M*a1 - s.Rational(362, 25)*M*c1,
])
nonlog2_source = (
    B1.subs(p, p1)*u1
    + B2.subs(p, p0)*u0
    + s.diff(B0, p).subs(p, p2)*v2_part
    + s.diff(B1, p).subs(p, p1)*v1
)
nonlog2_compatibility = s.factor(
    s.cancel(
        s.together(
            (l2.T*nonlog2_source)[0]
        )
    )
)
assert nonlog2_compatibility == 0

m = s.symbols("m", integer=True, nonnegative=True)
shifted_gamma_poly = s.expand(
    ((n - 1)**2*(12*n**2 - 24*n - 5)).subs(n, m + 3)
)
expected_shifted = (m + 2)**2*(12*m**2 + 48*m + 31)
assert s.expand(shifted_gamma_poly - expected_shifted) == 0

compat_det = s.factor(gamma_expected**2)
expected_det = (
    4*beta**4*(n - 1)**4
    *(12*n**2 - 24*n - 5)**2
    /(9*M**8)
)
assert s.factor(
    s.cancel(s.together(compat_det - expected_det))
) == 0

source_sha = hashlib.sha256(source.read_bytes()).hexdigest()

print("SOURCE :=", source)
print("SOURCE_SHA256 :=", source_sha)
print("EXCEPTIONAL_RESONANCE := omega=I/(4*M); alpha=1/2")
print("FORMAL_SERIES_ANSATZ := x^(1/2)*(u_0 + sum_{n>=1} x^n*(u_n+v_n*log(x)))")
print("LOW_ORDER_SEED := certified directly from current canonical source through total Laurent order 2")
print("SELECTED_FIRST_LOG_DIRECTION := v_1 = c1*(1,-2*M)")
print("SELECTED_LEADING_ORDINARY_AMPLITUDE := u_0 = c1*(3*M/5,6*M^2/5)")
print("ORDER_n_LEADING_BLOCK :=", A_derived)
print("ORDER_n_RIGHT_KERNEL := (1,2*M*(2*n+1))")
print("ORDER_n_LEFT_PROJECTOR := (1,2*M*(2*n-3))")
print("ADJACENT_KERNEL_COUPLING_GAMMA_n :=", gamma_derived)
print("LOG_KERNEL_DECOUPLING := l_n^T*D_nn*r_n = 0")
print("ORDER_n_COMPATIBILITY_DETERMINANT :=", compat_det)
print("NONVANISHING_CERTIFICATE := (m+2)^4*(12*m^2+48*m+31)^2 > 0 for integer m>=0")
print(
    "INDUCTION_STEP := log compatibility uniquely fixes kappa_(n-1); "
    "non-log compatibility uniquely fixes mu_(n-1); "
    "the current kernel pair (kappa_n,mu_n) remains free"
)
print(
    "RESULT := the current canonical GfE source certifies a formal "
    "exceptional logarithmic Frobenius solution to every Laurent order"
)
print(
    "BOUNDARY := coefficient growth, convergence, analytic continuation, "
    "global boundary conditions, and physical instability are not proved"
)
print(
    "NEXT_ACTIONS := preserve the certified formal theorem in standalone LaTeX"
)

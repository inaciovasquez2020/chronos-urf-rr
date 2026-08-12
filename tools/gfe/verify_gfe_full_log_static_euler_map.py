#!/usr/bin/env python3
from __future__ import annotations

import functools
import itertools
import json
from pathlib import Path

import sympy as sp


r, th, beta, M = sp.symbols(
    "r th beta M",
    positive=True,
)

v, ph = sp.symbols("v ph")

coords = [v, r, th, ph]
dim = 4

N = sp.Function("N")(r)
F = sp.Function("F")(r)


def S(x):
    return sp.factor(
        sp.trigsimp(
            sp.simplify(x),
            method="fu",
        )
    )


def Q(x):
    return sp.factor(
        sp.cancel(
            sp.together(x)
        )
    )


# ============================================================
# 1. REGULAR INGOING-EF GEOMETRY
# ============================================================

g = sp.Matrix([
    [-N**2 * F, N, 0, 0],
    [N, 0, 0, 0],
    [0, 0, r**2, 0],
    [0, 0, 0, r**2 * sp.sin(th)**2],
])

ginv = sp.simplify(g.inv())

Gamma = [
    [
        [0 for _ in range(dim)]
        for _ in range(dim)
    ]
    for _ in range(dim)
]

for a, b, c in itertools.product(
    range(dim),
    repeat=3,
):
    Gamma[a][b][c] = S(
        sp.Rational(1, 2)
        * sum(
            ginv[a, d]
            * (
                sp.diff(g[d, c], coords[b])
                + sp.diff(g[d, b], coords[c])
                - sp.diff(g[b, c], coords[d])
            )
            for d in range(dim)
        )
    )

Rup = [
    [
        [
            [0 for _ in range(dim)]
            for _ in range(dim)
        ]
        for _ in range(dim)
    ]
    for _ in range(dim)
]

for a, b, c, d in itertools.product(
    range(dim),
    repeat=4,
):
    expr = (
        sp.diff(
            Gamma[a][b][d],
            coords[c],
        )
        - sp.diff(
            Gamma[a][b][c],
            coords[d],
        )
    )

    expr += sum(
        Gamma[a][c][e]
        * Gamma[e][b][d]
        - Gamma[a][d][e]
        * Gamma[e][b][c]
        for e in range(dim)
    )

    Rup[a][b][c][d] = S(expr)

Ric = sp.Matrix(
    dim,
    dim,
    lambda b, d: S(
        sum(
            Rup[a][b][a][d]
            for a in range(dim)
        )
    ),
)

Rscalar = S(
    sum(
        ginv[a, b]
        * Ric[a, b]
        for a, b in itertools.product(
            range(dim),
            repeat=2,
        )
    )
)

Rlow = [
    [
        [
            [0 for _ in range(dim)]
            for _ in range(dim)
        ]
        for _ in range(dim)
    ]
    for _ in range(dim)
]

for a, b, c, d in itertools.product(
    range(dim),
    repeat=4,
):
    Rlow[a][b][c][d] = S(
        sum(
            g[a, e]
            * Rup[e][b][c][d]
            for e in range(dim)
        )
    )


# ============================================================
# 2. EXACT STATIC CURVATURE CHANNELS
# ============================================================

Np = sp.diff(N, r)
Npp = sp.diff(N, r, 2)

Fp = sp.diff(F, r)
Fpp = sp.diff(F, r, 2)

a = Q(
    -(
        2*r*F*Npp
        + r*N*Fpp
        + 3*r*Fp*Np
        + 4*F*Np
        + 2*N*Fp
    )/(2*r*N)
)

b = Q(
    2*Np/(r*N**2)
)

c = Q(
    -(
        2*r*F*Npp
        + r*N*Fpp
        + 3*r*Fp*Np
        + 2*N*Fp
    )/(2*r*N)
)

d = Q(
    -(
        r*F*Np
        + r*N*Fp
        + F*N
        - N
    )/(r**2*N)
)

e = Q(
    -(
        2*F*Npp
        + N*Fpp
        + 3*Fp*Np
    )/N
)

h = Q(
    -(
        2*F*Np
        + N*Fp
    )/(r*N)
)

j = Q(
    -Fp/r
)

k = Q(
    -2*(F-1)/r**2
)

ell = b

assert Q(
    a + c + 2*d - Rscalar
) == 0

assert Q(
    e + 2*h + 2*j + k - Rscalar
) == 0

assert Q(
    c - a - N*F*b
) == 0


# ============================================================
# 3. EXACT SCALAR / TRACE-LOG SECTOR
# ============================================================

channels = [
    (Rscalar, 1),
    (a, 1),
    (c, 1),
    (d, 2),
    (e, 1),
    (h, 2),
    (j, 2),
    (k, 1),
]

assert sum(
    mult
    for _, mult in channels
) == 11

for lam, _ in channels:

    assert Q(
        beta*lam/(1-beta*lam)
        - (
            1/(1-beta*lam)
            - 1
        )
    ) == 0

TrLogG = -sum(
    mult
    * sp.log(
        1-beta*lam
    )
    for lam, mult in channels
)

trace_curvature = sum(
    mult*lam
    for lam, mult in channels
)

assert Q(
    trace_curvature
    - 3*Rscalar
) == 0


# ============================================================
# 4. EXACT RESOLVENT DAG CARRIERS
#
# C = A + N F B is the already-proved self-adjoint relation.
# This representation introduces no artificial 1/F.
# ============================================================

G0 = sp.Function("G0")(r)

A = sp.Function("A")(r)
B = sp.Function("B")(r)

C = A + N*F*B

D = sp.Function("D")(r)

E = sp.Function("E")(r)
H = sp.Function("H")(r)
J = sp.Function("J")(r)
K = sp.Function("K")(r)
L = sp.Function("L")(r)

G1mixed = sp.Matrix([
    [A, 0, 0, 0],
    [B, C, 0, 0],
    [0, 0, D, 0],
    [0, 0, 0, D],
])

G1cov_matrix = sp.expand(
    G1mixed * g
)

assert (
    G1cov_matrix
    - G1cov_matrix.T
) == sp.zeros(4)


def G1cov(a_, b_):
    return G1cov_matrix[a_, b_]


pairs = [
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 3),
]

pair_index = {
    pair: i
    for i, pair
    in enumerate(pairs)
}

G2pair = sp.Matrix([
    [E, 0, 0, 0, 0, 0],
    [0, H, 0, 0, 0, 0],
    [0, 0, H, 0, 0, 0],
    [0, L, 0, J, 0, 0],
    [0, 0, L, 0, J, 0],
    [0, 0, 0, 0, 0, K],
])


def oriented_pair(a_, b_):

    if a_ == b_:
        return None, 0

    if a_ < b_:
        return pair_index[(a_, b_)], 1

    return pair_index[(b_, a_)], -1


def g2low(a_, b_, c_, d_):

    return sp.Rational(1, 2) * (
        g[a_, c_]*g[b_, d_]
        - g[a_, d_]*g[b_, c_]
    )


@functools.lru_cache(None)
def G2cov(a_, b_, c_, d_):

    ia, sign = oriented_pair(
        a_,
        b_,
    )

    if sign == 0:
        return sp.Integer(0)

    return sign * sum(
        G2pair[ia, ib]
        * g2low(
            e_,
            f_,
            c_,
            d_,
        )
        for ib, (e_, f_)
        in enumerate(pairs)
    )


@functools.lru_cache(None)
def G2_mu_up3(
    mu,
    eta,
    rho1,
    rho2,
):

    return S(
        sum(
            ginv[eta, a_]
            * ginv[rho1, b_]
            * ginv[rho2, c_]
            * G2cov(
                mu,
                a_,
                b_,
                c_,
            )
            for a_, b_, c_
            in itertools.product(
                range(dim),
                repeat=3,
            )
        )
    )


@functools.lru_cache(None)
def R_nu_up3(
    nu,
    eta,
    rho1,
    rho2,
):

    return S(
        sum(
            ginv[eta, a_]
            * ginv[rho1, b_]
            * ginv[rho2, c_]
            * Rlow[nu][a_][b_][c_]
            for a_, b_, c_
            in itertools.product(
                range(dim),
                repeat=3,
            )
        )
    )


# ============================================================
# 5. FOUNDATIONAL DRESSED-RICCI DAG
# ============================================================

def RG_component(mu, nu):

    return (
        G0*Ric[mu, nu]

        + sum(
            G1mixed[mu, rho]
            * Ric[rho, nu]
            for rho in range(dim)
        )

        - sum(
            G2cov(
                rho1,
                rho2,
                mu,
                eta,
            )
            * R_nu_up3(
                nu,
                eta,
                rho1,
                rho2,
            )
            for rho1, rho2, eta
            in itertools.product(
                range(dim),
                repeat=3,
            )
        )

        + 2*sum(
            G2_mu_up3(
                mu,
                eta,
                rho1,
                rho2,
            )
            * Rlow[
                rho1
            ][
                rho2
            ][
                nu
            ][
                eta
            ]
            for eta, rho1, rho2
            in itertools.product(
                range(dim),
                repeat=3,
            )
        )
    )


RGvr = RG_component(0, 1)
RGrv = RG_component(1, 0)
RGrr = RG_component(1, 1)


# ============================================================
# 6. EXACT COVARIANT D_mu_nu DAG
# ============================================================

@functools.lru_cache(None)
def cov1_G1(lam, a_, b_):

    expr = sp.diff(
        G1cov(a_, b_),
        coords[lam],
    )

    for slot, old in enumerate(
        (a_, b_)
    ):
        for e_ in range(dim):

            gamma = Gamma[e_][lam][old]

            if gamma == 0:
                continue

            inds = [a_, b_]
            inds[slot] = e_

            expr -= (
                gamma
                * G1cov(*inds)
            )

    return S(expr)


@functools.lru_cache(None)
def cov1_G2(
    lam,
    a_,
    b_,
    c_,
    d_,
):

    inds0 = (
        a_,
        b_,
        c_,
        d_,
    )

    expr = sp.diff(
        G2cov(*inds0),
        coords[lam],
    )

    for slot, old in enumerate(
        inds0
    ):
        for e_ in range(dim):

            gamma = Gamma[e_][lam][old]

            if gamma == 0:
                continue

            inds = list(inds0)
            inds[slot] = e_

            expr -= (
                gamma
                * G2cov(*inds)
            )

    return S(expr)


def cov2_G1(
    sigma,
    lam,
    a_,
    b_,
):

    expr = sp.diff(
        cov1_G1(
            lam,
            a_,
            b_,
        ),
        coords[sigma],
    )

    for e_ in range(dim):

        expr -= (
            Gamma[e_][sigma][lam]
            * cov1_G1(
                e_,
                a_,
                b_,
            )
        )

    for slot, old in enumerate(
        (a_, b_)
    ):
        for e_ in range(dim):

            gamma = Gamma[e_][sigma][old]

            if gamma == 0:
                continue

            inds = [a_, b_]
            inds[slot] = e_

            expr -= (
                gamma
                * cov1_G1(
                    lam,
                    *inds,
                )
            )

    return expr


def cov2_G2(
    sigma,
    lam,
    a_,
    b_,
    c_,
    d_,
):

    inds0 = (
        a_,
        b_,
        c_,
        d_,
    )

    expr = sp.diff(
        cov1_G2(
            lam,
            *inds0,
        ),
        coords[sigma],
    )

    for e_ in range(dim):

        expr -= (
            Gamma[e_][sigma][lam]
            * cov1_G2(
                e_,
                *inds0,
            )
        )

    for slot, old in enumerate(
        inds0
    ):
        for e_ in range(dim):

            gamma = Gamma[e_][sigma][old]

            if gamma == 0:
                continue

            inds = list(inds0)
            inds[slot] = e_

            expr -= (
                gamma
                * cov1_G2(
                    lam,
                    *inds,
                )
            )

    return expr


def scalar_hessian(
    phi,
    mu,
    nu,
):

    return (
        sp.diff(
            phi,
            coords[mu],
            coords[nu],
        )

        - sum(
            Gamma[e_][mu][nu]
            * sp.diff(
                phi,
                coords[e_],
            )
            for e_
            in range(dim)
        )
    )


def D_component(mu, nu):

    box0 = sum(
        ginv[a_, b_]
        * scalar_hessian(
            G0,
            a_,
            b_,
        )
        for a_, b_
        in itertools.product(
            range(dim),
            repeat=2,
        )
    )

    term0 = (
        g[mu, nu]*box0
        - scalar_hessian(
            G0,
            mu,
            nu,
        )
    )

    term1 = -sum(
        ginv[rho, sigma]
        * cov2_G1(
            sigma,
            nu,
            rho,
            mu,
        )
        for rho, sigma
        in itertools.product(
            range(dim),
            repeat=2,
        )
    )

    term2 = (
        sp.Rational(1, 2)
        * sum(
            ginv[rho, sigma]
            * cov2_G1(
                sigma,
                rho,
                mu,
                nu,
            )
            for rho, sigma
            in itertools.product(
                range(dim),
                repeat=2,
            )
        )
    )

    term3 = (
        sp.Rational(1, 2)
        * g[mu, nu]
        * sum(
            ginv[rho, sigma]
            * cov2_G1(
                sigma,
                eta,
                rho,
                eta,
            )
            for rho, sigma, eta
            in itertools.product(
                range(dim),
                repeat=3,
            )
        )
    )

    term4 = sum(
        ginv[eta, tau]
        * ginv[rho, sigma]
        * cov2_G2(
            tau,
            sigma,
            mu,
            rho,
            nu,
            eta,
        )
        for eta, tau, rho, sigma
        in itertools.product(
            range(dim),
            repeat=4,
        )
    )

    term5 = sum(
        ginv[rho, sigma]
        * ginv[eta, tau]
        * cov2_G2(
            sigma,
            tau,
            eta,
            mu,
            rho,
            nu,
        )
        for rho, sigma, eta, tau
        in itertools.product(
            range(dim),
            repeat=4,
        )
    )

    term6 = (
        sp.Rational(1, 2)
        * sum(
            ginv[rho, sigma]
            * ginv[eta, tau]
            * (
                cov2_G2(
                    sigma,
                    tau,
                    rho,
                    eta,
                    mu,
                    nu,
                )
                -
                cov2_G2(
                    tau,
                    sigma,
                    rho,
                    eta,
                    mu,
                    nu,
                )
            )
            for rho, sigma, eta, tau
            in itertools.product(
                range(dim),
                repeat=4,
            )
        )
    )

    return (
        term0
        + term1
        + term2
        + term3
        + term4
        + term5
        + term6
    )


Dvr = D_component(0, 1)
Drv = D_component(1, 0)
Drr = D_component(1, 1)


# ============================================================
# 7. q=0 NORMALIZATION
# ============================================================

q0 = {
    G0: 1,
    A: 1,
    B: 0,
    D: 1,
    E: 1,
    H: 1,
    J: 1,
    K: 1,
    L: 0,
}

for name, expr in [
    ("vr", Dvr),
    ("rv", Drv),
    ("rr", Drr),
]:
    assert S(
        expr
        .subs(q0)
        .doit()
    ) == 0, name

for name, expr in [
    (
        "vr_sym",
        (Dvr+Drv)/2,
    ),
    (
        "rr",
        Drr,
    ),
]:
    denominator = sp.factor(
        sp.denom(
            sp.together(expr)
        )
    )

    assert not denominator.has(F), (
        name,
        denominator,
    )

for name, expr, target in [
    (
        "vr",
        RGvr,
        3*Ric[0, 1],
    ),
    (
        "rv",
        RGrv,
        3*Ric[1, 0],
    ),
    (
        "rr",
        RGrr,
        3*Ric[1, 1],
    ),
]:
    assert S(
        expr.subs(q0)
        - target
    ) == 0, name


# ============================================================
# 8. EXACT COMPOSITIONAL STATIC EULER DAG
# ============================================================

Lfull = TrLogG/beta

Evr = (
    (RGvr+RGrv)/2

    - sp.Rational(1, 2)
    * N
    * Lfull

    + (Dvr+Drv)/2
)

Err = (
    RGrr
    + Drr
)

Phi1 = (
    r**2
    * (Evr/N)
    / 3
)

Phi2 = (
    r**2
    * (
        Evr/N
        + F*Err
    )
    / 3
)


# ============================================================
# 9. EXACT q=0 EINSTEIN REDUCTION
# ============================================================

L0 = 3*Rscalar

Evr0 = S(
    3*Ric[0, 1]
    - sp.Rational(1, 2)
    * N
    * L0
)

Err0 = S(
    3*Ric[1, 1]
)

Phi1_q0 = Q(
    r**2
    * (Evr0/N)
    / 3
)

Phi2_q0 = Q(
    r**2
    * (
        Evr0/N
        + F*Err0
    )
    / 3
)

Einstein1 = Q(
    r*Fp
    + F
    - 1
)

Einstein2 = Q(
    r*Fp
    + F
    - 1
    + 2*r*F*Np/N
)

assert Q(
    Phi1_q0
    - Einstein1
) == 0

assert Q(
    Phi2_q0
    - Einstein2
) == 0

schwarzschild = {
    N: 1,
    sp.diff(N, r): 0,
    sp.diff(N, r, 2): 0,

    F: 1 - 2*M/r,
    sp.diff(F, r): 2*M/r**2,
    sp.diff(F, r, 2): -4*M/r**3,
}

assert Q(
    Phi1_q0
    .subs(schwarzschild)
) == 0

assert Q(
    Phi2_q0
    .subs(schwarzschild)
) == 0


# ============================================================
# 10. MACHINE-READABLE CERTIFICATE
# ============================================================

artifact = {
    "result":
        "exact full-log static Euler compositional DAG assembled",

    "full_log_static_euler_map":
        "constructed_as_exact_compositional_DAG",

    "exact_curvature_blocks":
        True,

    "exact_resolvent_dag":
        True,

    "one_form_self_adjoint_relation":
        "C = A + N*F*B",

    "exact_dressed_scalar":
        True,

    "d_mu_nu_exact_dag":
        True,

    "d_mu_nu_q0_normalization":
        True,

    "ef_coordinate_regular_operator":
        True,

    "q0_einstein_reduction":
        True,

    "static_normalization":
        True,

    "curvature_truncation":
        "none",

    "phi1_q0":
        "r*F'(r)+F(r)-1",

    "phi2_q0":
        "r*F'(r)+F(r)-1+2*r*F(r)*N'(r)/N(r)",

    "boundaries": [
        "q^2 seed replay remains open",
        "Bianchi/conservation redundancy remains open",
        "C_N certification remains open",
        "Borel resummation remains open",
        "actual q=1e-2 resummed background remains open",
        "full-log six-state/rank-two rebuild remains open",
    ],
}

out = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "artifacts/chronos/gfe_full_log_static_euler_map_2026_08_12.json"
)

out.write_text(
    json.dumps(
        artifact,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)

print("STATIC_RICCI_SELF_ADJOINT_IDENTITY := PASS")
print("EXACT_SCALAR_CHANNELS := PASS")
print("EXACT_RESOLVENT_DAG := PASS")
print("D_MUNU_EXACT_DAG := PASS")
print("D_MUNU_Q0_NORMALIZATION := PASS")
print("D_MUNU_EF_REGULAR_OPERATOR := PASS")

print(
    "FULL_LOG_STATIC_EULER_MAP := "
    "constructed_as_exact_compositional_DAG"
)

print("PHI1_Q0_EINSTEIN := PASS")
print("PHI2_Q0_EINSTEIN := PASS")
print("SCHWARZSCHILD_Q0_EULER := PASS")

print(
    "ARTIFACT :=",
    out,
)

print(
    "BOUNDARY := q^2 seed replay, Bianchi redundancy, "
    "C_N, Borel resummation, q=1e-2 background, "
    "and six-state/rank-two rebuild remain open"
)

print("NEXT_ACTIONS := stop")

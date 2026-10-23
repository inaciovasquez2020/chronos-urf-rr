from __future__ import annotations

"""Metric-derived epsilon**2 coefficient of the six-dimensional curvature operator.

Convention: the returned second-order objects are coefficients of epsilon**2,
not second derivatives (so no extra factor of two is applied).
This module is deliberately limited to the operator coefficient; it does not
claim to derive the quadratic action.
"""

from itertools import product
import sympy as s

from gfe_polar_first_order_curvature_operator import build_first_order_operator


def build_second_order_operator():
    data = build_first_order_operator()
    x = data["coordinates"]
    g0 = data["background_metric"]
    h = data["perturbation"]
    inv0 = s.simplify(g0.inv())
    dinv = -inv0*h*inv0
    inv2 = inv0*h*inv0*h*inv0
    pairs = data["bivector_pairs"]
    G0 = {}
    dG1 = {}
    dG2 = {}
    for a,b,c in product(range(4), repeat=3):
        G0[a,b,c] = s.expand(sum(
            inv0[a,d]*(s.diff(g0[d,c],x[b])+s.diff(g0[d,b],x[c])-s.diff(g0[b,c],x[d]))
            for d in range(4)
        )/2)
        base_deriv = sum(
            s.diff(g0[d,c],x[b])+s.diff(g0[d,b],x[c])-s.diff(g0[b,c],x[d])
            for d in range(4)
        )
        perturb_deriv = sum(
            s.diff(h[d,c],x[b])+s.diff(h[d,b],x[c])-s.diff(h[b,c],x[d])
            for d in range(4)
        )
        dG1[a,b,c] = s.expand(sum(
            dinv[a,d]*(s.diff(g0[d,c],x[b])+s.diff(g0[d,b],x[c])-s.diff(g0[b,c],x[d]))
            + inv0[a,d]*(s.diff(h[d,c],x[b])+s.diff(h[d,b],x[c])-s.diff(h[b,c],x[d]))
            for d in range(4)
        )/2)
        dG2[a,b,c] = s.expand(sum(
            inv2[a,d]*(s.diff(g0[d,c],x[b])+s.diff(g0[d,b],x[c])-s.diff(g0[b,c],x[d]))
            + dinv[a,d]*(s.diff(h[d,c],x[b])+s.diff(h[d,b],x[c])-s.diff(h[b,c],x[d]))
            for d in range(4)
        )/2)

    R0 = data["background_riemann"]
    R1 = data["delta_riemann_mixed"]
    R2 = {}
    for a,b,c,d in product(range(4), repeat=4):
        R2[a,b,c,d] = s.expand(
            s.diff(dG2[a,b,d],x[c])-s.diff(dG2[a,b,c],x[d])
            + sum(
                dG2[a,c,e]*G0[e,b,d]+G0[a,c,e]*dG2[e,b,d]
                - dG2[a,d,e]*G0[e,b,c]-G0[a,d,e]*dG2[e,b,c]
                + dG1[a,c,e]*dG1[e,b,d]-dG1[a,d,e]*dG1[e,b,c]
                for e in range(4)
            )
        )
    Rlow0 = {}
    Rlow1 = data["delta_riemann_lowered"]
    Rlow2 = {}
    for a,b,c,d in product(range(4), repeat=4):
        Rlow0[a,b,c,d] = s.expand(sum(g0[a,e]*R0[e,b,c,d] for e in range(4)))
        Rlow2[a,b,c,d] = s.expand(sum(
            g0[a,e]*R2[e,b,c,d] + h[a,e]*R1[e,b,c,d]
            for e in range(4)
        ))

    Rop2 = s.zeros(6)
    for i,(a,b) in enumerate(pairs):
        for j,(c,d) in enumerate(pairs):
            acc = 0
            for e,q in product(range(4), repeat=2):
                acc += (
                    inv2[c,e]*inv0[d,q]*Rlow0[a,b,e,q]
                    + inv0[c,e]*inv2[d,q]*Rlow0[a,b,e,q]
                    + dinv[c,e]*dinv[d,q]*Rlow0[a,b,e,q]
                    + dinv[c,e]*inv0[d,q]*Rlow1[a,b,e,q]
                    + inv0[c,e]*dinv[d,q]*Rlow1[a,b,e,q]
                    + inv0[c,e]*inv0[d,q]*Rlow2[a,b,e,q]
                )
            Rop2[i,j] = s.expand(acc)
    return {
        "coordinates": x,
        "epsilon": data["epsilon"],
        "background_metric": g0,
        "perturbation": h,
        "inverse_metric_second_order": inv2,
        "christoffel_second_order": dG2,
        "riemann_mixed_second_order": R2,
        "riemann_lowered_second_order": Rlow2,
        "operator_second_order": Rop2,
        "bivector_pairs": pairs,
        "coefficient_convention": "coefficient_of_epsilon_squared",
    }


def direct_second_order_operator_comparison(data):
    """Independent exact coefficient algebra through epsilon**2; never invert g(epsilon)."""
    x = data["coordinates"]
    g0, h = data["background_metric"], data["perturbation"]
    pairs = data["bivector_pairs"]
    # Coefficients of g^{-1}: G0 - eps G0 h G0 + eps**2 G0 h G0 h G0.
    gi = [s.simplify(g0.inv()), None, None]
    gi[1] = -gi[0]*h*gi[0]
    gi[2] = gi[0]*h*gi[0]*h*gi[0]
    gm = [g0, h, s.zeros(4)]
    # Gamma[n] = 1/2 sum_{p+q=n} g^{-1}[p] * (partial g[q] + partial g[q] - partial g[q]).
    gamma = [dict() for _ in range(3)]
    for n in range(3):
        for a,b,c in product(range(4), repeat=3):
            value = 0
            for p in range(n+1):
                q = n-p
                value += sum(
                    gi[p][a,d]*(s.diff(gm[q][d,c],x[b])
                                +s.diff(gm[q][d,b],x[c])
                                -s.diff(gm[q][b,c],x[d]))
                    for d in range(4)
                )/2
            gamma[n][a,b,c] = s.expand(value)
    # R^a_{bcd}[n] from coefficient convolution of Gamma and its derivatives.
    rm = [dict() for _ in range(3)]
    for n in range(3):
        for a,b,c,d in product(range(4), repeat=4):
            value = s.diff(gamma[n][a,b,d],x[c])-s.diff(gamma[n][a,b,c],x[d])
            for p in range(n+1):
                q=n-p
                value += sum(
                    gamma[p][a,c,e]*gamma[q][e,b,d]
                    -gamma[p][a,d,e]*gamma[q][e,b,c]
                    for e in range(4)
                )
            rm[n][a,b,c,d] = s.expand(value)
    # Lower the first Riemann index by coefficient convolution.
    rl = [dict() for _ in range(3)]
    for n in range(3):
        for a,b,c,d in product(range(4), repeat=4):
            rl[n][a,b,c,d] = s.expand(sum(
                gm[p][a,e]*rm[n-p][e,b,c,d]
                for p in range(n+1) for e in range(4)
            ))
    # R_op coefficient at order two: sum gi[p] gi[q] R_low[k], p+q+k=2.
    op2 = s.zeros(6)
    for i,(a,b) in enumerate(pairs):
        for j,(c,d) in enumerate(pairs):
            value = 0
            for p,q,k in product(range(3), repeat=3):
                if p+q+k != 2:
                    continue
                value += sum(
                    gi[p][c,e]*gi[q][d,z]*rl[k][a,b,e,z]
                    for e,z in product(range(4), repeat=2)
                )
            op2[i,j] = s.expand(value)
    residuals = s.zeros(6)
    for i,j in product(range(6), repeat=2):
        residuals[i,j] = s.simplify(op2[i,j]-data["operator_second_order"][i,j])
    return residuals

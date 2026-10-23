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
    """Compare all 36 analytic entries with the epsilon**2 coefficient of exact g."""
    x, eps = data["coordinates"], data["epsilon"]
    g0, h = data["background_metric"], data["perturbation"]
    g = g0 + eps*h
    inv = g.inv()
    pairs = data["bivector_pairs"]
    G = {}
    for a,b,c in product(range(4), repeat=3):
        G[a,b,c] = s.cancel(sum(
            inv[a,d]*(s.diff(g[d,c],x[b])+s.diff(g[d,b],x[c])-s.diff(g[b,c],x[d]))
            for d in range(4)
        )/2)
    R = {}
    for a,b,c,d in product(range(4), repeat=4):
        R[a,b,c,d] = (
            s.diff(G[a,b,d],x[c])-s.diff(G[a,b,c],x[d])
            + sum(G[a,c,e]*G[e,b,d]-G[a,d,e]*G[e,b,c] for e in range(4))
        )
    Rlow = {
        (a,b,c,d): sum(g[a,z]*R[z,b,c,d] for z in range(4))
        for a,b,c,d in product(range(4), repeat=4)
    }
    op = s.zeros(6)
    for i,(a,b) in enumerate(pairs):
        for j,(c,d) in enumerate(pairs):
            op[i,j] = sum(
                inv[c,e]*inv[d,q]*Rlow[a,b,e,q]
                for e,q in product(range(4), repeat=2)
            )
    residuals = s.zeros(6)
    for i,j in product(range(6), repeat=2):
        exact_coefficient = s.diff(op[i,j],eps,2).subs(eps,0)/2
        residuals[i,j] = s.simplify(
            exact_coefficient-data["operator_second_order"][i,j]
        )
    return residuals

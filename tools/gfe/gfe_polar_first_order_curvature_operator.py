from __future__ import annotations

"""Independent first-order curvature operator for the polar l=2 metric.

This module derives the O(epsilon) tensor coefficient from the specified metric.
It intentionally does not use the repository's axial coefficient table or the
existing polar principal-part helpers.  The direct-expansion verifier is kept
as a separate path in this file.
"""

from itertools import product

import sympy as s


def build_first_order_operator():
    eps = s.symbols("epsilon", real=True)
    t, r, th, ph = s.symbols("t r theta phi", real=True)
    M = s.symbols("M", positive=True, real=True)
    H0 = s.Function("H0")(t, r)
    H1 = s.Function("H1")(t, r)
    H2 = s.Function("H2")(t, r)
    K = s.Function("K")(t, r)
    Y = s.sqrt(s.Rational(5, 16) / s.pi) * (3 * s.cos(th)**2 - 1)
    f = 1 - 2*M/r
    x = (t, r, th, ph)
    g0 = s.diag(-f, 1/f, r**2, r**2*s.sin(th)**2)
    h = s.zeros(4)
    h[0, 0] = -f*H0*Y
    h[0, 1] = h[1, 0] = H1*Y
    h[1, 1] = H2*Y/f
    h[2, 2] = r**2*K*Y
    h[3, 3] = r**2*s.sin(th)**2*K*Y
    g = g0 + eps*h
    ginv0 = s.simplify(g0.inv())
    # First-order inverse metric, derived from g*g^{-1}=I.
    delta_ginv = -ginv0*h*ginv0
    ginv1 = ginv0 + eps*delta_ginv

    def christoffel(metric, inverse):
        out = {}
        for a, b, c in product(range(4), repeat=3):
            out[a,b,c] = s.expand(sum(
                inverse[a,d] * (
                    s.diff(metric[d,c], x[b])
                    + s.diff(metric[d,b], x[c])
                    - s.diff(metric[b,c], x[d])
                ) for d in range(4)
            ) / 2)
        return out

    # Background connection and its first-order variation are calculated
    # separately; this avoids confusing an inverse-metric correction with
    # a derivative of the perturbation.
    G0 = christoffel(g0, ginv0)
    G1 = christoffel(h, ginv0)
    dG = {}
    for a,b,c in product(range(4), repeat=3):
        dG[a,b,c] = s.expand(G1[a,b,c] + sum(
            delta_ginv[a,d] * (
                s.diff(g0[d,c], x[b])
                + s.diff(g0[d,b], x[c])
                - s.diff(g0[b,c], x[d])
            ) / 2 for d in range(4)
        ))

    # R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb}
    #             + Gamma^a_{ce} Gamma^e_{db}
    #             - Gamma^a_{de} Gamma^e_{cb}.
    R0 = {}
    dR = {}
    for a,b,c,d in product(range(4), repeat=4):
        R0[a,b,c,d] = s.expand(
            s.diff(G0[a,b,d], x[c]) - s.diff(G0[a,b,c], x[d])
            + sum(G0[a,c,e]*G0[e,b,d] - G0[a,d,e]*G0[e,b,c]
                  for e in range(4))
        )
        dR[a,b,c,d] = s.expand(
            s.diff(dG[a,b,d], x[c]) - s.diff(dG[a,b,c], x[d])
            + sum(dG[a,c,e]*G0[e,b,d] + G0[a,c,e]*dG[e,b,d]
                  - dG[a,d,e]*G0[e,b,c] - G0[a,d,e]*dG[e,b,c]
                  for e in range(4))
        )

    # Lower the first index and retain the metric-lowering correction.
    dRlow = {}
    for a,b,c,d in product(range(4), repeat=4):
        dRlow[a,b,c,d] = s.expand(
            sum(h[a,e]*R0[e,b,c,d] + g0[a,e]*dR[e,b,c,d]
                for e in range(4))
        )
    pairs = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
    Rop0 = s.zeros(6)
    dRop = s.zeros(6)
    for i,(a,b) in enumerate(pairs):
        for j,(c,d) in enumerate(pairs):
            Rop0[i,j] = s.simplify(sum(
                ginv0[c,e]*ginv0[d,q]*sum(
                    g0[a,z]*R0[z,b,e,q] for z in range(4)
                ) for e in range(4) for q in range(4)
            ))
            dRop[i,j] = s.expand(sum(
                delta_ginv[c,e]*ginv0[d,q]*sum(
                    g0[a,z]*R0[z,b,e,q] for z in range(4)
                )
                + ginv0[c,e]*delta_ginv[d,q]*sum(
                    g0[a,z]*R0[z,b,e,q] for z in range(4)
                )
                + ginv0[c,e]*ginv0[d,q]*dRlow[a,b,e,q]
                for e in range(4) for q in range(4)
            ))
    return {
        "coordinates": x, "epsilon": eps, "metric": g, "background_metric": g0,
        "perturbation": h, "inverse_metric_first_order": ginv1,
        "background_riemann": R0, "delta_riemann_mixed": dR,
        "delta_riemann_lowered": dRlow, "bivector_pairs": pairs,
        "operator_background": Rop0, "operator_first_order": dRop,
    }


def verify_first_order_tensor_identities(data):
    """Return exact residuals; callers must assert all are zero."""
    x = data["coordinates"]
    eps = data["epsilon"]
    g = data["metric"]
    g0 = data["background_metric"]
    h = data["perturbation"]
    ginv = data["inverse_metric_first_order"]
    # Direct metric expansion: coefficient of epsilon in the full inverse.
    direct_inverse_residual = s.zeros(4)
    for i,j in product(range(4), repeat=2):
        direct_inverse_residual[i,j] = s.simplify(
            s.diff((g0 + eps*h).inv()[i,j], eps).subs(eps,0)
            - (ginv[i,j] - g0.inv()[i,j])
        )
    # Riemann antisymmetries and pair exchange are checked on lowered delta R.
    low = data["delta_riemann_lowered"]
    symmetry_residuals = []
    for a,b,c,d in product(range(4), repeat=4):
        symmetry_residuals.extend((
            s.simplify(low[a,b,c,d] + low[b,a,c,d]),
            s.simplify(low[a,b,c,d] + low[a,b,d,c]),
            s.simplify(low[a,b,c,d] - low[c,d,a,b]),
        ))
    return {
        "inverse_metric_direct_expansion": direct_inverse_residual,
        "riemann_symmetry_residuals": tuple(symmetry_residuals),
    }



def direct_epsilon_expansion_comparison(data, progress=None):
    """Independently expand the exact metric-derived tensors in epsilon.

    This deliberately recomputes the inverse metric, connection, mixed Riemann,
    lowered Riemann, and all 36 bivector-operator entries from g(epsilon).
    It is expensive by design; callers must run it and assert every residual
    is exactly zero before treating the first-order gate as passed.
    """
    def report(stage, residuals, count):
        if progress is not None:
            progress(stage, residuals, count)

    eps = data["epsilon"]
    x = data["coordinates"]
    g = data["metric"]
    g0 = data["background_metric"]
    pairs = data["bivector_pairs"]
    inv_exact = g.inv()

    def gamma(metric, inverse):
        result = {}
        for a, b, c in product(range(4), repeat=3):
            result[a,b,c] = s.cancel(sum(
                inverse[a,d] * (
                    s.diff(metric[d,c], x[b])
                    + s.diff(metric[d,b], x[c])
                    - s.diff(metric[b,c], x[d])
                ) for d in range(4)
            ) / 2)
        return result

    G = gamma(g, inv_exact)
    Rexact = {}
    for a,b,c,d in product(range(4), repeat=4):
        Rexact[a,b,c,d] = (
            s.diff(G[a,b,d], x[c]) - s.diff(G[a,b,c], x[d])
            + sum(G[a,c,e]*G[e,b,d] - G[a,d,e]*G[e,b,c]
                  for e in range(4))
        )
    Rlow_exact = {}
    for a,b,c,d in product(range(4), repeat=4):
        Rlow_exact[a,b,c,d] = sum(
            g[a,z]*Rexact[z,b,c,d] for z in range(4)
        )

    # Directly extract d/d epsilon at epsilon=0 from the exact tensors.
    direct_dR = {
        key: s.diff(value, eps).subs(eps, 0)
        for key, value in Rexact.items()
    }
    direct_dRlow = {
        key: s.diff(value, eps).subs(eps, 0)
        for key, value in Rlow_exact.items()
    }
    analytic_dR = data["delta_riemann_mixed"]
    analytic_dRlow = data["delta_riemann_lowered"]
    riemann_residuals = {
        key: s.simplify(direct_dR[key] - analytic_dR[key])
        for key in analytic_dR
    }
    report("mixed_riemann_direct_expansion", riemann_residuals, len(riemann_residuals))
    lowered_riemann_residuals = {
        key: s.simplify(direct_dRlow[key] - analytic_dRlow[key])
        for key in analytic_dRlow
    }
    report("lowered_riemann_direct_expansion", lowered_riemann_residuals, len(lowered_riemann_residuals))

    Rop_exact = s.zeros(6)
    for i, (a,b) in enumerate(pairs):
        for j, (c,d) in enumerate(pairs):
            Rop_exact[i,j] = sum(
                inv_exact[c,e]*inv_exact[d,q]*Rlow_exact[a,b,e,q]
                for e in range(4) for q in range(4)
            )
    direct_dRop = s.zeros(6)
    for i,j in product(range(6), repeat=2):
        direct_dRop[i,j] = s.diff(Rop_exact[i,j], eps).subs(eps, 0)
    operator_residuals = s.zeros(6)
    analytic_dRop = data["operator_first_order"]
    for i,j in product(range(6), repeat=2):
        operator_residuals[i,j] = s.simplify(
            direct_dRop[i,j] - analytic_dRop[i,j]
        )

    report("operator_direct_expansion", operator_residuals, 36)

    # Isolate the two inverse-metric variation terms separately.
    h = data["perturbation"]
    inv0 = g0.inv()
    dinv = -inv0*h*inv0
    inverse_term_residuals = (s.zeros(6), s.zeros(6))
    inverse_terms = (inverse_term_residuals[0], inverse_term_residuals[1])
    for i, (a,b) in enumerate(pairs):
        for j, (c,d) in enumerate(pairs):
            term1 = sum(
                dinv[c,e]*inv0[d,q]*sum(
                    g0[a,z]*data["background_riemann"][z,b,e,q]
                    for z in range(4)
                )
                for e in range(4) for q in range(4)
            )
            term2 = sum(
                inv0[c,e]*dinv[d,q]*sum(
                    g0[a,z]*data["background_riemann"][z,b,e,q]
                    for z in range(4)
                )
                for e in range(4) for q in range(4)
            )
            inverse_terms[0][i,j] = s.simplify(
                s.diff(sum(
                    inv_exact[c,e]*inv0[d,q]*sum(
                        g0[a,z]*data["background_riemann"][z,b,e,q]
                        for z in range(4)
                    )
                    for e in range(4) for q in range(4)
                ), eps).subs(eps, 0) - term1
            )
            inverse_terms[1][i,j] = s.simplify(
                s.diff(sum(
                    inv0[c,e]*inv_exact[d,q]*sum(
                        g0[a,z]*data["background_riemann"][z,b,e,q]
                        for z in range(4)
                    )
                    for e in range(4) for q in range(4)
                ), eps).subs(eps, 0) - term2
            )

    report("first_inverse_metric_variation_term", inverse_terms[0], 36)
    report("second_inverse_metric_variation_term", inverse_terms[1], 36)

    return {
        "riemann_component_count": len(riemann_residuals),
        "riemann_residuals": riemann_residuals,
        "lowered_riemann_component_count": len(lowered_riemann_residuals),
        "lowered_riemann_residuals": lowered_riemann_residuals,
        "operator_entry_count": 36,
        "operator_residuals": operator_residuals,
        "first_inverse_metric_term_residuals": inverse_terms[0],
        "second_inverse_metric_term_residuals": inverse_terms[1],
    }


def verify_background_operator(data):
    """Compare the six background diagonal entries with the contract values."""
    M, = (s.symbols("M", positive=True),)
    r = data["coordinates"][1]
    expected = s.diag(
        2*M/r**3, -M/r**3, -M/r**3,
        -M/r**3, -M/r**3, 2*M/r**3
    )
    actual = data["operator_background"]
    return s.Matrix(6, 6, lambda i,j: s.simplify(actual[i,j]-expected[i,j]))

from __future__ import annotations

"""Exact x=cos(theta) reduction for axisymmetric spherical densities.

The input is the full theta-density, including the spherical measure sin(theta).
No numerical quadrature or expression serialization is used.
"""
import sympy as sp


def reduce_spherical_density(raw_density, theta):
    """Return (x, polynomial) for raw_density dtheta after phi integration.

    The returned polynomial is the theta integrand with dtheta converted to dx:
    raw_density/sin(theta), expressed in x=cos(theta). The azimuthal factor
    2*pi is intentionally applied by integrate_spherical_density.
    """
    x = sp.Symbol("x_ang", real=True)
    u = sp.Symbol("sin_theta_aux", real=True)
    sine = sp.sin(theta)
    cosine = sp.cos(theta)

    # The spherical integral uses theta in [0, pi], so sin(theta) >= 0.
    # The metric determinant can simplify sqrt(sin(theta)**2) to Abs(sin(theta));
    # normalize that domain-dependent factor before removing the measure.
    raw_density = raw_density.xreplace({sp.Abs(sine): sine})

    # Keep sine as an algebraic auxiliary variable. This handles positive and
    # negative even powers uniformly, without trigonometric rewriting that can
    # introduce cos(2*theta) or cos(4*theta). Refuse any odd power rather than
    # silently selecting a square-root branch.
    reduced = sp.cancel(sp.together(raw_density / sine))
    reduced = sp.cancel(sp.together(reduced.subs(cosine, x).subs(sine, u)))
    numerator, denominator = sp.fraction(sp.cancel(sp.together(reduced)))
    try:
        numerator_poly = sp.Poly(numerator, u, domain="EX")
        denominator_poly = sp.Poly(denominator, u, domain="EX")
    except sp.PolynomialError as exc:
        raise ValueError("angular expression is not rational in sin(theta)") from exc

    def eliminate_even_sine(poly):
        result = sp.Integer(0)
        for (power,), coefficient in poly.terms():
            if power % 2:
                raise ValueError(f"odd sin(theta) power survives measure removal: {power}")
            result += coefficient * (1 - x**2)**(power // 2)
        return sp.expand(result)

    numerator_x = eliminate_even_sine(numerator_poly)
    denominator_x = eliminate_even_sine(denominator_poly)
    reduced_x = sp.cancel(sp.together(numerator_x / denominator_x))
    if reduced_x.has(u, sine, cosine):
        raise ValueError("angular reduction left unresolved trigonometric auxiliaries")
    numerator_x, denominator_x = sp.fraction(reduced_x)
    try:
        polynomial = sp.Poly(numerator_x, x, domain="EX")
        denominator_poly = sp.Poly(denominator_x, x, domain="EX")
    except sp.PolynomialError as exc:
        raise ValueError("angular dependence is not polynomial/rational in x=cos(theta)") from exc
    if denominator_poly.degree() != 0:
        raise ValueError("angular integrand is rational but not polynomial in x=cos(theta)")
    return x, polynomial.as_expr() / denominator_poly.as_expr()


def integrate_spherical_density(raw_density, theta):
    """Integrate an axisymmetric density over the sphere exactly."""
    x, polynomial = reduce_spherical_density(raw_density, theta)
    angular_integral = sp.integrate(polynomial, (x, -1, 1))
    if angular_integral.has(sp.Integral):
        raise ValueError("SymPy did not complete the exact polynomial integral")
    return sp.simplify(2 * sp.pi * angular_integral)


def verify_l2_harmonic_reduction():
    """Exact tests for Y_20 and its first two theta derivatives."""
    theta = sp.symbols("theta", real=True)
    x = sp.symbols("x_ang", real=True)
    y = sp.sqrt(sp.Rational(5, 16) / sp.pi) * (3 * sp.cos(theta)**2 - 1)
    y1 = sp.diff(y, theta)
    y2 = sp.diff(y, theta, 2)
    expected = (
        (sp.sqrt(sp.Rational(5, 16) / sp.pi) * (3*x**2 - 1))**2,
        (sp.sqrt(sp.Rational(5, 16) / sp.pi) * (-6*x*sp.sqrt(1-x**2)))**2,
        (sp.sqrt(sp.Rational(5, 16) / sp.pi) * (6 - 12*x**2))**2,
    )
    inputs = (sp.sin(theta)*y**2, sp.sin(theta)*y1**2, sp.sin(theta)*y2**2)
    outputs = []
    for density, target in zip(inputs, expected):
        _, got = reduce_spherical_density(density, theta)
        # The first derivative square has sin(theta)^2 after division by the
        # measure, so all expected expressions are polynomials in x.
        target_poly = sp.simplify(target.subs(sp.sqrt(1-x**2)**2, 1-x**2))
        residual = sp.simplify(got - target_poly)
        if residual != 0:
            raise AssertionError(f"l=2 angular derivative reduction residual: {residual}")
        outputs.append(got)
    norm = integrate_spherical_density(sp.sin(theta)*y**2, theta)
    if sp.simplify(norm - 1) != 0:
        raise AssertionError(f"Y20 normalization residual: {sp.simplify(norm - 1)}")
    return {"passed": True, "derivative_cases": len(outputs), "Y20_norm": str(norm)}

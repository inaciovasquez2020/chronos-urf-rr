from __future__ import annotations

import json
import sympy as sp
from gfe_polar_angular_reduction import (
    integrate_spherical_density,
    reduce_spherical_density,
    verify_l2_harmonic_reduction,
)


def main():
    harmonic = verify_l2_harmonic_reduction()
    theta = sp.symbols("theta", real=True)
    x = sp.symbols("x_ang", real=True)
    density = sp.sin(theta) * (1 + sp.cos(theta)**2 + sp.cos(theta)**4)
    reduced_x, polynomial = reduce_spherical_density(density, theta)
    assert sp.simplify(polynomial - (1 + x**2 + x**4)) == 0
    exact = integrate_spherical_density(density, theta)
    expected = 2 * sp.pi * sp.integrate(1 + x**2 + x**4, (x, -1, 1))
    assert sp.simplify(exact - expected) == 0

    # Regression: the metric determinant naturally yields Abs(sin(theta))
    # from sqrt(r**4*sin(theta)**2). On the spherical domain theta in [0, pi],
    # this is exactly sin(theta), so the reducer must handle it explicitly.
    r = sp.symbols("r", positive=True)
    metric_density = sp.sqrt(r**4 * sp.sin(theta)**2) * (
        1 + sp.cos(theta)**2 + sp.cos(theta)**4
    )
    _, metric_polynomial = reduce_spherical_density(metric_density, theta)
    metric_expected = r**2 * (1 + x**2 + x**4)
    assert sp.simplify(metric_polynomial - metric_expected) == 0
    metric_integral = integrate_spherical_density(metric_density, theta)
    metric_integral_expected = r**2 * expected
    assert sp.simplify(metric_integral - metric_integral_expected) == 0

    print(json.dumps({
        "schema": "gfe-polar-angular-reduction-test-v1",
        "passed": True,
        "l2_harmonic": harmonic,
        "polynomial_case": str(polynomial),
        "exact_integral": str(exact),
        "exact_integral_residual": str(sp.simplify(exact - expected)),
        "metric_determinant_regression": str(metric_polynomial),
        "metric_determinant_integral_residual": str(sp.simplify(metric_integral - metric_integral_expected)),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

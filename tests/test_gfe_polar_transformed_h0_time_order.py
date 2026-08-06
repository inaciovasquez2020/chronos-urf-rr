from __future__ import annotations
import sympy as s


def _mixed_h0_time_coefficient(mode: str, M: s.Symbol, r: s.Symbol) -> s.Expr:
    t, theta, phi = s.symbols("t theta phi", real=True)
    x, y = s.symbols("x y", real=True)
    f = 1 - 2 * M / r
    y20 = s.sqrt(s.Rational(5, 16) / s.pi) * (3 * s.cos(theta) ** 2 - 1)
    coordinates = (t, r, theta, phi)

    if mode == "H2":
        diagonal = (
            -f + x * f * y20,
            (1 + y * t**2 * y20 / 2) / f,
            r**2,
            r**2 * s.sin(theta) ** 2,
        )
    elif mode == "K":
        angular_factor = 1 + y * t**2 * y20 / 2
        diagonal = (
            -f + x * f * y20,
            1 / f,
            r**2 * angular_factor,
            r**2 * s.sin(theta) ** 2 * angular_factor,
        )
    else:
        raise ValueError(mode)

    metric = s.diag(*diagonal)
    inverse = s.diag(*(1 / entry for entry in diagonal))
    christoffel = [
        [[s.Integer(0) for _ in range(4)] for _ in range(4)]
        for _ in range(4)
    ]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                christoffel[a][b][c] = inverse[a, a] * (
                    s.diff(metric[a, c], coordinates[b])
                    + s.diff(metric[a, b], coordinates[c])
                    - s.diff(metric[b, c], coordinates[a])
                ) / 2

    riemann_up = [
        [
            [[s.Integer(0) for _ in range(4)] for _ in range(4)]
            for _ in range(4)
        ]
        for _ in range(4)
    ]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    value = (
                        s.diff(christoffel[a][b][d], coordinates[c])
                        - s.diff(christoffel[a][b][c], coordinates[d])
                    )
                    for e in range(4):
                        value += (
                            christoffel[a][c][e] * christoffel[e][b][d]
                            - christoffel[a][d][e] * christoffel[e][b][c]
                        )
                    riemann_up[a][b][c][d] = value

    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    operator = s.zeros(6)
    for row, (a, b) in enumerate(pairs):
        for column, (c, d) in enumerate(pairs):
            operator[row, column] = (
                metric[a, a]
                * riemann_up[a][b][c][d]
                * inverse[c, c]
                * inverse[d, d]
            )

    zero = {x: 0, y: 0, t: 0}
    derivative_matrices = []
    for take_x, take_y in ((False, False), (True, False), (False, True), (True, True)):
        matrix = s.zeros(6)
        for row in range(6):
            for column in range(6):
                value = operator[row, column]
                if take_x:
                    value = s.diff(value, x)
                if take_y:
                    value = s.diff(value, y)
                matrix[row, column] = s.factor(s.simplify(value.subs(zero)))
        derivative_matrices.append(matrix)

    background, lapse_variation, time_variation, mixed_variation = derivative_matrices
    trace_y = 3 * s.trace(background**2 * time_variation)
    trace_xy = 3 * s.trace(background**2 * mixed_variation) + 3 * s.trace(
        background
        * (lapse_variation * time_variation + time_variation * lapse_variation)
    )
    sqrt_g_0 = r**2 * s.sin(theta)
    sqrt_g_x = -r**2 * s.sin(theta) * y20 / 2
    density_xy = s.factor(s.simplify(sqrt_g_0 * trace_xy + sqrt_g_x * trace_y))
    integrated = s.integrate(
        density_xy,
        (phi, 0, 2 * s.pi),
        (theta, 0, s.pi),
    )
    return s.factor(8 * s.simplify(integrated))


def _gr_h0_operator(H2: s.Expr, K: s.Expr, r: s.Symbol, M: s.Symbol) -> s.Expr:
    return s.expand(
        r * (r - 2 * M) * s.diff(K, r, 2)
        - (r - 2 * M) * s.diff(H2, r)
        + (3 * r - 5 * M) * s.diff(K, r)
        - 4 * H2
        - 2 * K
    )


def test_transformed_h0_euler_equation_has_no_third_time_derivative() -> None:
    M, r, t = s.symbols("M r t", positive=True, real=True)
    h2mixed=_mixed_h0_time_coefficient("H2", M, r)
    kmixed=_mixed_h0_time_coefficient("K", M, r)
    print('mixed',h2mixed,kmixed)
    assert s.factor(h2mixed - 24*M**2/(r**3*(r-2*M)))==0
    assert s.factor(kmixed - 12*M*(M+6*r)/(r**3*(r-2*M)))==0
    H2hat=s.Function('H2hat')(t,r); Khat=s.Function('Khat')(t,r)
    f=1-2*M/r
    S=H2hat+2*Khat
    V=s.diff(H2hat,r)+2*(H2hat-Khat)/r
    radial_div=lambda W: f*s.diff(W,r)+(2*f/r+s.diff(f,r)/2)*W
    delta_r3=s.factor(2*M*(H2hat-Khat)/r**3+radial_div(V)-6*Khat/r**2-(f*s.diff(S,r,2)+(2*f/r+s.diff(f,r)/2)*s.diff(S,r))+6*S/r**2)
    gr=_gr_h0_operator(H2hat,Khat,r,M)
    print('delta',s.factor(delta_r3), 'gr',gr)
    assert s.simplify(gr+r**2*delta_r3/2)==0
    a=4*M/(3*r**2*(r-2*M))
    Htt=s.diff(H2hat,t,2); Ktt=s.diff(Khat,t,2)
    direct_h2=h2mixed/9; direct_k=kmixed/9
    transformed=s.factor(s.simplify(_gr_h0_operator(a*(Htt+Ktt),-a*Htt,r,M)+direct_h2*Htt+direct_k*Ktt))
    expected=s.factor(-4*M/(3*r**3*(r-2*M)**2)*(r**2*(r-2*M)**2*s.diff(Htt,r,2)-r*(r-2*M)*(2*r-M)*s.diff(Htt,r)+r*(2*r-M)*Htt+r*(r-2*M)**2*s.diff(Ktt,r)-(r-2*M)*(5*r-3*M)*Ktt))
    print('trans',transformed)
    assert s.simplify(transformed-expected)==0
    time_orders=[sum(v==t for v in d.variables) for d in transformed.atoms(s.Derivative)]
    print(time_orders,max(time_orders))
    assert max(time_orders)==2
    assert all(order<3 for order in time_orders)



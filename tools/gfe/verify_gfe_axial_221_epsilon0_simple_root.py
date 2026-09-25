#!/usr/bin/env python3
"""Verifier for the Schwarzschild axial (ell,m,n)=(2,2,1) root at epsilon=0.

This is a bounded projected-massless GfE certificate.  It proves only a
unique simple Schwarzschild root inside the stated frequency disk.  It does
not certify epsilon>0 continuation, dOmega/depsilon, the polar sector, or the
full unreduced trace-log spectrum.

The arithmetic core uses a 96-bit fixed-point affine center/sensitivity model
with outward-rounded scalar majorants.  Nonlinear remainders are transported
separately to avoid interval wrapping.
"""

import math

BITS = 96
S = 1 << BITS
INF = math.inf


def up(x):
    return math.nextafter(float(x), INF)


def dn(x):
    return math.nextafter(float(x), -INF)


def au_complex(z):
    return up(abs(z.real) + abs(z.imag))


def lo_complex(z):
    return dn(max(abs(z.real), abs(z.imag)))


def ulp_guard(x):
    x = float(x)
    return max(
        abs(math.nextafter(x, INF) - x),
        abs(x - math.nextafter(x, -INF)),
        2.0**-1074,
    )


def rnd_div(num, den):
    assert den > 0
    if num >= 0:
        return (2 * num + den) // (2 * den)
    return -((2 * (-num) + den) // (2 * den))


def ceil_div(num, den):
    assert num >= 0 and den > 0
    return (num + den - 1) // den


class A:
    __slots__ = ("cr", "ci", "lr", "li", "r")

    def __init__(self, c=0j, l=0j, r=0.0):
        if isinstance(c, A):
            self.cr, self.ci, self.lr, self.li, self.r = (
                c.cr,
                c.ci,
                c.lr,
                c.li,
                c.r,
            )
            return
        if not isinstance(c, complex):
            c = complex(float(c), 0.0)
        if not isinstance(l, complex):
            l = complex(float(l), 0.0)
        vals = []
        err = 0.0
        for x in (c.real, c.imag, l.real, l.imag):
            k = round(x * S)
            vals.append(int(k))
            err = up(err + abs(x - k / S) + 2 * ulp_guard(x))
        rr = up(float(r) + err)
        rad = max(0, math.ceil(up(rr * S))) + 4
        self.cr, self.ci, self.lr, self.li, self.r = (
            vals[0],
            vals[1],
            vals[2],
            vals[3],
            rad,
        )

    @classmethod
    def raw(cls, cr, ci, lr, li, r):
        o = object.__new__(cls)
        o.cr = int(cr)
        o.ci = int(ci)
        o.lr = int(lr)
        o.li = int(li)
        o.r = int(r)
        return o

    @staticmethod
    def co(x):
        return x if isinstance(x, A) else A(x)

    def center(self):
        return complex(self.cr / S, self.ci / S)

    def linear(self):
        return complex(self.lr / S, self.li / S)

    def rem(self):
        return up(self.r / S)

    def center_abs_upper(self):
        return up((abs(self.cr) + abs(self.ci)) / S)

    def linear_abs_upper(self):
        return up((abs(self.lr) + abs(self.li)) / S)

    def au(self):
        return up(
            (abs(self.cr) + abs(self.ci) + abs(self.lr) + abs(self.li) + self.r)
            / S
        )

    def dev(self):
        return up((abs(self.lr) + abs(self.li) + self.r) / S)

    def center_lower(self):
        return dn(max(abs(self.cr), abs(self.ci)) / S)

    def linear_lower(self):
        return dn(max(abs(self.lr), abs(self.li)) / S)

    def __add__(self, other):
        other = A.co(other)
        return A.raw(
            self.cr + other.cr,
            self.ci + other.ci,
            self.lr + other.lr,
            self.li + other.li,
            self.r + other.r,
        )

    __radd__ = __add__

    def __neg__(self):
        return A.raw(-self.cr, -self.ci, -self.lr, -self.li, self.r)

    def __sub__(self, other):
        return self + (-A.co(other))

    def __rsub__(self, other):
        return A.co(other) - self

    def __mul__(self, other):
        other = A.co(other)
        rn = self.cr * other.cr - self.ci * other.ci
        inn = self.cr * other.ci + self.ci * other.cr
        cr = rnd_div(rn, S)
        ci = rnd_div(inn, S)
        ec = abs(rn - cr * S) + abs(inn - ci * S)

        lrn = (
            self.cr * other.lr
            - self.ci * other.li
            + other.cr * self.lr
            - other.ci * self.li
        )
        lin = (
            self.cr * other.li
            + self.ci * other.lr
            + other.cr * self.li
            + other.ci * self.lr
        )
        lr = rnd_div(lrn, S)
        li = rnd_div(lin, S)
        el = abs(lrn - lr * S) + abs(lin - li * S)

        ca = abs(self.cr) + abs(self.ci)
        oa = abs(other.cr) + abs(other.ci)
        la = abs(self.lr) + abs(self.li)
        ola = abs(other.lr) + abs(other.li)
        cross = (
            ca * other.r
            + oa * self.r
            + la * ola
            + la * other.r
            + ola * self.r
            + self.r * other.r
        )
        rad = ceil_div(cross + ec + el, S) + 4
        return A.raw(cr, ci, lr, li, rad)

    __rmul__ = __mul__

    def inv(self):
        c = self.center()
        low = lo_complex(c)
        dev = self.dev()
        if not low > dev:
            raise AssertionError(("affine_inverse", low, dev, c, self.rem()))
        ic = 1 / c
        lin = -(self.linear()) / (c * c)
        rem = up(
            self.rem() / (low * low)
            + dev * dev / (low * low * dn(low - dev))
        )
        rem = up(
            rem
            + 32
            * max(
                ulp_guard(ic.real),
                ulp_guard(ic.imag),
                ulp_guard(lin.real),
                ulp_guard(lin.imag),
            )
        )
        return A(ic, lin, rem)

    def __truediv__(self, other):
        return self * A.co(other).inv()

    def __rtruediv__(self, other):
        return A.co(other) / self

    def __pow__(self, n):
        if n < 0:
            return self.inv() ** (-n)
        out = A(1.0)
        base = self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n //= 2
        return out

    def scale(self, q):
        if isinstance(q, complex):
            return self * A(
                q,
                0j,
                16 * max(ulp_guard(q.real), ulp_guard(q.imag)),
            )
        q = float(q)
        return self * A(q, 0j, 16 * ulp_guard(q))


OMEGA0 = complex(0.34671099687810465, -0.27391487535351058)
RROOT = 5e-6
O = A(OMEGA0, complex(RROOT, 0), 0)
OABS = up(au_complex(OMEGA0) + RROOT)


def zero_series(n):
    return [A(0.0) for _ in range(n)]


def conv(a, b, n):
    out = zero_series(n)
    for i in range(min(n, len(a))):
        for j in range(min(n - i, len(b))):
            out[i + j] = out[i + j] + a[i] * b[j]
    return out


def addser(a, b, n):
    return [
        (a[i] if i < len(a) else A(0)) + (b[i] if i < len(b) else A(0))
        for i in range(n)
    ]


def scaleser(a, q, n):
    return [
        (
            (a[i] if i < len(a) else A(0)) * q
            if isinstance(q, A)
            else (a[i] if i < len(a) else A(0)).scale(q)
        )
        for i in range(n)
    ]


def invlin(c, n):
    c = float(c)
    return [A(((-1.0) ** k) / (c ** (k + 1))) for k in range(n)]


def polyz(c, n):
    return [A(c), A(1.0)] + [A(0.0) for _ in range(max(0, n - 2))]


def horizon_coeffs(nmax):
    zi = invlin(2.0, nmax + 3)
    f = zero_series(nmax + 3)
    for n in range(1, nmax + 3):
        f[n] = zi[n - 1]
    fp = scaleser(conv(zi, zi, nmax + 3), 2.0, nmax + 3)
    aser = conv(f, f, nmax + 3)
    bser = conv(f, fp, nmax + 3)
    zi2 = conv(zi, zi, nmax + 3)
    zi3 = conv(zi2, zi, nmax + 3)
    v = addser(
        scaleser(zi2, 6.0, nmax + 3),
        scaleser(zi3, -6.0, nmax + 3),
        nmax + 3,
    )
    cser = zero_series(nmax + 3)
    cser[0] = O * O
    fv = conv(f, v, nmax + 3)
    cser = [cser[i] - fv[i] for i in range(nmax + 3)]
    alpha = O.scale(-2j)
    aa = [A(1.0)]
    for n in range(1, nmax + 1):
        an = alpha + A(float(n))
        den = aser[2] * an * (an - A(1.0)) + bser[1] * an + cser[0]
        low = A(0.0)
        for j in range(3, n + 3):
            k = n - j + 2
            ak = alpha + A(float(k))
            low += aser[j] * ak * (ak - A(1.0)) * aa[k]
        for j in range(2, n + 2):
            k = n - j + 1
            ak = alpha + A(float(k))
            low += bser[j] * ak * aa[k]
        for j in range(1, n + 1):
            low += cser[j] * aa[n - j]
        aa.append(-low / den)
    return aa


def horizon_majorant():
    radius = 1 / 8
    n0 = 40
    acoef = [0.0] * 11
    bcoef = [0.0] * 11
    ccoef = [0.0] * 11
    for j in range(9):
        acoef[j + 2] = math.comb(8, j) * 2.0 ** (8 - j)
    for j in range(8):
        bcoef[j + 1] = 2 * math.comb(7, j) * 2.0 ** (7 - j)
    for j in range(11):
        ccoef[j] += OABS * OABS * math.comb(10, j) * 2.0 ** (10 - j)
    for j in range(8):
        ccoef[j + 1] += 6 * math.comb(7, j) * 2.0 ** (7 - j)
    for j in range(7):
        ccoef[j + 1] += 6 * math.comb(6, j) * 2.0 ** (6 - j)
    ab = up(2 * OABS)
    numerator = 0.0
    for lag in range(1, 11):
        aval = acoef[lag + 2] if lag + 2 <= 10 else 0.0
        bval = bcoef[lag + 1] if lag + 1 <= 10 else 0.0
        cval = ccoef[lag]
        term = (
            aval * up((1 + ab / n0) * (1 + (1 + ab) / n0))
            + bval * up((1 + ab / n0) / n0)
            + cval / n0**2
        )
        numerator = up(numerator + up((radius**lag) * term))
    imabs = up(abs(OMEGA0.imag) + RROOT)
    denominator = dn(256 * (1 - 4 * imabs / n0))
    return up(numerator / denominator)


N_H = 32
aa = horizon_coeffs(N_H)
qmaj = horizon_majorant()
assert qmaj < 1, qmaj

RMAJ = 1 / 8
X0 = 1 / 16
RATIO = X0 / RMAJ
finite_max = 0.0
for n, coefficient in enumerate(aa):
    finite_max = max(finite_max, up(coefficient.au() * RMAJ**n))
assert finite_max <= 1.0000000001, finite_max

tail = up(RATIO ** (N_H + 1) / (1 - RATIO))
dtail = up(
    (1 / RMAJ)
    * RATIO**N_H
    * ((N_H + 1) - N_H * RATIO)
    / (1 - RATIO) ** 2
)
s_value = A(0)
s_derivative = A(0)
for n, coefficient in enumerate(aa):
    s_value += coefficient.scale(X0**n)
    if n:
        s_derivative += coefficient.scale(n * X0 ** (n - 1))
s_value.r += math.ceil(up(tail * S)) + 4
s_derivative.r += math.ceil(up(dtail * S)) + 4
assert s_value.center_lower() > s_value.dev()
L = s_derivative / s_value


def h_de_series(c, n):
    xi = invlin(c, n)
    zi = invlin(c + 2, n)
    xi2 = conv(xi, xi, n)
    z2 = conv(polyz(c + 2, n), polyz(c + 2, n), n)
    a0 = O.scale(-2j)
    g0 = a0 * (a0 - A(1))
    o2 = O * O
    d = addser(
        scaleser(xi, a0.scale(2), n),
        scaleser(conv(zi, xi, n), 2, n),
        n,
    )
    e = scaleser(xi2, g0, n)
    e = addser(e, scaleser(conv(zi, xi2, n), a0.scale(2), n), n)
    e = addser(e, conv(scaleser(z2, o2, n), xi2, n), n)
    e = addser(e, scaleser(conv(zi, xi, n), -6, n), n)
    e = addser(e, scaleser(conv(conv(zi, zi, n), xi, n), 6, n), n)
    return d, e


def h_bounds(c, radius):
    xlo = dn(c - radius)
    zlo = dn(c + 2 - radius)
    assert xlo > 0 and zlo > 0
    invx = up(1 / xlo)
    invz = up(1 / zlo)
    ab = up(2 * OABS)
    gb = up(ab * up(ab + 1))
    d0 = up(2 * ab * invx + 2 * invz * invx)
    f_lo = dn(xlo / (c + 2 + radius))
    assert f_lo > 0
    vb = up(6 * invz**2 + 6 * invz**3)
    cb = up(OABS**2 + up((c + radius) / (c + 2 - radius)) * vb)
    e0 = up(gb * invx**2 + 2 * ab * invz * invx**2 + cb / (f_lo * f_lo))
    return d0, e0


def find_h_bound(y, radius, d0, e0):
    bound = up(max(1.0, 2 * y))
    for _ in range(100):
        rhs = up(y + radius * up(bound * bound + d0 * bound + e0))
        lip = up(radius * (2 * bound + d0))
        if rhs <= bound and lip < 1:
            return bound
        bound = up(max(1.25 * bound, 1.05 * rhs))
    raise AssertionError(("horizon_local_majorant", y, radius, bound, lip))


def h_step_model(current, c, h, order, radius):
    assert current.r == 0
    dser, eser = h_de_series(c, order + 1)
    coeff = [current]
    for n in range(order):
        source = A(0)
        for k in range(n + 1):
            source += (
                coeff[k] * coeff[n - k]
                + dser[k] * coeff[n - k]
            )
        source += eser[n]
        coeff.append(source.scale(-1 / (n + 1)))
    out = A(0)
    hp = 1.0
    for coefficient in coeff:
        out += coefficient.scale(hp)
        hp *= h
    d0, e0 = h_bounds(c, radius)
    bound = find_h_bound(current.au(), radius, d0, e0)
    rho = abs(h) / radius
    truncation = up(bound * rho ** (order + 1) / (1 - rho))
    local = up(out.rem() + truncation)
    clean = A.raw(out.cr, out.ci, out.lr, out.li, 0)
    return clean, local, bound, d0, e0


def h_growth_bounds(current, remainder, c, h, bound, d0, e0):
    center = current.center()
    linear = current.linear_abs_upper()
    fbound = up(bound * bound + d0 * bound + e0)
    center_delta = up(h * fbound)
    midpoint = c + h / 2
    halfwidth = h / 2
    xlo = dn(midpoint - halfwidth)
    xup = up(midpoint + halfwidth)
    zlo = dn(midpoint + 2 - halfwidth)
    assert xlo > 0 and zlo > 0
    dcenter = (-4j * OMEGA0 / midpoint) + 2 / (midpoint * (midpoint + 2))
    dx_bound = up(
        4 * OABS / (xlo * xlo)
        + 4 * (xup + 1) / (xlo * xlo * zlo * zlo)
    )
    d_radius = up(4 * RROOT / xlo + halfwidth * dx_bound)
    growth_center = -2 * center - dcenter
    growth_radius = up(
        2 * (linear + remainder + center_delta) + d_radius
    )
    growth = up(growth_center.real + growth_radius)
    d1 = up(4 * RROOT / xlo)
    flo = dn(xlo / (xup + 2))
    assert flo > 0
    e2 = up(
        4 * RROOT * RROOT / (xlo * xlo)
        + RROOT * RROOT / (flo * flo)
    )
    forcing = up(linear * linear + d1 * linear + e2)
    return growth, 1.0, forcing


h_remainder = L.rem()
L = A.raw(L.cr, L.ci, L.lr, L.li, 0)
x = X0
horizon_steps = 0
while x < 1 - 1e-18:
    if x < 1 / 8:
        h = 1 / 1024
    elif x < 1 / 4:
        h = 1 / 512
    elif x < 1 / 2:
        h = 1 / 256
    elif x < 7 / 8:
        h = 1 / 512
    else:
        h = 1 / 1024
    if x + h > 1:
        h = 1 - x
    radius = min(4 * h, x / 16)
    next_l, local, bound, d0, e0 = h_step_model(
        L, x, h, 12, radius
    )
    growth, nonlinear, forcing = h_growth_bounds(
        L, h_remainder, x, h, bound, d0, e0
    )
    bootstrap = up(max(2 * h_remainder, 1e-8))
    for _ in range(64):
        rhs = up(
            h_remainder
            + h
            * (
                max(growth, 0.0) * bootstrap
                + nonlinear * bootstrap * bootstrap
                + forcing
            )
        )
        if rhs <= bootstrap:
            break
        bootstrap = up(max(1.25 * bootstrap, 1.05 * rhs))
    else:
        raise AssertionError(("horizon_error_bootstrap", x))
    denominator = dn(1 - growth * h)
    assert denominator > 0
    h_remainder = up(
        (
            h_remainder
            + h * (forcing + nonlinear * bootstrap * bootstrap)
        )
        / denominator
        + local
    )
    L = next_l
    x += h
    horizon_steps += 1

alpha = O.scale(-2j)
q_horizon = (alpha + L).scale(1 / 3) - O.scale(1j)
q_horizon_remainder = up(q_horizon.rem() + h_remainder / 3)
q_horizon = A.raw(
    q_horizon.cr,
    q_horizon.ci,
    q_horizon.lr,
    q_horizon.li,
    math.ceil(up(q_horizon_remainder * S)) + 4,
)


def laurent_coeffs(nmax):
    coeff = [A(0) for _ in range(nmax + 1)]
    for n in range(2, nmax + 1):
        rhs = A(6 if n == 2 else -18 if n == 3 else 12 if n == 4 else 0)
        if n - 1 >= 2:
            rhs += coeff[n - 1].scale(n - 1)
        if n - 2 >= 2:
            rhs -= coeff[n - 2].scale(2 * (n - 2))
        square = A(0)
        for j in range(2, n - 1):
            square += coeff[j] * coeff[n - j]
        coeff[n] = (rhs - square) / O.scale(2j)
    return coeff


N_J = 14
jost_coeff = laurent_coeffs(N_J)
zstart = 3 + 32j
iz = 1 / zstart
q_infinity = A(0)
power = 1 + 0j
for n in range(1, N_J + 1):
    power *= iz
    if n >= 2:
        q_infinity += jost_coeff[n].scale(power)

rho = 1 / 32
qbound = 0.0
resbound = 0.0
for n in range(2, N_J + 1):
    qbound = up(qbound + up(jost_coeff[n].au() * rho**n))
for n in range(N_J + 1, 2 * N_J + 2):
    residual = A(0)
    if 2 <= n - 1 <= N_J:
        residual -= jost_coeff[n - 1].scale(n - 1)
    if 2 <= n - 2 <= N_J:
        residual += jost_coeff[n - 2].scale(2 * (n - 2))
    for j in range(2, N_J + 1):
        k = n - j
        if 2 <= k <= N_J:
            residual += jost_coeff[j] * jost_coeff[k]
    resbound = up(resbound + up(residual.au() * rho**n))

remin = dn(OMEGA0.real - RROOT)
pdelta = 2 * rho
pinv = up(1 / (1 - pdelta))
damping = dn(
    2 * remin
    - 2 * OABS * pdelta * pinv
    - 2 * qbound * pinv
)
forcing = up(resbound * pinv)
nonlinear = pinv
jost_tail = 1e-9
assert damping > 0
assert dn(damping * jost_tail) >= up(
    forcing + nonlinear * jost_tail * jost_tail
)
assert up(2 * nonlinear * jost_tail) < damping
q_infinity.r += math.ceil(up(jost_tail * S)) + 4


def invz_series(zc, n):
    iz = 1 / zc
    out = []
    power = iz
    for k in range(n):
        if k == 0:
            phase = 1 + 0j
        elif k % 4 == 1:
            phase = 1j
        elif k % 4 == 2:
            phase = -1 + 0j
        else:
            phase = -1j
        out.append(A(phase * power))
        power *= iz
    return out


def infinity_series(s0, n):
    zc = 3 + 1j * (32 - s0)
    zi = invz_series(zc, n)
    zi2 = conv(zi, zi, n)
    zi3 = conv(zi2, zi, n)
    zi4 = conv(zi3, zi, n)
    pser = [A(1)] + [A(0) for _ in range(n - 1)]
    pser = addser(pser, scaleser(zi, -2, n), n)
    qser = addser(
        scaleser(zi2, 6, n),
        scaleser(zi3, -18, n),
        n,
    )
    qser = addser(qser, scaleser(zi4, 12, n), n)
    return pser, qser


def infinity_bounds(s0, radius):
    t = abs(32 - s0)
    zlo = dn(max(3.0, t) - radius)
    assert zlo > 2
    plo = dn(1 - 2 / zlo)
    qbound = up(6 / zlo**2 + 18 / zlo**3 + 12 / zlo**4)
    return plo, qbound


def find_infinity_bound(y, radius, plo, qbound):
    bound = up(max(2 * y, 0.01))
    for _ in range(100):
        rhs = up(
            y
            + radius
            * up(bound * bound + 2 * OABS * bound + qbound)
            / plo
        )
        lip = up(radius * (2 * bound + 2 * OABS) / plo)
        if rhs <= bound and lip < 1:
            return bound
        bound = up(max(1.25 * bound, 1.05 * rhs))
    raise AssertionError(("infinity_local_majorant", y, radius, bound, lip))


def infinity_step_model(current, s0, h, order, radius):
    assert current.r == 0
    pser, qser = infinity_series(s0, order + 1)
    coeff = [current]
    for n in range(order):
        square = A(0)
        for k in range(n + 1):
            square += coeff[k] * coeff[n - k]
        rhs = (
            square.scale(1j)
            - O * coeff[n].scale(2)
            - qser[n].scale(1j)
        )
        correction = A(0)
        for k in range(1, n + 1):
            correction += pser[k] * coeff[n - k + 1].scale(n - k + 1)
        coeff.append((rhs - correction) / pser[0].scale(n + 1))
    out = A(0)
    hp = 1.0
    for coefficient in coeff:
        out += coefficient.scale(hp)
        hp *= h
    plo, qbound = infinity_bounds(s0, radius)
    bound = find_infinity_bound(current.au(), radius, plo, qbound)
    rho_local = abs(h) / radius
    truncation = up(
        bound * rho_local ** (order + 1) / (1 - rho_local)
    )
    local = up(out.rem() + truncation)
    clean = A.raw(out.cr, out.ci, out.lr, out.li, 0)
    return clean, local, bound, plo, qbound


def infinity_growth_bounds(
    current,
    remainder,
    s0,
    h,
    bound,
    plo,
    qbound,
):
    center = current.center()
    linear = current.linear_abs_upper()
    fbound = up(
        (bound * bound + 2 * OABS * bound + qbound) / plo
    )
    center_delta = up(h * fbound)
    qradius = up(linear + remainder + center_delta)

    zmid = 3 + 1j * (32 - (s0 + h / 2))
    zlo = dn(abs(zmid) - h / 2)
    assert zlo > 2
    pcenter = 1 - 2 / zmid
    pradius = up(h / (abs(zmid) * zlo))
    plow = dn(abs(pcenter) - pradius)
    assert plow > 0

    numerator_center = 2j * center - 2 * OMEGA0
    numerator_radius = up(2 * qradius + 2 * RROOT)
    growth_center = numerator_center / pcenter
    growth_radius = up(
        numerator_radius / plow
        + abs(numerator_center)
        * pradius
        / (abs(pcenter) * plow)
    )
    growth = up(growth_center.real + growth_radius)
    quadratic = up(1 / plo)
    parameter_forcing = up(
        (linear * linear + 2 * RROOT * linear) / plo
    )
    return growth, quadratic, parameter_forcing


infinity_remainder = q_infinity.rem()
q_infinity = A.raw(
    q_infinity.cr,
    q_infinity.ci,
    q_infinity.lr,
    q_infinity.li,
    0,
)
s = 0.0
infinity_steps = 0
while s < 32 - 1e-15:
    t = 32 - s
    if t > 16:
        radius = 1 / 4
    elif t > 8:
        radius = 1 / 8
    elif t > 4:
        radius = 1 / 16
    elif t > 2:
        radius = 1 / 32
    elif t > 1:
        radius = 1 / 64
    else:
        radius = 1 / 128
    h = radius / 4
    if s + h > 32:
        h = 32 - s

    next_q, local, bound, plo, qbound = infinity_step_model(
        q_infinity,
        s,
        h,
        14,
        radius,
    )
    growth, quadratic, parameter_forcing = infinity_growth_bounds(
        q_infinity,
        infinity_remainder,
        s,
        h,
        bound,
        plo,
        qbound,
    )
    bootstrap = up(max(2 * infinity_remainder, 1e-8))
    for _ in range(64):
        rhs = up(
            infinity_remainder
            + h
            * (
                max(growth, 0.0) * bootstrap
                + quadratic * bootstrap * bootstrap
                + parameter_forcing
            )
        )
        if rhs <= bootstrap:
            break
        bootstrap = up(max(1.25 * bootstrap, 1.05 * rhs))
    else:
        raise AssertionError(("infinity_error_bootstrap", s))

    denominator = dn(1 - growth * h)
    assert denominator > 0
    infinity_remainder = up(
        (
            infinity_remainder
            + h
            * (
                parameter_forcing
                + quadratic * bootstrap * bootstrap
            )
        )
        / denominator
        + local
    )
    q_infinity = next_q
    s += h
    infinity_steps += 1

q_infinity.r = math.ceil(up(infinity_remainder * S)) + 4

mismatch = q_horizon - q_infinity
linear_lower = mismatch.linear_lower()
error_upper = up(
    mismatch.center_abs_upper() + mismatch.rem()
)
margin = dn(linear_lower - error_upper)

print("GFE_AXIAL_221_EPSILON0_FAST_AFFINE")
print("OMEGA_CENTER :=", OMEGA0.real, OMEGA0.imag)
print("OMEGA_RADIUS :=", RROOT)
print("HORIZON_MAJORANT_Q :=", qmaj)
print("HORIZON_STEPS :=", horizon_steps)
print("INFINITY_DAMPING_LOWER :=", damping)
print("INFINITY_STEPS :=", infinity_steps)
print(
    "MISMATCH_CENTER :=",
    mismatch.center().real,
    mismatch.center().imag,
)
print(
    "MISMATCH_LINEAR :=",
    mismatch.linear().real,
    mismatch.linear().imag,
)
print("MISMATCH_REMAINDER :=", mismatch.rem())
print("ROUCHE_LINEAR_LOWER :=", linear_lower)
print("ROUCHE_ERROR_UPPER :=", error_upper)
print("ROUCHE_MARGIN :=", margin)
assert margin > 0, ("rouche", linear_lower, error_upper, margin)
print("RESULT := CERTIFIED_UNIQUE_SIMPLE_ROOT_DISK")

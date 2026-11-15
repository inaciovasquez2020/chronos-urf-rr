# Comparable pairs in the full expanding-circle diamond

**Result.** With full five-dimensional volume sampling and five-dimensional causal order, the comparable-pair probability is
(P_2^{(5)}(\varepsilon)=128/3003+(6400/189189)\varepsilon^2+O(\varepsilon^4)).
The exact coefficients were replayed with rational arithmetic. Lean verification and novelty assessment remain open.

## Model and sampling

Use the [pinned Cosmology expanding-circle metric](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/blob/1714d0e17ed4c4bfa7aff01019ffacca23397aaf/research/5d/EXPANDING_CIRCLE_STATUS.md). The circle coordinate has period (2\pi). The coordinate
(\eta=-e^{-ht}/h<0) gives the conformal factor ((-h\eta)^{-2}) multiplying the flat product metric.

Place the tips at the same spatial and circle coordinates with conformal times (\eta_0\pm\delta). Require (0<\delta<\min(-\eta_0,\pi)). Causal paths through the diamond lift to the common tip-centered interval in the circle cover. A path from the earlier tip through a pair to a different lift of the later tip would need circle displacement at least (2\pi) over conformal duration (2\delta<2\pi). Thus the flat covering-space order agrees with the cylinder order on this diamond.

In scaled coordinates (s=(\eta-\eta_0)/\delta), the unit diamond satisfies (|s|+r<1), where (r) includes all four spatial coordinates. The density relative to flat uniform sampling is proportional to (w(s)=(1-\varepsilon s)^{-5}), with (\varepsilon=\delta/(-\eta_0)). The exponent comes from the five-dimensional volume form.

## Exact coefficient

With flat expectation (E) and comparability indicator (I), the full probability is (E[Iw(s_1)w(s_2)]/E[w]^2). Set (x=(1+s+r)/2, y=(1+s-r)/2). The normalized radial measure is (20(x-y)^3 dx,dy) on (0<y<x<1). The past subdiamond fraction is (u=(xy)^{5/2}), and the future fraction is (v=((1-x)(1-y))^{5/2}). Their sum (q=u+v) is the conditional comparability probability.

The past subdiamond time centroid is ((s-1)/2), by reflection in the midpoint of its tips. The future centroid is ((s+1)/2). Time reflection therefore gives (E[I s_1s_2]=E[s(s-1)u]). Expanding the density and the normalizer gives the quadratic coefficient (30\operatorname{Cov}(s^2,q)+25 E[I s_1 s_2]). Time reflection makes the probability even in (\varepsilon). Analyticity near zero follows by uniformly expanding the density on the bounded diamond.

The flat coefficient agrees with the Myrheim–Meyer chain abundance. See Roy, Sinha and Surya, [The Discrete Geometry of a Small Causal Diamond](https://arxiv.org/abs/1212.0631).

## Exact replay

Run with SymPy available. Each polynomial monomial is integrated over the radial triangle with the displayed fractional weight.

```python
import sympy as S

x, y = S.symbols("x y")
s = x + y - 1

def moment(poly, power):
    return sum(
        20 * c / ((j + power + 1) * (i + j + 2 * power + 2))
        for (i, j), c in S.Poly(poly * (x - y)**3, x, y).terms()
    )

flat = S.Integer(0)
past = S.Rational(5, 2)
assert moment(1, flat) == 1
p0 = 2 * moment(1, past)
variance = moment(s**2, flat)
covariance = 2 * moment(s**2, past) - variance * p0
cross = moment(s * (s - 1), past)
assert p0 == S.Rational(128, 3003)
assert variance == S.Rational(1, 21)
assert covariance == S.Rational(1280, 292383)
assert cross == -S.Rational(256, 65637)
assert 30 * covariance + 25 * cross == S.Rational(6400, 189189)
print("DIRECT_5D_COMPARABLE_PAIR_COEFFICIENTS := PASS")
```

## What projection changes

Writing (r_3) for the visible spatial radius, the projected event density is proportional to
((1-\varepsilon s)^{-5}\sqrt{(1-|s|)^2-r_3^2})
relative to flat coordinate volume. The square root comes from the length of the circle-coordinate interval over each point of the base diamond.

Projection also loses causal information. For example, take zero visible spatial coordinates and scaled times (-1/4,1/4). The circle coordinates (0,0) give a comparable pair. The coordinates (-1/2,1/2) give an incomparable pair with the same projected coordinates. The inequalities are strict and persist on neighborhoods of positive measure. Thus testing 4D comparability on the projected sample strictly increases the comparable-pair probability relative to testing the original 5D order on that sample.

The [matched zero-mode comparison](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/778a7039bddd9441eb7c4aa69ff4561a35bc9165/docs/status/EXPANDING_CIRCLE_CHRONOS_PAIR_MATCH_2026_11_15.md) instead samples using the 4D Einstein-frame volume, with flat limiting probability (1/10). Full 5D sampling differs from that prediction for sufficiently small (\varepsilon). The comparison uses different observation prescriptions. An experimentally accessible signature, a predicted projected pair probability, and discrimination against a 4D model allowed to reproduce the projected event law remain open.

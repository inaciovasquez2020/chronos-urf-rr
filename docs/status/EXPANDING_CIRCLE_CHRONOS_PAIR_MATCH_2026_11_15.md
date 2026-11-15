# Chronos comparable pairs for the expanding-circle reduction

**Result:** The Einstein-frame zero mode of the specified expanding-circle model and a standalone four-dimensional Einstein–scalar model give identical finite-sample causal-order laws. On a comoving causal diamond their common comparable-pair probability is
`P₂ = 1/10 + (16/175) ε² + O(ε⁴)`.
This is a continuum derivation with exact rational checks of the coefficient. Lean verification and novelty assessment are open.

## Models and observation prescription

The source is [DFM-MKC Cosmology's expanding-circle construction](https://github.com/inaciovasquez2020/dfm-mkc-cosmology/blob/1714d0e17ed4c4bfa7aff01019ffacca23397aaf/research/5d/EXPANDING_CIRCLE_STATUS.md).
Use its 4D Einstein-frame zero mode, with a fixed parameter `h > 0`, proper time `τ > 0`, and
`a(τ)=(hτ/2)³`, `φ(τ)=√(3/2) log((hτ/2)²)`.
The standalone 4D comparator is Einstein gravity coupled to a canonical scalar with potential
`V(φ)=6h² exp(-√(2/3) φ)`, on the same spatially flat FLRW solution and with the same clock and volume prescription.
In units with reduced 4D Planck mass one, substitution gives
`H=3/τ`, `φ̇=√6/τ`, `V=24/τ²`,
`3H²=φ̇²/2+V`, `Ḣ=-φ̇²/2`, and `φ̈+3Hφ̇+V′=0`.
The 4D comparator can therefore be defined directly by its action and solution.

Integrating `dη=dτ/a(τ)` gives `η=-4/(h³τ²)<0`, `a=(-hη)^(-3/2)`. Use a diamond with tips at the same comoving position and conformal times `η₀±δ`, with `η₀<0` and `0<δ<-η₀`. Set `ε=δ/(-η₀)`, `η=η₀+δt`, and rescale comoving positions by `δ`. The diamond is then `|t|+r<1` in flat coordinates. Its causal order is the flat order, and the normalized Einstein-frame volume has density proportional to
`wε(t)=(1-εt)^(-6)` relative to flat uniform volume. The constant factors cancel upon normalization.

Use the iid volume sampling and unlabeled chain convention of [Chronos #1347](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1347). For any fixed sample size, both models use the same product measure and the same map from points to causal order. Their order laws therefore agree exactly for every `0<ε<1`. In particular the comparable-pair statistic has the same law, including the finite-sample uncertainty induced by this observation prescription.

## Comparable-pair coefficient

Write `E₀` for normalized flat uniform expectation. Let `I` indicate that two flat-sampled points are comparable. Then the common probability has the exact integral
`P₂(ε)=E₀[I wε(t₁)wε(t₂)] / E₀[wε(t)]²`,
with the numerator taken over independent flat points.

For a fixed point `(t,r)`, define `A=((1+t)²-r²)²` and `B=((1-t)²-r²)²`. The past and future subdiamond volume fractions are `A/16` and `B/16`. Thus `q=(A+B)/16` is its conditional comparability probability. The flat time centroid of either subdiamond is the midpoint time of its two tips by reflection about the spacetime midpoint. Hence
`E₀[I t₁t₂]=E₀[t((t-1)A+(t+1)B)]/32`.

Expanding `wε=1+6εt+21ε²t²+O(ε³)` and dividing by the squared normalization gives the quadratic coefficient
`42 Cov₀(t²,q)+36 E₀[I t₁t₂]`.
The moment values are `E₀[q]=1/10`, `E₀[t²]=1/15`,
`Cov₀(t²,q)=1/105` and `E₀[I t₁t₂]=-3/350`, giving `16/175`.
Time reflection makes the probability even in `ε`. The density and its integral are analytic near zero since `|t|≤1` and the normalizer is positive there, so the remainder starts at order four.

## Exact replay

Run this block with SymPy available. It checks the comparator field equations, conformal-time derivative, and rational moments. The monomial formula integrates over the half diamond and uses reflection; odd time moments vanish.

```python
from math import factorial
import sympy as S

h, tau = S.symbols("h tau", positive=True)
a = (h * tau / 2)**3
phi = S.sqrt(6) * S.log(h * tau / 2)
H = S.diff(a, tau) / a
V = 6 * h**2 * S.exp(-S.sqrt(S.Rational(2, 3)) * phi)
phi_dot = S.diff(phi, tau)
for residual in (
    3 * H**2 - phi_dot**2 / 2 - V,
    S.diff(H, tau) + phi_dot**2 / 2,
    S.diff(phi_dot, tau) + 3 * H * phi_dot - S.sqrt(S.Rational(2, 3)) * V,
    S.diff(-4 / (h**3 * tau**2), tau) - 1 / a,
):
    assert S.simplify(residual) == 0

t, r = S.symbols("t r")
A = ((1 + t)**2 - r**2)**2
B = ((1 - t)**2 - r**2)**2
q = (A + B) / 16

def moment(poly):
    return sum(
        12 * coefficient * S.Rational(
            factorial(i) * factorial(j + 3),
            (j + 3) * factorial(i + j + 4),
        )
        for (i, j), coefficient in S.Poly(poly, t, r).terms()
        if i % 2 == 0
    )

assert moment(q) == S.Rational(1, 10)
assert moment(t**2) == S.Rational(1, 15)
covariance = moment(t**2 * q) - moment(t**2) * moment(q)
cross = moment(t * ((t - 1) * A + (t + 1) * B)) / 32
assert covariance == S.Rational(1, 105)
assert cross == -S.Rational(3, 350)
assert 42 * covariance + 36 * cross == S.Rational(16, 175)
print("EXPANDING_CIRCLE_CHRONOS_PAIR_MATCH := PASS")
```

## Scope

This comparison uses the quotient's Einstein-frame causal order and volume. It leaves direct 5D sprinkling, projection of a 5D causal sample, nonzero Kaluza–Klein modes, circle stabilization, physical frame selection, and empirical signatures open. The reduced circle grows with `τ`, so the result supplies no late-time control of the zero-mode approximation. The comparable-pair statistic detects a change relative to flat sampling in this family, and has exactly zero discriminating power between the two matched models under the stated sampling law.

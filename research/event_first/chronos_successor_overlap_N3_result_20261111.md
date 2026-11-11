# Chronos–URF–RR: exact three-event successor-overlap correction

Date: 2026-11-11. Scope: finite randomized causal orders from iid uniform points in an Alexandrov diamond. Mathematical status: **PROVED (paper proof), not Lean-verified**. Bounded numerical validation: **COMPUTATION_PASS**. Minkowski uniform-tail convergence and gravitational dynamics: **OPEN**.

## Exact three-event first-birth density

Let D be a finite-volume, nonatomic causal domain and let X,Y,Z be iid from its normalized volume probability measure μ. Let S(x)=μ(J⁻(x)∩D), F(x)=μ(J⁺(x)∩D), and A(x)=1-S(x)-F(x). For three sampled events, choose a uniformly random linear extension of their induced causal order. Define h₃(x) as the first-birth spatial density relative to μ, i.e. the law of the first event has density h₃ against μ.

Let

    T(x)= ∫_{y≻x} μ({z∈D: z∥x and z≺y}) μ(dy).

Here z∥x means causal incomparability. Then the exact formula is

    h₃(x) = A(x)² + 4 F(x) A(x) + 3 F(x)² - T(x)
           = (1-S(x))² + 2F(x)(1-S(x)) - T(x).

As 0≤T(x)≤F(x)A(x), this improves the existing geometric first-birth envelopes exactly at N=3. For N=2, h₂(x)=1-S(x)+F(x).

**Proof.** Condition on the distinguished point X=x, then sample Y,Z iid. If either other point lies in the strict past of x, the first-birth probability of x is zero. If both lie in the future of x, it is one. If both are incomparable with x, it is 1/3. If exactly one is in the future and the other is incomparable, it is 2/3, except when the incomparable point precedes the future point, in which case it is 1/2. (The reversed relation would contradict transitivity.) The two permutations of the mixed case produce correction 2 × (1/6) T(x) = T(x)/3 to the conditional probability of x being first. Multiplication by 3 yields the displayed h₃(x).

For an Alexandrov diamond D=I(p,q), if x≺y, causal transitivity gives the more explicit expression

    μ({z: z∥x, z≺y}) = S(y)-S(x)-V(x,y),

where V(x,y)=μ(I(x,y)). Therefore

    T(x) = ∫_{y≻x}[S(y)-S(x)-V(x,y)]μ(dy).

This is an exact **correlation-overlap correction**, not an independence approximation.

## Four-dimensional exact integrated correction

In a 4D Minkowski diamond, normalized volumes satisfy S(x)=[τ(p,x)/τ(p,q)]⁴ and F(x)=[τ(x,q)/τ(p,q)]⁴. The exact causal-past volume-fraction density is

    f_S(s)=3s^(-1/2)+3log(s)-3s^(1/2),  0<s<1.

Integration gives E[S]=E[F]=1/20 and E[S²]=E[F²]=1/105. The mixed moment is the elementary null-coordinate polynomial integral

    E[SF] = ∫₀¹∫₀ᵘ 12(u-w)²(uw)²((1-u)(1-w))² dw du = 1/2100.

For y in the future diamond of x, the integral ∫_{y≻x}V(x,y) μ(dy) equals F(x)²/20 (one directional pair-comparability probability in four dimensions, or half the 1/10 ordering fraction).

Since E[∫_{y≻x}S(y) μ(dy)]=E[S²] by exchangeability,

    E[T] = E[S²] - E[SF] - E[F²]/20
         = 1/105 - 1/2100 - 1/2100 = 3/350.

Consequently the earlier N=3 geometric upper-envelope integral is

    E[(1-S)²+2F(1-S)] = 353/350,

while the exact correction is 3/350, so ∫h₃ dμ=1 as required. The formula is not a first-birth density approximation; it is exact at N=3.

## Validation receipt

Standalone standard-library certificate `chronos_successor_overlap_N3_audit_20261111.py`:
- Exhaustive checked all 14 relevant minimal distinguished-event cases arising from every transitively closed, three-element forward-edge configuration and all distinguished-event placements. A separate full permutation enumeration agrees with the case probabilities.
- Independently sampled 120,000 iid triples from the 4D diamond using a fixed seed (20261111), checked the mean upper envelope and T against exact rational integrals within a bounded stated tolerance.
- Observed upper envelope ≈1.008515 versus 353/350; observed correction ≈0.00810 versus 3/350; observed density integral ≈1.000415 (sampling error).
- Python run: PASS, no downloads or repository writes. Lean verification: NOT_RUN.

## Boundary and next theorem

This closes the N=3 correction but provides **no uniform-in-N error control**. The higher-N density depends on joint relations among more than two successor events and on the ratio of full linear-extension counts. An exact small-N formula should not be extrapolated to the iterated tail N→∞ then n→∞. Next: seek higher-order inclusion–exclusion / cluster bounds on the successor-overlap contribution, and test whether any sign or magnitude survives averaging.

Background (not novelty claims): Brightwell and Łuczak, *Order-invariant measures on causal sets*; Surya, *The causal set approach to quantum gravity* (2019), DOI 10.1007/s41114-019-0023-1.